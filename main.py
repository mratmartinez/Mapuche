#!/usr/bin/python3

import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QMenuBar, QMenu

class MainWindow(QMainWindow):
    class MenuBar(QMenuBar):
        class ProjectMenuItem(QMenu):
            def __init__(self):
                super().__init__()
                self.setTitle('Project')
                self.new_button = self.addAction('New')
                self.exit_button = self.addAction('Exit')

                self.new_button.setDisabled(True)
                self.exit_button.triggered.connect(self.handle_exit_button_click)

            def handle_exit_button_click(self):
                sys.exit()

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
