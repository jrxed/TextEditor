from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QKeySequence
from PyQt5.QtWidgets import QMenuBar, QHBoxLayout, QMenu, QLabel, QAction, QShortcut


class MenuBar(QMenuBar):
    '''
    Меню
    '''
    def __init__(self, parent, controller, text_area):
        super().__init__(parent)
        self.controller = controller
        self.text_area = text_area
        self.items = []

        self.setFixedWidth(0)

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.init_actions()

    def add_menu_item(self, item):
        '''
        Добавления секции в меню
        '''
        self.layout().addWidget(item)
        self.addMenu(item)
        self.items.append(item)
        self.setFixedWidth(self.width() + item.width())

    def init_actions(self):
        '''
        Инициализация действий в меню
        '''
        file_item = MenuItem("File", self)

        save_action = MenuAction(None, "&Save file", file_item, lambda:
            file_item.execute_action(lambda: self.controller.save_file()), self.parent(), "Ctrl+S")

        save_as_action = MenuAction(None, "Save file as", file_item, lambda:
            file_item.execute_action(lambda: self.controller.save_file_as()), self.parent(), "Ctrl+Shift+S")

        open_action = MenuAction(None, "&Open file", file_item, lambda:
            file_item.execute_action(lambda: self.controller.open_file()), self.parent(), "Ctrl+O")

        new_action = MenuAction(None, "&New file", file_item, lambda:
            file_item.execute_action(lambda: self.controller.create_file()), self.parent(), "Ctrl+N")

        close_action = MenuAction(None, "Close file", file_item, lambda:
            file_item.execute_action(lambda: self.controller.close_file()), self.parent(), "Ctrl+W")

        exit_action = MenuAction(None, "&Exit", file_item, lambda:
            file_item.execute_action(lambda: self.controller.exit()), self.parent(), "Alt+f4")

        file_item.init_actions(save_action, save_as_action, open_action, new_action, close_action, None, exit_action)
        self.add_menu_item(file_item)

        edit_item = MenuItem("Edit", self)

        cut_action = MenuAction(None, "Cut", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.cut()), self.parent(), "Ctrl+X")

        copy_action = MenuAction(None, "&Copy", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.copy()), self.parent(), "Ctrl+C")

        paste_action = MenuAction(None, "Paste", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.paste()), self.parent(), "Ctrl+V")

        all_action = MenuAction(None, "Select &All", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.selectAll()), self.parent(), "Ctrl+A")

        find_action = MenuAction(None, "&Find", edit_item, lambda:
            edit_item.execute_action(lambda: self.controller.toggle_find()), self.parent(), "Ctrl+F")

        undo_action = MenuAction(None, "&Undo", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.undo()), self.parent(), "Ctrl+Z")

        redo_action = MenuAction(None, "&Redo", edit_item, lambda:
            edit_item.execute_action(lambda: self.text_area.redo()), self.parent(), "Ctrl+Y")

        edit_item.init_actions(cut_action, copy_action, paste_action,
                               all_action, find_action, None, undo_action, redo_action)
        self.add_menu_item(edit_item)

        help_item = MenuItem("Help", self)

        about_action = MenuAction(None, "&About", help_item, lambda:
        help_item.execute_action(lambda: self.controller.show_about()), self.parent())

        help_item.init_actions(about_action)
        self.add_menu_item(help_item)


class MenuItem(QMenu):
    '''
    Секция меню
    '''
    def __init__(self, text, master):
        super().__init__()

        self.master = master

        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFixedSize(40, 40)

        self.normal_style = '''
            color: white;
            border: 0;
            border-radius: 0;
            padding: 0;
            margin: 0;
        '''
        self.hover_style = '''
            background-color: #555;
            color: white;
            border: 0;
            border-radius: 0;
            padding: 0;
            margin: 0;
        '''
        self.setStyleSheet(self.normal_style)

        self.setFixedSize(40, 40)

        self.menu = QMenu(self)

        self.installEventFilter(self)
        self.menu.installEventFilter(self)

    def init_actions(self, *actions):
        '''
        Добавление действий в секцию меню
        '''
        for action in actions:
            if action:
                self.menu.addAction(action)
            else:
                self.menu.addSeparator()

    def eventFilter(self, source, event):
        '''
        Обработка событий
        '''
        if source == self:
            if event.type() == event.Enter:
                self.setStyleSheet(self.hover_style)
                self.menu.exec(self.mapToGlobal(QPoint(0, self.height())))

            elif event.type() == event.HoverLeave:
                self.setStyleSheet(self.normal_style)

        elif source == self.menu:
            if event.type() == event.MouseMove:
                cursor = QCursor()
                pos = cursor.pos()
                self_pos = self.master.mapToGlobal(self.pos())
                menu_pos = self.menu.pos()

                if (self_pos.x() > pos.x() or self_pos.x() + self.width() <= pos.x() or
                    self_pos.y() > pos.y() or self_pos.y() + self.height() <= pos.y()) and \
                        (menu_pos.x() > pos.x() or menu_pos.x() + self.menu.width() <= pos.x() or
                         menu_pos.y() > pos.y() or menu_pos.y() + self.menu.height() <= pos.y()):

                    self.setStyleSheet(self.normal_style)
                    self.menu.destroy()

        return super().eventFilter(source, event)

    def execute_action(self, command):
        '''
        Выполнение действия меню
        '''
        self.setStyleSheet(self.normal_style)
        command()


class MenuAction(QAction):
    '''
    Действие меню
    '''
    def __init__(self, icon, text, parent, command, main_menu, key_seq=None):
        if icon:
            super().__init__(icon, text, parent)
        else:
            super().__init__(text, parent)

        self.command = command
        self.triggered.connect(self.command)

        if key_seq:
            self.seq = QKeySequence(main_menu.tr(key_seq))
            shortcut = QShortcut(self.seq, main_menu)
            shortcut.activated.connect(command)
            self.setShortcut(self.seq)

        self.setStatusTip(''.join(c for c in text if c != '&'))
