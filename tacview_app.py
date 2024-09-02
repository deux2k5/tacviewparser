import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QTabWidget
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class TacviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = {}
        self.events = []
        self.stats = {}
        self.missionName = ""
        self.startTime = 0
        self.duration = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tacview')
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()

        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)

        self.infoTextEdit = QTextEdit()
        self.infoTextEdit.setReadOnly(True)
        self.infoTextEdit.setFont(QFont('Courier', 10))
        self.tabWidget.addTab(self.infoTextEdit, "Mission Info")

        self.statsTable = QTableWidget()
        self.tabWidget.addTab(self.statsTable, "Statistics")

        self.eventsTable = QTableWidget()
        self.tabWidget.addTab(self.eventsTable, "Events")

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
        self.parseXML(file_path)
        self.displayMissionInfo()
        self.displayStats()
        self.displayEvents()

    def parseXML(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        self.missionName = root.find('Title').text if root.find('Title') is not None else 'Unknown Mission'
        self.startTime = self.parse_time(root.find('MissionTime').text) if root.find('MissionTime') is not None else 0
        self.duration = int(root.find('Duration').text) if root.find('Duration') is not None else 0

        for event in root.findall('.//Event'):
            event_data = {
                'Time': float(event.find('Time').text),
                'Action': event.find('Action').text,
                'PrimaryObject': self.parse_object(event.find('PrimaryObject')),
                'SecondaryObject': self.parse_object(event.find('SecondaryObject')),
                'ParentObject': self.parse_object(event.find('ParentObject')),
                'Airport': self.parse_object(event.find('Airport'))
            }
            self.events.append(event_data)
            self.update_stats(event_data)

    def parse_object(self, obj):
        if obj is None:
            return None
        return {child.tag: child.text for child in obj}

    def update_stats(self, event):
        if event['PrimaryObject'] is None or 'Pilot' not in event['PrimaryObject']:
            return

        pilot = event['PrimaryObject']['Pilot']
        if pilot not in self.stats:
            self.stats[pilot] = {
                'Aircraft': event['PrimaryObject'].get('Name', 'Unknown'),
                'Group': event['PrimaryObject'].get('Group', 'Unknown'),
                'TakeOffs': 0,
                'Lands': 0,
                'Fired': 0,
                'Hit': 0,
                'Destroyed': 0,
                'Killed': {'Aircraft': 0, 'Helicopter': 0, 'Ship': 0, 'SAM/AAA': 0, 'Tank': 0, 'Car': 0, 'Infantry': 0},
                'FriendlyFire': 0
            }

        if event['Action'] == 'HasTakenOff':
            self.stats[pilot]['TakeOffs'] += 1
        elif event['Action'] == 'HasLanded':
            self.stats[pilot]['Lands'] += 1
        elif event['Action'] == 'HasFired':
            self.stats[pilot]['Fired'] += 1
        elif event['Action'] == 'HasBeenHitBy':
            self.stats[pilot]['Hit'] += 1
        elif event['Action'] == 'HasBeenDestroyed':
            self.stats[pilot]['Destroyed'] += 1
            if event['SecondaryObject'] and 'Pilot' in event['SecondaryObject']:
                killer = event['SecondaryObject']['Pilot']
                if killer in self.stats:
                    object_type = event['PrimaryObject']['Type']
                    if object_type not in self.stats[killer]['Killed']:
                        self.stats[killer]['Killed'][object_type] = 0
                    self.stats[killer]['Killed'][object_type] += 1
                    if event['PrimaryObject'].get('Coalition') == event['SecondaryObject'].get('Coalition'):
                        self.stats[killer]['FriendlyFire'] += 1

    def displayMissionInfo(self):
        info = f"Mission Name: {self.missionName}\n"
        info += f"Start Time: {self.displayTime(self.startTime)}\n"
        info += f"Duration: {self.displayTime(self.duration)}\n"
        self.infoTextEdit.setText(info)

    def displayStats(self):
        self.statsTable.setColumnCount(17)
        self.statsTable.setHorizontalHeaderLabels([
            "Pilot", "Aircraft", "Group", "Take-offs", "Landings", "Fired", "Aircraft Kills",
            "Helo Kills", "Ship Kills", "SAM Kills", "Tank Kills", "Car Kills", "Infantry Kills", "Team Kills", "Hit", "Destroyed"
        ])
        self.statsTable.setRowCount(len(self.stats))

        for row, (pilot, data) in enumerate(self.stats.items()):
            self.statsTable.setItem(row, 0, QTableWidgetItem(pilot))
            self.statsTable.setItem(row, 1, QTableWidgetItem(data['Aircraft']))
            self.statsTable.setItem(row, 2, QTableWidgetItem(data['Group']))
            self.statsTable.setItem(row, 3, QTableWidgetItem(str(data['TakeOffs'])))
            self.statsTable.setItem(row, 4, QTableWidgetItem(str(data['Lands'])))
            self.statsTable.setItem(row, 5, QTableWidgetItem(str(data['Fired'])))
            self.statsTable.setItem(row, 6, QTableWidgetItem(str(data['Killed'].get('Aircraft', 0))))
            self.statsTable.setItem(row, 7, QTableWidgetItem(str(data['Killed'].get('Helicopter', 0))))
            self.statsTable.setItem(row, 8, QTableWidgetItem(str(data['Killed'].get('Ship', 0))))
            self.statsTable.setItem(row, 9, QTableWidgetItem(str(data['Killed'].get('SAM/AAA', 0))))
            self.statsTable.setItem(row, 10, QTableWidgetItem(str(data['Killed'].get('Tank', 0))))
            self.statsTable.setItem(row, 11, QTableWidgetItem(str(data['Killed'].get('Car', 0))))
            self.statsTable.setItem(row, 12, QTableWidgetItem(str(data['Killed'].get('Infantry', 0))))
            self.statsTable.setItem(row, 13, QTableWidgetItem(str(data['FriendlyFire'])))
            self.statsTable.setItem(row, 14, QTableWidgetItem(str(data['Hit'])))
            self.statsTable.setItem(row, 15, QTableWidgetItem(str(data['Destroyed'])))

        self.statsTable.resizeColumnsToContents()

    def displayEvents(self):
        self.eventsTable.setColumnCount(3)
        self.eventsTable.setHorizontalHeaderLabels(["Time", "Type", "Action"])
        self.eventsTable.setRowCount(len(self.events))

        for row, event in enumerate(self.events):
            time_item = QTableWidgetItem(self.displayTime(self.startTime + event['Time']))
            self.eventsTable.setItem(row, 0, time_item)

            type_item = QTableWidgetItem(event['PrimaryObject'].get('Type', 'Unknown'))
            self.eventsTable.setItem(row, 1, type_item)

            action_text = f"{event['PrimaryObject'].get('Name', 'Unknown')} ({event['PrimaryObject'].get('Pilot', 'Unknown')}) {event['Action']}"
            if event['Action'] in ['HasFired', 'HasBeenHitBy']:
                action_text += f" {event['SecondaryObject'].get('Name', 'Unknown')}"
            action_item = QTableWidgetItem(action_text)
            self.eventsTable.setItem(row, 2, action_item)

            # Set row color based on event type
            row_color = self.get_row_color(event)
            for col in range(3):
                self.eventsTable.item(row, col).setBackground(row_color)

        self.eventsTable.resizeColumnsToContents()

    def get_row_color(self, event):
        if event['Action'] == 'HasBeenDestroyed':
            return QColor(211, 211, 211)  # Light gray
        elif event['Action'] == 'HasBeenHitBy':
            return QColor(255, 254, 224)  # Light yellow
        elif event['PrimaryObject'].get('Coalition') == 'Allies':
            return QColor(249, 216, 214)  # Light red
        elif event['PrimaryObject'].get('Coalition') == 'Enemies':
            return QColor(203, 228, 249)  # Light blue
        else:
            return QColor(211, 248, 211)  # Light green

    def parse_time(self, time_str):
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return (dt - datetime(1970, 1, 1)).total_seconds()

    def displayTime(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def main():
    app = QApplication(sys.argv)
    ex = TacviewApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
