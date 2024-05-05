import sys

from .grip import *
from .menu import *
from .search import *
from .status import *
from .text_area import *
from .title_bar import *
from .tab_bar import *


class TextEditorView:
    '''
    Представление приложения - надкласс над окном
    '''
    def __init__(self, controller):
        self.app = QApplication(sys.argv)

        self.controller = controller

        self.initUI()

    def initUI(self):
        '''
        Инициализация элементов интерфейса
        '''
        self._window = self.create_window()
        self._window.setWindowIcon(QIcon("image/app icon.png"))

        central_widget = QWidget()
        self._window.setCentralWidget(central_widget)

        layout = QGridLayout()
        self._window.centralWidget().setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._text_area = self.create_text_area()
        self._empty_space_label = self.create_empty_space_label()
        self.show_empty_label()
        self._search_entry = self.create_search_entry()

        self._left_grip = LeftGrip(self._window)
        self._right_grip = RightGrip(self._window)
        self._bottom_grip = BottomGrip(self._window)
        self._bottom_left_grip = BottomLeftGrip(self._window)
        self._bottom_right_grip = BottomRightGrip(self._window)

        self._menu_bar = self.create_menu_bar()
        self._title_bar = self.create_title_bar()
        self._tab_bar = self.create_tab_bar()
        self._status_bar = self.create_status_bar()

        layout.addWidget(self._left_grip, 1, 0, 4, 1)
        layout.addWidget(self._right_grip, 1, 2, 4, 1)
        layout.addWidget(self._bottom_grip, 5, 1, 1, 1)
        layout.addWidget(self._bottom_left_grip, 5, 0, 1, 1)
        layout.addWidget(self._bottom_right_grip, 5, 2, 1, 1)
        layout.addWidget(self._title_bar, 0, 0, 1, 3)
        layout.addWidget(self._tab_bar, 1, 1, 1, 1)
        layout.addWidget(self._status_bar, 4, 1, 1, 1)
        layout.addWidget(self._search_entry, 2, 1, 1, 1)
        layout.addWidget(self._text_area, 3, 1, 1, 1)
        layout.addWidget(self._empty_space_label, 3, 1, 1, 1, Qt.AlignCenter)

        self._window.show()

    def run(self):
        '''
        Запуск окна
        '''
        self.app.exec()

    def add_tab(self, text, filename, slider_pos, cursor_pos):
        '''
        Добавление новой вкладки
        '''
        self._tab_bar.addTab(filename)
        self.switch_tab(self._tab_bar.count() - 1, text, slider_pos, cursor_pos)
        self.hide_empty_label()

    def switch_tab(self, index, text, slider_pos, cursor_pos):
        '''
        Смена активной вкладки
        '''
        self._tab_bar.setCurrentIndex(index)
        self._text_area.set_text(text)
        self._text_area.set_cursor_pos(cursor_pos)
        self._text_area.set_vertical_slider_pos(slider_pos)
        self._text_area.setFocus()

    def get_tab_index(self):
        '''
        Получение номера открытой вкладки
        '''
        return self._tab_bar.currentIndex()

    def edit_current_tab(self, text):
        '''
        Изменение текста открытой вкладки
        '''
        self._tab_bar.setTabText(self.get_tab_index(), text)

    def close_tab(self):
        '''
        Закрытие открытой вкладки
        '''
        self._tab_bar.removeTab(self.get_tab_index())
        if not self._tab_bar.count():
            self.show_empty_label()

    def add_tab_star(self):
        '''
        Пометка звездой открытой вкладки
        '''
        self.edit_current_tab(self._tab_bar.tabText(self.get_tab_index()) + '*')

    def remove_tab_star(self):
        '''
        Снятие метки с открытой вкладки
        '''
        if self._tab_bar.tabText(self.get_tab_index()).endswith('*'):
            self.edit_current_tab(self._tab_bar.tabText(self.get_tab_index())[:-1])

    def scroll_to_index(self, index, length):
        '''
        Промотка текстового поля до нужного текста
        '''
        self._text_area.scroll_to_index(index, length)

    def hide_find(self):
        '''
        Скрытие фрейма поиска
        '''
        self._search_entry.hide()

    def toggle_find(self):
        '''
        Переключение видимости фрейма поиска
        '''
        if self._search_entry.isHidden():
            self._search_entry.show()
        else:
            self._search_entry.hide()

    def show_empty_label(self):
        '''
        Показ метки, заполняющей пустое место на экране
        '''
        self._text_area.hide()
        self._empty_space_label.resize(self._text_area.width(), self._text_area.height())
        self._empty_space_label.show()

    def hide_empty_label(self):
        '''
        Скрытие метки, показ текстового поля
        '''
        self._empty_space_label.hide()
        self._text_area.resize(self._empty_space_label.width(), self._empty_space_label.height())
        self._text_area.show()

    # Дальше идет создание всех элементов интерфейса

    def create_window(self):
        return TextEditorWindow(self.controller)

    def create_empty_space_label(self):
        empty_space_label = QLabel("Create new file\nor open existing\nto start working")
        empty_space_label.setFont(QFont("Arial", 20))
        empty_space_label.setMinimumHeight(300)
        return empty_space_label

    def create_text_area(self):
        return TextArea(self.controller)

    def create_menu_bar(self):
        submenu = self._window.menuBar()
        return MenuBar(submenu, self.controller, self._text_area)

    def create_title_bar(self):
        return TitleBar(self._window, self._menu_bar)

    def create_tab_bar(self):
        return TabBar(self.controller)

    def create_status_bar(self):
        return StatusBar(self._window)

    def create_search_entry(self):
        return SearchEntry(self._window, self.controller)

    def set_label_cursor_pos(self, row, column):
        '''
        Вывод текущего положения курсора в тексте
        '''
        self._status_bar.show_pos(row, column)

    def apply_settings(self, pos, size):
        '''
        Применение настроек от прошлого сеанса
        '''
        self._window.move(*pos)
        self._window.resize(*size)

    def get_window_settings(self):
        '''
        Получение настроек окна от текущего сеанса
        '''
        pos = self._window.pos().x(), self._window.pos().y()
        size = self._window.width(), self._window.height()
        return pos, size

    def exit(self):
        '''
        Остановка приложения
        '''
        self._window.destroy()
        sys.exit(0)

    def set_text(self, text):
        '''
        Установка текста
        '''
        slider_pos = self._text_area.get_vertical_slider_pos()
        self._text_area.set_text(text)
        self._text_area.set_vertical_slider_pos(slider_pos)

    def get_text_cursor_position(self):
        '''
        Получение позиции курсора в тексте
        '''
        return self._text_area.textCursor().position()


class TextEditorWindow(QMainWindow):
    '''
    Главное окно приложения
    '''
    def __init__(self, controller):
        self.controller = controller

        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setStyleSheet('background-color: #333;')

    def closeEvent(self, event):
        '''
        Перенаправление попыток закрытия окна
        '''
        self.controller.exit()
        event.ignore()
