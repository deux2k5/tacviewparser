import sys
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem, QTabWidget, QLabel, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtCore import Qt, QSortFilterProxyModel

class Language:
    def __init__(self):
        self.translations = {
            'information': 'Information',
            'missionName': 'Mission Name',
            'missionTime': 'Mission Time',
            'missionDuration': 'Mission Duration',
            'statsByPilot': 'Statistics by Pilot',
            'pilotName': 'Pilot Name',
            'aircraft': 'Aircraft',
            'group': 'Group',
            'takeoff': 'Take-off',
            'landing': 'Landing',
            'firedArmement': 'Fired Armament',
            'killedAircraft': 'Killed Aircraft',
            'killedHelo': 'Killed Helicopter',
            'killedShip': 'Killed Ship',
            'killedSAM': 'Killed SAM/AAA',
            'killedTank': 'Killed Tank',
            'killedCar': 'Killed Car',
            'killedInfantry': 'Killed Infantry',
            'teamKill': 'Team Kill',
            'hit': 'Hit',
            'destroyed': 'Destroyed',
            'events': 'Events',
            'time': 'Time',
            'type': 'Type',
            'action': 'Action',
            'nothing': 'Nothing',
            'takeoff_long': 'Take-off',
            'landing_long': 'Landing',
            'firedArmement_long': 'Fired Armament',
            'hitBy': 'Hit By',
            'pilotStats': 'Pilot Statistics',
        }

    def L(self, key):
        return self.translations.get(key, key)

class TacviewApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = Language()
        self.events = []
        self.stats = {}
        self.missionName = ""
        self.startTime = 0
        self.duration = 0
        self.image_path = "objectIcons/"
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Tacview')
        self.setGeometry(100, 100, 1200, 800)

        layout = QVBoxLayout()

        self.tabWidget = QTabWidget()
        layout.addWidget(self.tabWidget)

        # Mission Info Tab
        self.infoWidget = QWidget()
        infoLayout = QVBoxLayout()
        self.infoWidget.setLayout(infoLayout)
        self.tabWidget.addTab(self.infoWidget, self.language.L("information"))

        # Statistics Tab
        statsWidget = QWidget()
        statsLayout = QVBoxLayout()
        self.statsSearchInput = QLineEdit()
        self.statsSearchInput.setPlaceholderText("Search pilots...")
        self.statsSearchInput.textChanged.connect(self.filterStats)
        statsLayout.addWidget(self.statsSearchInput)
        self.statsTable = QTableWidget()
        self.statsTable.setSortingEnabled(True)
        statsLayout.addWidget(self.statsTable)
        statsWidget.setLayout(statsLayout)
        self.tabWidget.addTab(statsWidget, self.language.L("statsByPilot"))

        # Events Tab
        eventsWidget = QWidget()
        eventsLayout = QVBoxLayout()
        self.eventsSearchInput = QLineEdit()
        self.eventsSearchInput.setPlaceholderText("Search events...")
        self.eventsSearchInput.textChanged.connect(self.filterEvents)
        eventsLayout.addWidget(self.eventsSearchInput)
        self.eventsTable = QTableWidget()
        self.eventsTable.setSortingEnabled(True)
        eventsLayout.addWidget(self.eventsTable)
        eventsWidget.setLayout(eventsLayout)
        self.tabWidget.addTab(eventsWidget, self.language.L("events"))

        openButton = QPushButton('Open XML File')
        openButton.clicked.connect(self.openFile)
        layout.addWidget(openButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def filterStats(self, text):
        for row in range(self.statsTable.rowCount()):
            pilot = self.statsTable.item(row, 0).text().lower()
            self.statsTable.setRowHidden(row, text.lower() not in pilot)

    def filterEvents(self, text):
        for row in range(self.eventsTable.rowCount()):
            event_text = self.eventsTable.item(row, 2).text().lower()
            self.eventsTable.setRowHidden(row, text.lower() not in event_text)

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

        self.events.sort(key=lambda x: x['Time'])

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
                'TakeOffs': {'Count': 0},
                'Lands': {'Count': 0},
                'Fired': {'Count': 0},
                'Hit': {'Count': 0},
                'Destroyed': {'Count': 0},
                'Killed': {'Aircraft': {'Count': 0}, 'Helicopter': {'Count': 0}, 'Ship': {'Count': 0}, 
                           'SAM/AAA': {'Count': 0}, 'Tank': {'Count': 0}, 'Car': {'Count': 0}, 'Infantry': {'Count': 0}},
                'FriendlyFire': {'Count': 0}
            }

        if event['Action'] == 'HasTakenOff':
            self.stats[pilot]['TakeOffs']['Count'] += 1
            airport = event['Airport']['Name'] if event['Airport'] else 'No Airport'
            self.stats[pilot]['TakeOffs'][airport] = self.stats[pilot]['TakeOffs'].get(airport, 0) + 1
        elif event['Action'] == 'HasLanded':
            self.stats[pilot]['Lands']['Count'] += 1
            airport = event['Airport']['Name'] if event['Airport'] else 'No Airport'
            self.stats[pilot]['Lands'][airport] = self.stats[pilot]['Lands'].get(airport, 0) + 1
        elif event['Action'] == 'HasFired':
            self.stats[pilot]['Fired']['Count'] += 1
            weapon = event['SecondaryObject']['Name']
            self.stats[pilot]['Fired'][weapon] = self.stats[pilot]['Fired'].get(weapon, 0) + 1
        elif event['Action'] == 'HasBeenHitBy':
            self.stats[pilot]['Hit']['Count'] += 1
            weapon = event['SecondaryObject']['Name']
            self.stats[pilot]['Hit'][weapon] = self.stats[pilot]['Hit'].get(weapon, 0) + 1
        elif event['Action'] == 'HasBeenDestroyed':
            self.stats[pilot]['Destroyed']['Count'] += 1
            if event['SecondaryObject'] and 'Pilot' in event['SecondaryObject']:
                killer = event['SecondaryObject']['Pilot']
                if killer in self.stats:
                    object_type = event['PrimaryObject']['Type']
                    self.stats[killer]['Killed'][object_type]['Count'] += 1
                    object_name = event['PrimaryObject']['Name']
                    self.stats[killer]['Killed'][object_type][object_name] = self.stats[killer]['Killed'][object_type].get(object_name, 0) + 1
                    if event['PrimaryObject'].get('Coalition') == event['SecondaryObject'].get('Coalition'):
                        self.stats[killer]['FriendlyFire']['Count'] += 1
                        self.stats[killer]['FriendlyFire'][object_name] = self.stats[killer]['FriendlyFire'].get(object_name, 0) + 1

    def displayMissionInfo(self):
        infoLayout = self.infoWidget.layout()
        for i in reversed(range(infoLayout.count())): 
            infoLayout.itemAt(i).widget().setParent(None)

        infoLayout.addWidget(QLabel(f"<h1>{self.language.L('information')}</h1>"))
        
        infoTable = QTableWidget(3, 2)
        infoTable.setHorizontalHeaderLabels([self.language.L('missionName'), self.language.L('missionTime'), self.language.L('missionDuration')])
        infoTable.setVerticalHeaderLabels([self.language.L('missionName'), self.language.L('missionTime'), self.language.L('missionDuration')])
        
        infoTable.setItem(0, 0, QTableWidgetItem(self.language.L('missionName')))
        infoTable.setItem(0, 1, QTableWidgetItem(self.missionName))
        infoTable.setItem(1, 0, QTableWidgetItem(self.language.L('missionTime')))
        infoTable.setItem(1, 1, QTableWidgetItem(self.displayTime(self.startTime)))
        infoTable.setItem(2, 0, QTableWidgetItem(self.language.L('missionDuration')))
        infoTable.setItem(2, 1, QTableWidgetItem(self.displayTime(self.duration)))
        
        infoTable.resizeColumnsToContents()
        infoTable.resizeRowsToContents()
        
        infoLayout.addWidget(infoTable)

    def displayStats(self):
        self.statsTable.clear()
        self.statsTable.setColumnCount(16)
        self.statsTable.setHorizontalHeaderLabels([
            self.language.L("pilotName"), self.language.L("aircraft"), self.language.L("group"),
            self.language.L("takeoff"), self.language.L("landing"), self.language.L("firedArmement"),
            self.language.L("killedAircraft"), self.language.L("killedHelo"), self.language.L("killedShip"),
            self.language.L("killedSAM"), self.language.L("killedTank"), self.language.L("killedCar"),
            self.language.L("killedInfantry"), self.language.L("teamKill"), self.language.L("hit"),
            self.language.L("destroyed")
        ])
        self.statsTable.setRowCount(len(self.stats))

        for row, (pilot, data) in enumerate(self.stats.items()):
            self.statsTable.setItem(row, 0, QTableWidgetItem(pilot))
            self.statsTable.setItem(row, 1, QTableWidgetItem(data['Aircraft']))
            self.statsTable.setItem(row, 2, QTableWidgetItem(data['Group']))
            self.statsTable.setItem(row, 3, QTableWidgetItem(str(data['TakeOffs']['Count'])))
            self.statsTable.setItem(row, 4, QTableWidgetItem(str(data['Lands']['Count'])))
            self.statsTable.setItem(row, 5, QTableWidgetItem(str(data['Fired']['Count'])))
            self.statsTable.setItem(row, 6, QTableWidgetItem(str(data['Killed']['Aircraft']['Count'])))
            self.statsTable.setItem(row, 7, QTableWidgetItem(str(data['Killed']['Helicopter']['Count'])))
            self.statsTable.setItem(row, 8, QTableWidgetItem(str(data['Killed']['Ship']['Count'])))
            self.statsTable.setItem(row, 9, QTableWidgetItem(str(data['Killed']['SAM/AAA']['Count'])))
            self.statsTable.setItem(row, 10, QTableWidgetItem(str(data['Killed']['Tank']['Count'])))
            self.statsTable.setItem(row, 11, QTableWidgetItem(str(data['Killed']['Car']['Count'])))
            self.statsTable.setItem(row, 12, QTableWidgetItem(str(data['Killed']['Infantry']['Count'])))
            self.statsTable.setItem(row, 13, QTableWidgetItem(str(data['FriendlyFire']['Count'])))
            self.statsTable.setItem(row, 14, QTableWidgetItem(str(data['Hit']['Count'])))
            self.statsTable.setItem(row, 15, QTableWidgetItem(str(data['Destroyed']['Count'])))

            # Set background color for even rows
            if row % 2 == 0:
                for col in range(16):
                    self.statsTable.item(row, col).setBackground(QColor(236, 236, 236))

        self.statsTable.resizeColumnsToContents()
        self.statsTable.setSortingEnabled(True)

    def displayEvents(self):
        self.eventsTable.clear()
        self.eventsTable.setColumnCount(3)
        self.eventsTable.setHorizontalHeaderLabels([self.language.L("time"), self.language.L("type"), self.language.L("action")])
        self.eventsTable.setRowCount(len(self.events))

        for row, event in enumerate(self.events):
            time_item = QTableWidgetItem(self.displayTime(self.startTime + event['Time']))
            time_item.setData(Qt.UserRole, event['Time'])  # Store original time for sorting
            self.eventsTable.setItem(row, 0, time_item)

            type_item = QTableWidgetItem(event['PrimaryObject'].get('Type', 'Unknown'))
            self.eventsTable.setItem(row, 1, type_item)

            action_text = self.format_event_action(event)
            action_item = QTableWidgetItem(action_text)
            self.eventsTable.setItem(row, 2, action_item)

            # Set row color based on event type
            row_color = self.get_row_color(event)
            for col in range(3):
                self.eventsTable.item(row, col).setBackground(row_color)

        self.eventsTable.resizeColumnsToContents()
        self.eventsTable.setSortingEnabled(True)
        # Sort by time initially
        self.eventsTable.sortItems(0, Qt.AscendingOrder)

    def get_row_color(self, event):
        if event['Action'] == 'HasBeenDestroyed':
            return QColor(211, 211, 211)  # Light gray
        elif event['Action'] == 'HasBeenHitBy':
            if (event['PrimaryObject'].get('Coalition') == event['SecondaryObject'].get('Coalition') and
                event['PrimaryObject'].get('Coalition') is not None):
                return QColor(255, 215, 181)  # Light orange (for friendly fire)
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

    def format_event_action(self, event):
        action_text = f"{event['PrimaryObject'].get('Name', 'Unknown')} ({event['PrimaryObject'].get('Pilot', 'Unknown')}) {self.language.L(event['Action'])}"
        
        if event['Action'] == 'HasLanded' or event['Action'] == 'HasTakenOff':
            if event['Airport']:
                action_text += f" {event['Airport'].get('Name', 'Unknown Airport')}"
            elif event['SecondaryObject'] and event['SecondaryObject'].get('Type') == 'Carrier':
                action_text += f" {event['SecondaryObject'].get('Name', 'Unknown Carrier')}"
        elif event['Action'] in ['HasFired', 'HasBeenHitBy']:
            if event['SecondaryObject']:
                action_text += f" {event['SecondaryObject'].get('Name', 'Unknown')}"
            if event['Action'] == 'HasBeenHitBy' and event['ParentObject']:
                action_text += f" [{event['ParentObject'].get('Name', 'Unknown')} ({event['ParentObject'].get('Pilot', 'Unknown')})]"
        elif event['Action'] == 'HasBeenDestroyed':
            if event['SecondaryObject'] and 'Pilot' in event['SecondaryObject']:
                action_text += f" by {event['SecondaryObject'].get('Pilot', 'Unknown')}"
        
        return action_text

def main():
    app = QApplication(sys.argv)
    ex = TacviewApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
