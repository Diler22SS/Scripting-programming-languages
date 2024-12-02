import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QComboBox, QFileDialog,
                             QTextEdit, QLineEdit)

class DataVisualizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('lab 5 qt')
        self.setGeometry(100, 100, 1200, 800)
        self.df = None

        # Основной интерфейс
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # Левая панель
        controls = QVBoxLayout()
        self.load_button = QPushButton('Загрузить CSV Файл')
        self.load_button.clicked.connect(self.load_data)
        controls.addWidget(self.load_button)

        self.stats_display = QTextEdit()
        self.stats_display.setReadOnly(True)
        controls.addWidget(QLabel('Статистика:'))
        controls.addWidget(self.stats_display)

        self.viz_selector = QComboBox()
        self.viz_selector.addItems(['Линейный График', 'Гистограмма', 'Круговая Диаграмма'])
        self.viz_selector.currentIndexChanged.connect(self.update_plot)
        controls.addWidget(QLabel('Тип Графика:'))
        controls.addWidget(self.viz_selector)

        self.date_input = QLineEdit(placeholderText='Date (YYYY-MM-DD)')
        self.value1_input = QLineEdit(placeholderText='Value1')
        self.value2_input = QLineEdit(placeholderText='Value2')
        self.category_input = QLineEdit(placeholderText='Category')
        controls.addWidget(QLabel('Добавить Данные:'))
        for widget in [self.date_input, self.value1_input, self.value2_input, self.category_input]:
            controls.addWidget(widget)

        self.add_data_button = QPushButton('Добавить')
        self.add_data_button.clicked.connect(self.add_manual_data)
        controls.addWidget(self.add_data_button)

        controls.addStretch()

        # Тут графики
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addLayout(controls)
        layout.addWidget(self.canvas)

    def load_data(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Открыть CSV файл', '', 'CSV Files (*.csv)')
        self.df = pd.read_csv(filename)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df.sort_values('Date', inplace=True)
        self.update_statistics()
        self.update_plot()

    def update_statistics(self):
        if self.df is not None:
            stats = f"Rows: {len(self.df)}\nColumns: {len(self.df.columns)}\n"
            df_stats = self.df[['Value1', 'Value2']].describe()
            stats += df_stats.to_string()
            self.stats_display.setText(stats)

    def update_plot(self):
        if self.df is None:
            return
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        plot_type = self.viz_selector.currentText()
        
        if plot_type == 'Линейный График':
            ax.plot(self.df['Date'], self.df['Value1'])
            ax.set(title='Линейный График', xlabel='Date', ylabel='Value1')

        elif plot_type == 'Гистограмма':
            ax.bar(self.df['Date'], self.df['Value2'])
            ax.set(title='Гистограмма', xlabel='Date', ylabel='Value2')

        elif plot_type == 'Круговая Диаграмма':
            ax.pie(self.df['Category'].value_counts(), labels=self.df['Category'].unique(), autopct='%1.1f%%')
            ax.set(title='Круговая Диаграмма')
        self.figure.tight_layout()  # Подгоняем элементы
        self.canvas.draw()

    def add_manual_data(self):
        if self.df is None:
            self.df = pd.DataFrame(columns=['Date', 'Value1', 'Value2', 'Category'])
        try:
            new_row = {
                'Date': self.date_input.text(),
                'Value1': float(self.value1_input.text()),
                'Value2': float(self.value2_input.text()),
                'Category': self.category_input.text()
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
            self.update_statistics()
            self.update_plot()
            for widget in [self.date_input, self.value1_input, self.value2_input, self.category_input]:
                widget.clear()
        except ValueError:
            pass  # Некорректные данные игнорируются

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizerApp()
    window.show()
    sys.exit(app.exec_())