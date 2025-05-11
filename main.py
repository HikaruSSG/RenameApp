import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import GUI
from file_operations import FileOperations

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('pen.ico'))
    file_operations = FileOperations()
    gui = GUI(file_operations)
    gui.show()
    sys.exit(app.exec_())
