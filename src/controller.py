import json
import webbrowser

from PyQt5.QtWidgets import QFileDialog, QMessageBox

from .model import *
from .view import *
from .constants import PATH_TO_SAVE_APP_DATA, PATH_TO_SAVE_OPENED_FILES, DOCUMENTATION_LINK


class TextEditorController:
    '''
    Объект данного класса обеспечивает взаимодействие между графическим интерфейсом и данными приложения
    '''
    def __init__(self):
        self._model = TextEditorModel()
        self._view = None

        self.new_files_counter = 1

        was_saved_opened, files = self.check_for_opened_files()
        self._view = TextEditorView(self)

        if was_saved_opened:
            self.init_states(files)

        was_saved_app, settings = self.check_for_app_data()
        if was_saved_app:
            self._view.apply_settings(pos=settings["pos"], size=settings["size"])
            self.change_state(settings["index"])

    def run(self):
        '''
        Запуск приложения
        '''
        self._view.run()

    def check_for_opened_files(self):
        '''
        Проверка, оставались ли открытые файлы после прошлого сеанса с целью их открытия
        '''
        if os.path.isfile(PATH_TO_SAVE_OPENED_FILES):
            with open(PATH_TO_SAVE_OPENED_FILES, 'r') as file:
                cont = json.loads(file.read())

            if len(cont):
                return True, cont

        return False, None

    def check_for_app_data(self):
        '''
        Сохранение настроек от предыдущего сеанса
        '''
        if os.path.isfile(PATH_TO_SAVE_APP_DATA):
            with open(PATH_TO_SAVE_APP_DATA, 'r') as file:
                cont = json.loads(file.read())

            if len(cont):
                return True, cont

        return False, None

    def init_states(self, data):
        '''
        Инициализация данных о файлах из предыдущего сеанса
        '''
        for filename in data:
            slider_pos, cursor_pos = map(int, data[filename])
            if self._model.load(filename, slider_pos, cursor_pos):
                self._view.add_tab(self._model.get_text(), filename.split('/')[-1], slider_pos, cursor_pos)

        return self._model.get_number_of_states()

    def open_file(self):
        '''
        Открытие файла
        '''
        path = QFileDialog.getOpenFileName(None, 'Open file', os.path.curdir, "All files (*)")[0]
        if self._model.load(path):
            self._view.add_tab(self._model.get_text(), self._model.get_filename().split('/')[-1], 0, 0)
        else:
            index = self._model.find(path)
            self._model.change_state(index)
            self._view.switch_tab(index, self._model.get_text(),
                                  self._model.get_slider_pos(), self._model.get_cursor_pos())

    def change_state(self, index):
        '''
        Изменение активного файла
        '''
        if self._model.get_number_of_states() <= index or index == -1:
            return
        self._model.change_state(index)
        text = self._model.get_text()
        slider_pos = self._model.get_slider_pos()
        cursor_pos = self._model.get_cursor_pos()
        self._view.switch_tab(index, text, slider_pos, cursor_pos)

    def save_file(self):
        '''
        Сохранение активного файла
        '''
        if self._model.current_state:
            print(self._model.get_is_filename_actual())
            if not self._model.get_filename() or not self._model.get_is_filename_actual():
                self.save_file_as()
            else:
                with open(self._model.get_filename(), 'w') as file:
                    file.write(self._model.get_text())
                self._model.set_is_modified(False)
                self._view.remove_tab_star()

    def save_file_as(self):
        '''
        Сохранение активного файла как
        '''
        dialog = QFileDialog()
        options = dialog.options()
        options |= QFileDialog.DontConfirmOverwrite
        filename = dialog.getSaveFileName(None, 'Save file', os.path.curdir, "All files (*)", options=options)[0]

        if not filename:
            return

        if os.path.exists(filename):
            overwrite = QMessageBox.question(None, 'Overwrite',
                "Do you want to overwrite existing file?", QMessageBox.Yes | QMessageBox.No)
            if overwrite == QMessageBox.No:
                return
            else:
                self._model.set_not_actual_filename(filename)

        self._model.set_filename(filename)
        self._model.set_is_filename_actual(True)
        self._view.edit_current_tab(filename.split('/')[-1])
        self.save_file()

    def save_all(self):
        '''
        Сохранение всех открытых файлов
        '''
        count = self._model.get_number_of_states()
        for i in range(count):
            self.change_state(i)
            self.save_file()

    def create_file(self):
        '''
        Создание нового файла
        '''
        name = f"New file {self.new_files_counter}"
        self.new_files_counter += 1
        self._model.create()
        self._model.set_filename(name)
        self._view.add_tab(self._model.get_text(), self._model.get_filename().split('/')[-1], 0, 0)

    def close_file(self):
        '''
        Закрытие активного файла
        '''
        if not self._model.get_number_of_states():
            self.exit()

        if self._model.get_is_modified():
            save_before_close = QMessageBox.question(None, 'Save file',
                "Do you want to save the file before closing?", QMessageBox.Yes | QMessageBox.No)

            if save_before_close:
                self.save_file()

        index = self._view.get_tab_index()
        index = max(index - 1, 0)
        self._model.close_state()
        self._view.close_tab()

        if self._model.get_number_of_states():
            self.change_state(index)
        else:
            self._view.hide_find()

    def exit(self):
        '''
        Выход из приложения
        '''
        if self._model.get_count_unsaved():
            save_before_exit = QMessageBox.question(None, 'Save files',
                                                    "Do you want to save files before exiting?",
                                                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            if save_before_exit == QMessageBox.Cancel:
                return
            elif save_before_exit == QMessageBox.Yes:
                self.save_all()

        self.save_data()
        self._view.exit()

    def save_data(self):
        '''
        Сохранение данных о сеансе
        '''
        data_opened = {}
        for state in self._model.get_states():
            data_opened.setdefault(state.get_filename(), [state.get_slider_pos(), state.get_cursor_pos()])

        with open(PATH_TO_SAVE_OPENED_FILES, 'w') as file:
            file.write(json.dumps(data_opened, indent=4))

        data_app = {}
        window_pos, window_size = self._view.get_window_settings()
        data_app.setdefault("pos", window_pos)
        data_app.setdefault("size", window_size)
        data_app.setdefault("index", self._view.get_tab_index())

        with open(PATH_TO_SAVE_APP_DATA, 'w') as file:
            file.write(json.dumps(data_app, indent=4))

    def toggle_find(self):
        '''
        Переключение видимости окна поиска
        '''
        if self._model.get_number_of_states():
            self._view.toggle_find()

    def show_about(self):
        '''
        Открытие README проекта
        '''
        webbrowser.open(DOCUMENTATION_LINK)

    def update_text(self, text):
        '''
        Обновление состояния после изменения текста
        '''
        if not self._model.get_number_of_states():
            return
        if self._model.get_text() != text and not self._model.get_is_modified():
            self._model.set_is_modified(True)
            self._view.add_tab_star()
        self._model.set_text(text)

    def update_slider_pos(self, slider_pos):
        '''
        Обновление состояния после изменения положения слайдера
        '''
        if not self._model.get_number_of_states():
            return

        self._model.set_slider_pos(slider_pos)

    def update_cursor_pos(self, position, row, column):
        '''
        Обновление состояния после изменения положения курсора в тексте
        '''
        self._view.set_label_cursor_pos(row, column)

        if not self._model.get_number_of_states():
            return

        self._model.set_cursor_pos(position)

    def find(self, string):
        '''
        Поиск слова в тексте, начиная с текущего положения курсора
        '''
        pos = self._view.get_text_cursor_position()
        text = self._model.get_text()
        index = text[pos:].find(string)
        if index == -1:
            index = text.find(string)
            if index == -1:
                return
        else:
            index += pos

        self._view.scroll_to_index(index, len(string))

    def replace(self, old, new):
        '''
        Замена всех вхождений слова old на new
        '''
        text = self._model.get_text()
        text = text.replace(old, new)
        self._view.set_text(text)
