import abc
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CommonGrip(QFrame):
    '''
    Объект, с помощью которого можно растягивать окно
    '''
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.dragged = False
        self.size = 3
        self.old_pos = None
        self.old_size = None
        self.drag = None

        self.setStyleSheet('background-color: #222;')
        self.cursor_style = Qt.ArrowCursor

    def mousePressEvent(self, event, mouse_event=None):
        '''
        Обработка события нажатия кнопки мыши
        '''
        if not self.window.isMaximized():
            self.old_pos = self.window.pos()
            self.old_size = self.window.size()
            self.drag = self.mapToGlobal(event.pos())
            self.dragged = True

    def enterEvent(self, event):
        '''
        Обработка события наведения курсора на элемент
        '''
        if not self.window.isMaximized():
            QApplication.setOverrideCursor(self.cursor_style)

    def leaveEvent(self, event):
        '''
        Обработка события выхода курсора за границы элемента
        '''
        if not self.dragged:
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        '''
        Обработка события отпускания кнопки мыши
        '''
        self.dragged = False

    def mouseMoveEvent(self, event, mouse_event=None):
        '''
        Обработка события движения мыши
        '''
        if not self.window.isMaximized():
            self.change_size(event)

    @abc.abstractmethod
    def change_size(self, event):
        '''
        Изменение размера окна
        '''
        pass


class RightGrip(CommonGrip):
    '''
    Правая сторона
    '''
    def __init__(self, window):
        super().__init__(window)

        self.setFixedWidth(self.size)
        self.cursor_style = Qt.SizeHorCursor

    def change_size(self, event):
        self.window.setGeometry(self.old_pos.x(), self.old_pos.y(),
                                max(self.old_size.width() + self.mapToGlobal(event.pos()).x() - self.drag.x(),
                                    self.window.minimumWidth()),
                                self.window.height())


class LeftGrip(CommonGrip):
    '''
    Левая сторона
    '''
    def __init__(self, window):
        super().__init__(window)

        self.setFixedWidth(self.size)
        self.cursor_style = Qt.SizeHorCursor

    def change_size(self, event):
        self.window.setGeometry(min(self.old_pos.x() + self.mapToGlobal(event.pos()).x() - self.drag.x(),
                                    self.old_pos.x() + self.old_size.width() - self.window.minimumWidth()),
                                self.old_pos.y(),
                                self.old_size.width() + self.drag.x() - self.mapToGlobal(event.pos()).x(),
                                self.window.height())


class BottomGrip(CommonGrip):
    '''
    Нижняя сторона
    '''
    def __init__(self, window):
        super().__init__(window)

        self.setFixedHeight(self.size)
        self.cursor_style = Qt.SizeVerCursor

    def change_size(self, event):
        self.window.setGeometry(self.old_pos.x(), self.old_pos.y(),
                                self.old_size.width(),
                                max(self.old_size.height() + self.mapToGlobal(event.pos()).y() - self.drag.y(),
                                    self.window.minimumHeight()))


class BottomLeftGrip(CommonGrip):
    '''
    Левый нижний угол
    '''
    def __init__(self, window):
        super().__init__(window)

        self.setFixedWidth(self.size)
        self.setFixedHeight(self.size)
        self.cursor_style = Qt.SizeBDiagCursor

    def change_size(self, event):
        self.window.setGeometry(min(self.old_pos.x() + self.mapToGlobal(event.pos()).x() - self.drag.x(),
                                    self.old_pos.x() + self.old_size.width() - self.window.minimumWidth()),
                                self.old_pos.y(),
                                self.old_size.width() + self.drag.x() - self.mapToGlobal(event.pos()).x(),
                                max(self.old_size.height() + self.mapToGlobal(event.pos()).y() - self.drag.y(),
                                    self.window.minimumHeight()))


class BottomRightGrip(CommonGrip):
    '''
    Правый нижний угол
    '''
    def __init__(self, window):
        super().__init__(window)

        self.setFixedWidth(self.size)
        self.setFixedHeight(self.size)
        self.cursor_style = Qt.SizeFDiagCursor

    def change_size(self, event):
        self.window.setGeometry(self.old_pos.x(), self.old_pos.y(),
                                max(self.old_size.width() + self.mapToGlobal(event.pos()).x() - self.drag.x(),
                                    self.window.minimumWidth()),
                                max(self.old_size.height() + self.mapToGlobal(event.pos()).y() - self.drag.y(),
                                    self.window.minimumHeight()))
