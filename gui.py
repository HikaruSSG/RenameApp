from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QFileDialog, QLabel, QLineEdit, QCheckBox, QFrame)
from PyQt5.QtCore import Qt, QPoint, QSize
import os
from PyQt5 import QtGui

class GUI(QWidget):
    def __init__(self, file_operations):
        super().__init__()
        self.file_operations = file_operations
        self.setWindowTitle("RenaMe")

        app_icon = QtGui.QIcon()
        app_icon.addFile("pen 16.png", QSize(16, 16))
        app_icon.addFile("pen 32.png", QSize(32, 32))
        app_icon.addFile("pen 256.png", QSize(256, 256))
        self.setWindowIcon(app_icon)


        # Apply dark theme and gradient background
        self.setStyleSheet("""
            QWidget {
                background-color: #333;
                color: white;
                border: 2px solid #555;
            }
        """)

        self.m_drag = False
        self.m_start = QPoint(0, 0)

        self.layout = QVBoxLayout()
       
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0, 0, 0, 0)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                margin: 5px;
                width: 150px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #367C39;
            }
        """

        self.select_folder_button = QPushButton("Select Folder")
        self.select_folder_button.clicked.connect(self.select_folder)
        self.select_folder_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.select_folder_button, 1)

        self.select_all_button = QPushButton("Select All")
        self.select_all_button.clicked.connect(self.select_all)
        self.select_all_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.select_all_button, 1)
        
        self.rename_button = QPushButton("Rename Files")
        self.rename_button.clicked.connect(self.rename_files)
        self.rename_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.rename_button, 1)
        
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.file_operations.undo_rename)
        self.undo_button.setStyleSheet(button_style)
        self.button_layout.addWidget(self.undo_button, 1)
        
        button_row_layout = QHBoxLayout()
        button_row_layout.addLayout(self.button_layout)
        
        
        self.layout.addLayout(button_row_layout)

        # Add stretch to the main layout

        self.name_label = QLabel("Base Name:")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        self.layout.addWidget(self.name_input)

        self.file_table = QTableWidget()
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(["Select", "Name", "Type", "Size", "Order"])
        self.file_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.file_table.setSelectionMode(QTableWidget.SingleSelection)
        self.file_table.horizontalHeader().setStretchLastSection(True)
        self.file_table.setMinimumHeight(300)
        self.layout.addWidget(self.file_table)

        self.name_input.setStyleSheet("""
            QLineEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.file_table.setStyleSheet("""
            QTableWidget {
                background-color: #222;
                color: white;
                border: 1px solid #555;
            }
            QHeaderView::section {
                background-color: #333;
                color: white;
                border: none;
                padding: 4px;
            }
            QTableWidget::item {
                padding: 4px;
            }
            QTableWidget::item:selected {
                background-color: #444;
                color: white;
            }
        """)

        self.setLayout(self.layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.file_operations.set_folder_path(folder_path)
            self.populate_table()

    def populate_table(self):
        files = self.file_operations.list_files()
        # Sort files numerically
        files.sort(key=lambda x: self.file_operations.natural_sort_key(x[0]))
        self.file_data = []
        self.file_table.setRowCount(len(files))
        for row, file_data in enumerate(files):
            name, file_type, size = file_data
            self.file_data.append(file_data)
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            if self.file_table.rowCount() > row and self.file_table.item(row, 0) is not None:
                checkbox.setCheckState(self.file_table.item(row, 0).checkState())
            else:
                checkbox.setCheckState(Qt.Unchecked)
            self.file_table.setItem(row, 0, checkbox)
            self.file_table.setItem(row, 1, QTableWidgetItem(name))
            self.file_table.setItem(row, 2, QTableWidgetItem(file_type))
            self.file_table.setItem(row, 3, QTableWidgetItem(str(size)))
            self.file_table.setItem(row, 4, QTableWidgetItem(str(row + 1)))

        # Resize columns based on content
        self.file_table.resizeColumnsToContents()

    def rename_files(self):
        base_name = self.name_input.text()
        files_with_order = []
        for row in range(self.file_table.rowCount()):
            if self.file_table.item(row, 0).checkState() == Qt.Checked:
                name = self.file_data[row][0]
                order = int(self.file_table.item(row, 4).text())
                files_with_order.append((order, name))

        ordered_files = [name for order, name in sorted(files_with_order)]
        self.file_operations.rename_files(base_name, ordered_files)
        self.populate_table()

    def select_all(self):
        # Determine the current check state of the first checkbox
        if self.file_table.rowCount() > 0:
            first_item = self.file_table.item(0, 0)
            if first_item is not None:
                current_state = first_item.checkState()
                new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
                for row in range(self.file_table.rowCount()):
                    item = self.file_table.item(row, 0)
                    if item is not None:
                        item.setCheckState(new_state)
