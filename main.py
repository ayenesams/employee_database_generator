import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow  # new module

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(600, 200)
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
