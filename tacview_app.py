import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QFont

class TacviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tacview')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setFont(QFont('Courier', 10))
        layout.addWidget(self.textEdit)

        openButton = QPushButton('Open XML File')
        openButton.clicked.connect(self.openFile)
        layout.addWidget(openButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)")
        if fileName:
            self.processXMLFile(fileName)

    def processXMLFile(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        mission_name = root.find('Title').text if root.find('Title') is not None else 'Unknown Mission'
        start_time = self.parse_time(root.find('MissionTime').text) if root.find('MissionTime') is not None else 'Unknown'
        duration = root.find('Duration').text if root.find('Duration') is not None else 'Unknown'

        output = f"Mission Name: {mission_name}\n"
        output += f"Start Time: {start_time}\n"
        output += f"Duration: {duration}\n\n"

        output += "Events:\n"
        for event in root.findall('.//Event'):
            time = event.find('Time').text
            action = event.find('Action').text
            primary_object = event.find('PrimaryObject')
            if primary_object is not None:
                primary_name = primary_object.find('Name').text if primary_object.find('Name') is not None else 'Unknown'
                primary_type = primary_object.find('Type').text if primary_object.find('Type') is not None else 'Unknown'
                output += f"{time}: {primary_name} ({primary_type}) {action}\n"

        self.textEdit.setText(output)

    def parse_time(self, time_str):
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%H:%M:%S")

def main():
    app = QApplication(sys.argv)
    ex = TacviewApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
