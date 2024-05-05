from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton


class TitleBar(QFrame):
    '''
    Верхняя панель окна с кнопками управления приложением
    '''
    def __init__(self, parent, menu_bar):
        super().__init__(parent)

        self.master = parent
        self._menu_bar = menu_bar

        self.setStyleSheet('background-color: #222;')
        self.setFixedHeight(40)

        self.initUI()

    def initUI(self):
        '''
        Инициализация элементов управления
        '''
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._menu_bar)

        self.label = self.create_label()

        self.minimize_button = self.create_common_button(QIcon("image/minimize.png"), self.master.showMinimized)
        self.maximize_button = self.create_common_button(QIcon("image/to full-screen.png"), self.toggle_full_screen)
        self.close_button = self.create_close_button(QIcon("image/close.png"), self.master.close)

        layout.addWidget(self.label)
        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def create_label(self):
        '''
        Создание метки, за которую можно перемещать окно
        '''
        label = TitleLabel("Sigma Text Editor", self.master)
        label.set_style('''
            color: white;
            font-size: 20px;
            font: Arial;
            padding: 0 auto 0 auto;
            margin: 0;
        ''')

        return label

    def create_common_button(self, icon, command):
        '''
        Создание обычной (серой) кнопки
        '''
        button = TitleBarButton(icon, command)

        button.set_style('''
        TitleBarButton {
            border: 0;
            padding: 0;
            margin: 0;
            color: white;
            font-size: 20px;
            font: Arial;
        }
        TitleBarButton:hover {
            background-color: #555;
        }
        ''')

        return button

    def create_close_button(self, icon, command):
        '''
        Создание красной кнопки
        '''
        button = TitleBarButton(icon, command)

        button.set_style('''
        TitleBarButton {
            border: 0;
            padding: 0;
            margin: 0;
            color: white;
            font-size: 20px;
            font: Arial;
            color: white;
        }
        TitleBarButton:hover {
            background-color: #F33;
        }
        ''')

        return button

    def toggle_full_screen(self):
        '''
        Переключение режимов полного экрана и обычного
        '''
        if self.master.isMaximized():
            self.master.showNormal()
            self.maximize_button.setIcon(QIcon("../image/to full-screen.png"))
        else:
            self.master.showMaximized()
            self.maximize_button.setIcon(QIcon("../image/from full-screen.png"))

class TitleLabel(QLabel):
    '''
    Метка с возможностью перемещения окна с ее помощью
    '''
    def __init__(self, text, window):
        super().__init__(text)

        self.window = window
        self.setAlignment(Qt.AlignCenter)
        self.dragged = False
        self.drag_x = None
        self.drag_y = None
        self.old_pos = None

    def set_style(self, style):
        '''
        Установка данного стиля
        '''
        self.setStyleSheet(style)

    def mousePressEvent(self, event, mouse_event=None):
        '''
        Обработка нажатия кнопки мыши
        '''
        self.dragged = True
        self.drag_x = event.globalX()
        self.drag_y = event.globalY()
        self.old_pos = self.window.pos()

    def mouseMoveEvent(self, event, mouse_event=None):
        '''
        Обработка перемещения мыши с зажатой кнопкой
        '''
        if self.dragged:
            self.window.move(self.old_pos.x() + event.globalX() - self.drag_x,
                             self.old_pos.y() + event.globalY() - self.drag_y)

class TitleBarButton(QPushButton):
    '''
    Кнопка для оконной панели фиксированного размера
    '''
    def __init__(self, icon, command):
        super().__init__(icon=icon)

        self.master = self
        self.clicked.connect(command)

        self.setFixedSize(40, 40)

    def set_style(self, style):
        '''
        Установка данного стиля
        '''
        self.setStyleSheet(style)
