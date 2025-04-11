import sys
from PyQt5 import QtWidgets
from ui.main_window import MainWindow

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.resize(1300, 900)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
