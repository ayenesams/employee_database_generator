import os
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QIntValidator

from generator import DataGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Database Generator")
        self.folder: Optional[str] = None
        self.df = None
        self.generator = DataGenerator(use_api=True)
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        hnum = QHBoxLayout()
        hnum.addWidget(QLabel("Number of employees:"))
        self.num_input = QLineEdit()
        hnum.addWidget(self.num_input)
        layout.addLayout(hnum)

        hfolder = QHBoxLayout()
        self.folder_label = QLabel("No folder selected")
        select_btn = QPushButton("Select Folder")
        select_btn.clicked.connect(self.select_folder)
        hfolder.addWidget(select_btn)
        hfolder.addWidget(self.folder_label)
        layout.addLayout(hfolder)

        actions = QHBoxLayout()
        gen_btn = QPushButton("Generate Data")
        gen_btn.clicked.connect(self.on_generate)
        export_btn = QPushButton("Export to Excel")
        actions.addWidget(gen_btn)
        actions.addWidget(export_btn)
        layout.addLayout(actions)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder = folder
            self.folder_label.setText(self.folder)

    def on_generate(self):
        num_text = self.num_input.text().strip()
        if not num_text:
            QMessageBox.warning(self, "Input required", "Please enter number of employees.")
            return
        try:
            n = int(num_text)
            if n <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Please enter a positive integer.")
            return
        self.df = self.generator.generate(n)
        QMessageBox.information(self, "Data Generated", f"Generated {len(self.df)} employees.")
        self.status_label.setText("")