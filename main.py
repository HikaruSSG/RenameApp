import sys
from PyQt5.QtWidgets import QApplication
from gui import GUI
from file_operations import FileOperations

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_operations = FileOperations()
    gui = GUI(file_operations)
    gui.show()
    sys.exit(app.exec_())
