from PyQt5.QtWidgets import *


class SearchEntry(QFrame):
    '''
    Фрейм для поиска и замены
    '''
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.setStyleSheet("background-color: #222; border-bottom: 1px solid #555;")
        self.setFixedHeight(70)

        self.initUI()

    def initUI(self):
        '''
        Инициализация элементов управления
        '''
        layout = QGridLayout()
        self.setLayout(layout)

        self.search_field = self.createTextField()
        layout.addWidget(self.search_field, 0, 0)

        self.replace_field = self.createTextField()
        layout.addWidget(self.replace_field, 1, 0)

        self.find_button = self.createFindButton()
        layout.addWidget(self.find_button, 0, 1)

        self.replace_button = self.createReplaceButton()
        layout.addWidget(self.replace_button, 1, 1)

        self.close_button = self.createCloseButton()
        layout.addWidget(self.close_button, 0, 2)

        self.hide()

    def createTextField(self):
        '''
        Создание текстового поля
        '''
        text_field = QLineEdit()

        return text_field

    def get_find_input(self):
        '''
        Получения текста из поля поиска
        '''
        return self.search_field.text()

    def get_replace_input(self):
        '''
        Получение текста из поля замены
        '''
        return self.replace_field.text()

    def createFindButton(self):
        '''
        Создание кнопки поиска
        '''
        button = QPushButton("Find", self)

        button.clicked.connect(lambda: self.controller.find(self.get_find_input()))

        return button

    def createReplaceButton(self):
        '''
        Создание кнопки замены
        '''
        button = QPushButton("Replace all", self)

        button.clicked.connect(lambda: self.controller.replace(self.get_find_input(), self.get_replace_input()))

        return button

    def createCloseButton(self):
        '''
        Создания кнопки закрытия фрейма
        '''
        button = QPushButton("X", self)
        button.setFixedSize(20, 20)

        button.clicked.connect(self.hide)

        return button
