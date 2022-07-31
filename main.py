#!/usr/bin/python3

import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QMenuBar, QMenu

class MainWindow(QMainWindow):
    class MenuBar(QMenuBar):
        class ProjectMenuItem(QMenu):
            def __init__(self):
                super().__init__()
                self.structure = {
                    'title': 'Project',
                    'items': [
                        {
                            'name': 'New',
                            'disabled': True,
                            'shortcut': 'Ctrl+N'
                        },
                        {
                            'name': 'Exit',
                            'shortcut': 'Ctrl+Q',
                            'trigger': self.handle_exit_button_click
                        }
                    ]
                }

            def handle_exit_button_click(self):
                sys.exit(0)

            @property
            def structure(self):
                return self._structure

            @structure.setter
            def structure(self, structure):
                self._structure = structure
                self.setTitle(structure['title'])
                for item in structure['items']:
                    item_action = self.addAction(item.get('name'))
                    for key in item.keys():
                        match key:
                            case 'checkable':
                                item_action.setCheckable(item['checkable'])
                            case 'disabled':
                                item_action.setDisabled(item['disabled'])
                            case 'shortcut':
                                item_action.setShortcut(QKeySequence(item['shortcut']))
                            case 'trigger':
                                item_action.triggered.connect(item['trigger'])
                return

        def __init__(self):
            super().__init__()
            self.bar_items = [self.ProjectMenuItem()]
            return

        @property
        def bar_items(self):
            return self._items

        @bar_items.setter
        def bar_items(self, items_list):
            self._items = []
            for item in items_list:
                self._items.append(item)
                if item == None:
                    self.addSeparator()
                    continue
                self.addMenu(item)
            return

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(500, 500)

        self.menu_bar = self.MenuBar()
        return

    @property
    def menu_bar(self):
        return self._menu_bar

    @menu_bar.setter
    def menu_bar(self, menu_bar):
        self._menu_bar = menu_bar
        self.setMenuWidget(menu_bar) 
        return

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
