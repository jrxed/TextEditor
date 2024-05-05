from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QStatusBar

class StatusBar(QFrame):
    '''
    Статус бар - вывод подсказок и положения курсора в тексте
    '''
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent

        self.setMaximumHeight(20)
        self.setStyleSheet('background-color: #111;')

        self.initUI()

    def initUI(self):
        '''
        Инициализация элементов управления
        '''
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("font-size: 14px; color: white; margin-left: 5px;")
        self.status_label.setAlignment(Qt.AlignLeft)

        self.fake_status_bar = QStatusBar(self.master)
        self.master.setStatusBar(self.fake_status_bar)
        self.fake_status_bar.hide()
        self.fake_status_bar.messageChanged.connect(lambda:
            self.status_label.setText(self.fake_status_bar.currentMessage()))

        self.pos_label = QLabel()
        self.pos_label.setFont(QFont("Monospace", 11))
        self.pos_label.setStyleSheet("font-size: 14px; color: white; margin-right: 5px;")
        self.pos_label.setAlignment(Qt.AlignRight)

        layout.addWidget(self.status_label)
        layout.addWidget(self.pos_label)

    def show_pos(self, row, col):
        '''
        Отображения координат курсора в тексте
        '''
        self.pos_label.setText(f"row: {row:<4} col: {col:<4}")
