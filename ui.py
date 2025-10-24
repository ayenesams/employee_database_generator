import os
from typing import Optional
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtGui import QIntValidator

from generator import DataGenerator
from exporter import ExcelExporter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Database Generator")
        self.folder: Optional[str] = None
        self.df = None
        self.generator = DataGenerator(use_api=True)
        self.exporter = ExcelExporter()
        self._init_ui()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        hnum = QHBoxLayout()
        hnum.addWidget(QLabel("Number of employees:"))
        self.num_input = QLineEdit()
        self.num_input.setValidator(QIntValidator(1, 1000000))
        self.num_input.setPlaceholderText("Enter an integer (e.g. 100)")
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
        export_btn.clicked.connect(self.on_export)
        actions.addWidget(gen_btn)
        actions.addWidget(export_btn)
        layout.addLayout(actions)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        preview_label = QLabel("Preview (first up to 5 rows):")
        layout.addWidget(preview_label)
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(0)
        self.preview_table.setRowCount(0)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.preview_table)

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
        self.update_preview()  # show preview after generation

    def on_export(self):
        if self.df is None:
            QMessageBox.warning(self, "No data", "Please generate data first.")
            return
        if not self.folder:
            QMessageBox.warning(self, "No folder", "Please select a folder to save the Excel file.")
            return
        try:
            filepath = self.exporter.export(self.df, self.folder)
            self.status_label.setText(f"File Generated: {filepath}")
            QMessageBox.information(self, "Exported", f"File saved to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export Excel:\n{e}")

    def update_preview(self):
        # Clear preview if no data
        if self.df is None or self.df.empty:
            self.preview_table.clear()
            self.preview_table.setRowCount(0)
            self.preview_table.setColumnCount(0)
            return

        # Prepare up to first 5 rows
        preview_df = self.df.head(5)
        cols = list(preview_df.columns)
        self.preview_table.setColumnCount(len(cols))
        self.preview_table.setHorizontalHeaderLabels(cols)
        self.preview_table.setRowCount(len(preview_df))

        for r, (_, row) in enumerate(preview_df.iterrows()):
            for c, col in enumerate(cols):
                val = row[col]
                item = QTableWidgetItem(str(val))
                self.preview_table.setItem(r, c, item)

        # adjust header stretch for readability
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

