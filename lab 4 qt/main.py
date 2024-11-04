import sys
from PyQt5 import QtWidgets, QtSql, QtCore

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
        self.setWindowTitle("Lab Qt")
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

        self.add_btn = QtWidgets.QPushButton("Добавить")
        self.update_btn = QtWidgets.QPushButton("Обновить")
        self.del_btn = QtWidgets.QPushButton("Удалить")

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()  # Используем QFormLayout для размещения полей ввода
        btn_layout = QtWidgets.QHBoxLayout()

        # Добавление полей ввода в form_layout
        form_layout.addRow("User ID:", self.postUserID_text)
        form_layout.addRow("Title:", self.postTitle_text)
        form_layout.addRow("Body:", self.postBody_text)

        # Кнопки
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.del_btn)

        # Добавление элементов в главный макет
        main_layout.addWidget(self.search_line)
        main_layout.addWidget(self.main_table)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)

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

        self.main_table.setModel(self.main_model)
        self.selection_model = self.main_table.selectionModel()

        # Signals
        self.add_btn.clicked.connect(self.add_record)
        self.del_btn.clicked.connect(self.delete_record)
        self.search_line.textChanged.connect(self.search_post)

        # Стилизация
        self.apply_styles()

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
        self.main_model.select()

    def clear_fields(self):
        self.postUserID_text.clear()
        self.postTitle_text.clear()
        self.postBody_text.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
