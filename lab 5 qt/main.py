import sys
import requests
import asyncio
import sqlite3
from PyQt5 import QtWidgets, QtSql, QtCore
from PyQt5.QtCore import QTimer


def create_connection():
    db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('posts.db')
    if not db.open():
        QtWidgets.QMessageBox.critical(None, "Database Error", "Cannot open database.")
        return False
    return True


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab5 Qt")
        self.resize(800, 600)

        # UI Components
        self.search_line = QtWidgets.QLineEdit()
        self.main_table = QtWidgets.QTableView()
        self.postUserID_text = QtWidgets.QLineEdit()
        self.postTitle_text = QtWidgets.QLineEdit()
        self.postBody_text = QtWidgets.QLineEdit()

        # Установка подсказок для полей ввода
        self.search_line.setPlaceholderText("Поиск по заголовку")
        self.postUserID_text.setPlaceholderText("User ID")
        self.postTitle_text.setPlaceholderText("Title")
        self.postBody_text.setPlaceholderText("Body")

        self.upload_btn = QtWidgets.QPushButton("Загрузить данные")
        self.add_btn = QtWidgets.QPushButton("Добавить")
        self.update_btn = QtWidgets.QPushButton("Обновить")
        self.del_btn = QtWidgets.QPushButton("Удалить")

        self.progress_bar = QtWidgets.QProgressBar()
        self.status_label = QtWidgets.QLabel("")
        
        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()  # Используем QFormLayout для размещения полей ввода
        btn_layout = QtWidgets.QHBoxLayout()
        
        # Добавление полей ввода в form_layout
        form_layout.addRow("User ID:", self.postUserID_text)
        form_layout.addRow("Title:", self.postTitle_text)
        form_layout.addRow("Body:", self.postBody_text)

        # Кнопки
        btn_layout.addWidget(self.upload_btn)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.del_btn)

        # Добавление элементов в главный макет
        main_layout.addWidget(self.search_line)
        main_layout.addWidget(self.main_table)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)

        # Database and model
        self.connection = create_connection()
        self.main_model = QtSql.QSqlTableModel()
        self.main_model.setTable("posts")
        self.main_model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.main_model.select()
        
        # Table headers
        self.main_model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.main_model.setHeaderData(1, QtCore.Qt.Horizontal, "User ID")
        self.main_model.setHeaderData(2, QtCore.Qt.Horizontal, "Title")
        self.main_model.setHeaderData(3, QtCore.Qt.Horizontal, "Body")
        
        # Worker setup
        self.upload_worker = PostUploader()
        self.upload_worker.progress_updated.connect(self.progress_bar.setValue)
        self.upload_worker.status_updated.connect(self.status_label.setText)
        self.upload_worker.finished.connect(self.on_upload_finished)

        self.update_worker = PostUpdater()
        self.update_worker.finished.connect(self.main_model.select) 

        # Подключение сигналов
        self.upload_btn.clicked.connect(self.start_upload)
        self.add_btn.clicked.connect(self.add_record)
        self.update_btn.clicked.connect(self.update_record)
        self.del_btn.clicked.connect(self.delete_record)
        self.search_line.textChanged.connect(self.search_post)
        
        self.main_table.setModel(self.main_model)

        self.update_timer = QTimer()
        self.update_timer.setInterval(10000)
        self.update_timer.timeout.connect(self.update_worker.start)
        self.update_timer.start()
        
        self.apply_styles()

        
    def start_upload(self):
        self.progress_bar.setValue(0)
        self.upload_worker.start()


    def on_upload_finished(self):
        QtWidgets.QMessageBox.information(self, "Загрузка завершена", "Данные успешно загружены в базу.")
        self.clear_fields()
    

    def add_record(self):
        row = self.main_model.rowCount()
        self.main_model.insertRow(row)
        self.main_model.setData(self.main_model.index(row, 1), self.postUserID_text.text())
        self.main_model.setData(self.main_model.index(row, 2), self.postTitle_text.text())
        self.main_model.setData(self.main_model.index(row, 3), self.postBody_text.text())
        if not self.main_model.submitAll():
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to add record.")
        else:
            self.clear_fields()


    def update_record(self):
        index = self.main_table.selectionModel().currentIndex()
        if not index.isValid():
            return        
        
        self.main_model.setData(self.main_model.index(index.row(), 1), self.postUserID_text.text())
        self.main_model.setData(self.main_model.index(index.row(), 2), self.postTitle_text.text())
        self.main_model.setData(self.main_model.index(index.row(), 3), self.postBody_text.text())

        if not self.main_model.submitAll():
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Не удалось обновить запись.")
        else:
            self.clear_fields()


    def delete_record(self):
        index = self.main_table.selectionModel().currentIndex()
        if index.isValid():
            self.main_model.removeRow(index.row())
            if not self.main_model.submitAll():
                QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete record.")
            else:
                self.clear_fields()


    def search_post(self):
        filter_str = f"title LIKE '%{self.search_line.text()}%'"
        self.main_model.setFilter(filter_str)
        self.clear_fields()


    def clear_fields(self):
        self.postUserID_text.clear()
        self.postTitle_text.clear()
        self.postBody_text.clear()
        self.main_model.select()


    def apply_styles(self):
        # Применяем стили к элементам интерфейса
        self.setStyleSheet("""
            QTableView {
                border: 1px solid #ccc;
                background-color: white;
            }
            QTableView::item {
                padding: 10px;
            }
        """)


class PostUploader(QtCore.QThread):
    progress_updated = QtCore.pyqtSignal(int)  # Сигнал для обновления прогресс-бара
    status_updated = QtCore.pyqtSignal(str)     # Сигнал для обновления статус-метки
    finished = QtCore.pyqtSignal()      # Сигнал для завершения загрузки

    def run(self):
        asyncio.run(self.upload_posts())

    async def upload_posts(self):
        self.status_updated.emit("Запуск выполнения запроса...")
        try:
            await asyncio.sleep(2)  # Имитируем задержку для демонстрации
            url = "https://jsonplaceholder.typicode.com/posts"
            response = requests.get(url)
            response.raise_for_status()
            posts = response.json()
            self.status_updated.emit("Запрос выполнен, данные получены.")
            await self.save_posts(posts)
        except Exception as e:
            self.status_updated.emit(f"Ошибка загрузки данных: {e}")
        self.status_updated.emit("Сохранение завершено.")
        self.finished.emit()
        
    async def save_posts(self, posts):
        self.status_updated.emit("Сохранение данных в базу...")
        
        with sqlite3.connect('posts.db') as connection:
            cursor = connection.cursor()
            for i, post in enumerate(posts):
                await asyncio.sleep(0.1)  # Имитируем задержку записи в БД
                cursor.execute(
                    "INSERT INTO posts(user_id, title, body) VALUES (?, ?, ?)",
                    (post["userId"], post["title"], post["body"])
                )
                self.progress_updated.emit(i + 1)  # Обновляем прогресс-бар
            connection.commit()
        # connection.close()


class PostUpdater(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self):
        super().__init__()
        self.db_lock = asyncio.Lock()

    def run(self):
        asyncio.run(self.check_for_updates())

    async def check_for_updates(self):
        try:
            await asyncio.sleep(2)
            url = "https://jsonplaceholder.typicode.com/posts"
            new_posts = requests.get(url).json()

            # Use the lock to ensure single access
            async with self.db_lock:
                with sqlite3.connect('posts.db') as connection:
                    cursor = connection.cursor()
                    for post in new_posts:
                        cursor.execute(
                            "INSERT OR IGNORE INTO posts(user_id, title, body) VALUES (?, ?, ?)",
                            (post["userId"], post["title"], post["body"])
                        )
                    connection.commit()
        except Exception as e:
            print(e)
        self.finished.emit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
