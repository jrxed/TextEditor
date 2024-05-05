from PyQt5.QtGui import QFont, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import QFrame, QTextEdit


class TextArea(QTextEdit):
    '''
    Поле для редактирования содержимого файла
    '''
    def __init__(self, controller):
        super().__init__()

        self.setStyleSheet("background-color: #222;")
        self.setFont(QFont("Monospace", 11))
        self.setFrameShadow(QFrame.Shadow(1))
        self.setMinimumHeight(300)

        self._text = ""
        self.controller = controller
        self.highlighter = PythonHighlighter(self.document())

        self.cursorPositionChanged.connect(
            lambda: self.controller.update_cursor_pos(self.textCursor().position(),
                                                      self.textCursor().blockNumber(),
                                                      self.textCursor().columnNumber()))
        self.textChanged.connect(lambda: self.controller.update_text(self.get_text()))
        self.verticalScrollBar().valueChanged.connect(
            lambda: self.controller.update_slider_pos(self.get_vertical_slider_pos()))

    def scroll_to_index(self, index, length):
        '''
        Промотка окна до выделенного куска текста
        '''
        self.select_text(index, index + length)

    def get_vertical_slider_pos(self):
        '''
        Получение положения слайдера
        '''
        return self.verticalScrollBar().sliderPosition()

    def set_vertical_slider_pos(self, pos):
        '''
        Установка значения слайдера
        '''
        self.verticalScrollBar().setSliderPosition(pos)

    def set_text(self, text):
        '''
        Установка текста
        '''
        self._text = text
        self.setPlainText(self._text)

    def get_text(self):
        '''
        Получение текста
        '''
        self._text = self.toPlainText()
        return self._text

    def select_text(self, start, end):
        '''
        Выбор текста на символах от start до end
        '''
        self.setFocus()
        cursor = self.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.KeepAnchor)
        self.setTextCursor(cursor)

    def set_cursor_pos(self, cursor_pos):
        '''
        Установка курсора на данную позицию в тексте
        '''
        cursor = self.textCursor()
        cursor.setPosition(cursor_pos)
        self.setTextCursor(cursor)


class PythonHighlighter(QSyntaxHighlighter):
    '''
    Подсветка синтаксиса Python
    (попытка реализации)
    '''
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.keywords = ["False",     "await",      "else",       "import",   "pass",
                         "None",      "break",      "except",     "in",       "raise",
                         "True",      "class",      "finally",    "is",       "return",
                         "and",       "continue",   "for",        "lambda",   "try",
                         "as",        "def",        "from",       "nonlocal", "while",
                         "assert",    "del",        "global",     "not",      "with",
                         "async",     "elif",       "if",         "or",       "yield"]

        self.functions = ["abs",      "aiter",      "all",        "anext",    "any",      "ascii",     "bin",
                          "bool",     "breakpoint", "bytearray",  "bytes",    "callable", "chr",       "classmethod",
                          "compile",  "complex",    "delattr",    "dict",     "dir",      "divmod",    "enumerate",
                          "eval",     "exec",       "filter",     "float",    "format",   "frozenset", "getattr",
                          "globals",  "hasattr",    "hash",       "help",     "hex",      "id",        "input",
                          "int",      "isinstance", "issubclass", "iter",     "len",      "list",      "locals",
                          "map",      "max",        "memoryview", "min",      "next",     "object",    "oct",
                          "open",     "ord",        "pow",        "print",    "property", "range",     "repr",
                          "reversed", "round",      "set",        "setattr",  "slice",    "sorted",    "staticmethod",
                          "str",      "sum",        "super",      "tuple",    "type",     "vars",      "zip"]

    def highlightBlock(self, text):
        '''
        Подсветка одной строки
        Замечение: по-другому фреймворк сделать не позволяет
        '''
        block_text = self.currentBlock().text() + ' '

        fmt = QTextCharFormat()
        fmt.setBackground(QColor("#222"))
        fmt.setForeground(QColor("#FFF"))
        self.setFormat(0, len(block_text), fmt)

        start = 0
        word = ""
        last_word = ""
        open_quotes = False
        last_quote = ""

        for index, char in enumerate(block_text):
            if open_quotes and char not in ("'", '"'):
                continue

            if char == '#' and not open_quotes:
                fmt.setForeground(QColor("red").lighter(120))
                self.setFormat(index, len(block_text) - index, fmt)
                break

            elif char in ("'", '"'):
                if not open_quotes:
                    start = index
                    last_quote = char
                    open_quotes = True

                elif char == last_quote:
                    fmt.setForeground(QColor("green").lighter(120))
                    self.setFormat(start, index - start + 1, fmt)
                    open_quotes = False

            elif char.isalpha() or char.isdigit() or char == '_':
                word += char
            else:
                if last_word == "def":
                    if word.startswith("__") and word.endswith("__"):
                        fmt.setForeground(QColor("purple").lighter(300))
                    else:
                        fmt.setForeground(QColor("cyan"))
                elif word in self.keywords:
                    fmt.setForeground(QColor("orange"))
                elif word in self.functions or word in ('self', 'cls') or\
                        (word.endswith("__") and word.startswith("__")):
                    fmt.setForeground(QColor("purple").lighter(300))
                elif word.isdigit():
                    fmt.setForeground(QColor("cyan"))
                else:
                    word = ''
                    last_word = word
                    continue

                self.setFormat(index - len(word), len(word), fmt)
                word = ''
                last_word = word
        else:
            if open_quotes:
                fmt.setForeground(QColor("green").lighter(120))
                self.setFormat(start, len(block_text) - start, fmt)
