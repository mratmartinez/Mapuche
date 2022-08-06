#!/usr/bin/python3

import sys

from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu

class MainWindow(QMainWindow):
    class MenuBar(QMenuBar):
        def __init__(self,*args):
            super().__init__()
            self.structure = list(args)
            return

        def get_menu(self, model):
            try:
                menu_title = model.get('title')
                menu = QMenu(menu_title)
                items = model.get('items')
            except TypeError as err:
                return None
            except KeyError as err:
                return menu
            except Exception as err:
                raise err
            
            if (type(items) not in [list, tuple]):
                return menu

            for item in items:
                if (item == None):
                    menu.addSeparator()
                    continue
                item_action = menu.addAction(item.get('name'))
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
            return menu

        @property
        def structure(self):
            return self._structure

        @structure.setter
        def structure(self, items_list):
            self._structure = []
            for item in items_list:
                item = self.get_menu(item)
                if item == None:
                    self.addSeparator()
                    continue
                self._structure.append(item)
                self.addMenu(item)
            return

    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(500, 500)

        self.menu_bar = self.MenuBar({
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
                            'trigger': lambda: sys.exit(0)
                        }
                    ]
                })
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
