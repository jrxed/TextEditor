import os


class TextEditorModel:
    '''
    Данные об открытых файлах
    '''
    def __init__(self):
        self.states = []
        self.count_unsaved = 0
        self.current_state = None

    def change_state(self, index):
        '''
        Смена активного файла
        '''
        self.current_state = self.states[index]

    def close_state(self):
        '''
        Закрытие активного файла
        '''
        if self.current_state.get_is_modified():
            self.count_unsaved -= 1
        self.states.remove(self.current_state)

    def load(self, filename, slider_pos=0, cursor_pos=0):
        '''
        Загрузка нового файла
        '''
        if not os.path.isfile(filename):
            return False

        if any(True for state in self.states if os.path.abspath(state.filename) == filename):
            return False

        with open(filename, 'r') as file:
            text = file.read()

        new_state = State(text, False, filename, True, slider_pos, cursor_pos)

        self.states.append(new_state)
        self.current_state = new_state

        return True

    def save(self, filename):
        '''
        Сохранение активного файла
        '''
        with open(filename, 'w') as file:
            file.write(self.current_state.get_text())

        self.current_state.set_is_modified(False)
        self.current_state.set_filename(filename)
        self.current_state.set_is_filename_actual(True)

    def create(self):
        '''
        Создание данных о новом файле
        '''
        new_state = State("", False, "", False, 0, 0)
        self.states.append(new_state)
        self.current_state = new_state

    def find(self, filename):
        '''
        Поиск файла с данным путем
        '''
        for i, state in enumerate(self.states):
            if os.path.abspath(state.filename) == filename:
                return i

        return -1

    def get_number_of_states(self):
        '''
        Количество открытых файлов
        '''
        return len(self.states)

    def get_count_unsaved(self):
        '''
        Количество несохраненных файлов
        '''
        return self.count_unsaved

    def set_not_actual_filename(self, filename):
        '''
        Обновление всех файлов с данным путем
        '''
        for state in self.states:
            if os.path.abspath(state.get_filename()) == os.path.abspath(filename):
                state.set_is_filename_actual(False)
                state.set_is_modified(True)
                self.count_unsaved += 1

    # Дальше куча геттеров и сеттеров, думаю, что для них и так понятно, что они делают

    def get_states(self):
        return self.states

    def set_text(self, text):
        self.current_state.set_text(text)

    def get_text(self):
        return self.current_state.get_text()

    def set_is_modified(self, is_modified):
        if is_modified and not self.current_state.get_is_modified():
            self.count_unsaved += 1
        elif not is_modified and self.current_state.get_is_modified():
            self.count_unsaved -= 1

        self.current_state.set_is_modified(is_modified)

    def get_is_modified(self):
        return self.current_state.get_is_modified()

    def set_filename(self, filename):
        self.current_state.set_filename(filename)

    def get_filename(self):
        return self.current_state.get_filename()

    def set_is_filename_actual(self, is_filename_actual):
        self.current_state.set_is_filename_actual(is_filename_actual)

    def get_is_filename_actual(self):
        return self.current_state.get_is_filename_actual()

    def set_slider_pos(self, slider_pos):
        self.current_state.set_slider_pos(slider_pos)

    def get_slider_pos(self):
        return self.current_state.get_slider_pos()

    def set_cursor_pos(self, cursor_pos):
        self.current_state.set_cursor_pos(cursor_pos)

    def get_cursor_pos(self):
        return self.current_state.get_cursor_pos()


class State:
    '''
    Класс, хранящий данные об одном файле
    '''
    def __init__(self, text, is_modified, filename, is_filename_actual, slider_pos, cursor_pos):
        self.text = text
        self.is_modified = is_modified
        self.filename = filename
        self.is_filename_actual = is_filename_actual
        self.slider_pos = slider_pos
        self.cursor_pos = cursor_pos

    # Аналогично куча геттеров и сеттеров

    def set_text(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def set_is_modified(self, is_modified):
        self.is_modified = is_modified

    def get_is_modified(self):
        return self.is_modified

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_is_filename_actual(self, is_filename_actual):
        self.is_filename_actual = is_filename_actual

    def get_is_filename_actual(self):
        return self.is_filename_actual

    def set_slider_pos(self, slider_pos):
        self.slider_pos = slider_pos

    def get_slider_pos(self):
        return self.slider_pos

    def set_cursor_pos(self, cursor_pos):
        self.cursor_pos = cursor_pos

    def get_cursor_pos(self):
        return self.cursor_pos
