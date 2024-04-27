from PyQt5.QtWidgets import *

class TabBar(QTabBar):
    '''
    Фрейм с вкладками открытых файлов
    '''
    def __init__(self, controller):
        super().__init__()
        self.setFixedHeight(32)

        self.style = '''
        TabBar {
            background: #333;          
        }
        TabBar::tab {
            height: 32px;
            background: #555;
            color: #FFF;
            font-size: 16px;
            border-bottom: 1px solid #555;
        }
        TabBar::tab:selected {
            background-color: #222;
            color: #FFF;
        }
        '''
        self.setStyleSheet(self.style)

        self.tabBarClicked.connect(lambda index: controller.change_state(index))

    def add_tab(self, text):
        '''
        Добавление новой вкладки
        '''
        self.addTab(text)
        index = self.count() - 1
        self.setFixedWidth((index + 1) * 40)
        self.setTabButton(index, QTabBar.ButtonPosition(1), TabCloseButton(self, index))


class TabCloseButton(QPushButton):
    '''
    Кнопка закрытия вкладки
    '''
    def __init__(self, tab_bar, tab_num):
        super().__init__()

        self.tab_bar = tab_bar
        self.num = tab_num

        self.clicked.connect(lambda: self.tab_bar.on_close_tab(self.num))

        self.setText("✕")
        self.setFixedSize(20, 20)
        self.setStyleSheet('''
        TabCloseButton {
            border: 0;
            padding: 0;
            margin: 0;
            color: white;
            font-size: 15px;
            font: Arial;
            background-color: #333;
        }
        TabCloseButton:hover {
            background-color: #444;
        }
        ''')