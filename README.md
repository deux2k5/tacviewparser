# Tacview Parser

This application is a GUI tool for parsing and analyzing Tacview ACMI files. It provides a user-friendly interface to view mission information, pilot statistics, and event details from Tacview Flight Logs.

## Features

1. **Mission Information**: Displays general information about the mission, including source, recorder, recording time, author, mission name, category, time, and duration.

2. **Pilot Statistics**: Shows detailed statistics for each pilot, including:
   - Aircraft flown
   - Number of armaments fired
   - Kills (aircraft, helicopters, ships, SAM/AAA, tanks, cars, infantry)
   - Team kills
   - Times hit
   - Times destroyed

3. **Event Log**: Provides a chronological list of events that occurred during the mission, including:
   - Take-offs and landings
   - Weapon firings
   - Hits and destructions

4. **Filtering and Sorting**: Allows users to filter and sort data in both the statistics and events views.

5. **CSV Export**: Enables exporting of pilot statistics to a CSV file for further analysis.

## Files

- `tacview_app.py`: The main application file containing the GUI and parsing logic.
- `build_exe.py`: Script to build the executable using PyInstaller.
- `requirements.txt`: List of Python dependencies required for the project.

## How to Use

1. Run the application by executing `tacview_app.py`.
2. Use the "Open XML File" button to load a Tacview ACMI file (XML format).
3. Navigate through the tabs to view different aspects of the mission data.
4. Use the search and filter options to find specific information.
5. Export statistics to CSV using the "Export to CSV" button.

## Building the Executable

To create a standalone executable:

1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Run the build script: `python build_exe.py`
3. The executable will be created in the `dist` directory.

## Dependencies

- PyQt5: For the graphical user interface
- PyInstaller: For creating the standalone executable

## Note

This application is designed to work with Tacview ACMI files in XML format. Ensure your Tacview Flight Logs are exported to XML before attempting to parse them with this tool.

## Google Sheets Integration

The Tacview Parser application includes functionality to integrate with Google Sheets for web-based viewing of mission data. This integration consists of two main components:

1. **index.html**: This file contains the HTML and JavaScript code for the web interface. It provides a user-friendly way to view mission data stored in Google Sheets, including:
   - A dropdown to select specific missions or view overall statistics
   - A table displaying pilot statistics
   - Filtering options for aircraft types
   - A deployment stats view for overall mission performance

2. **Code.gs**: This Google Apps Script file contains server-side functions that interact with the Google Sheets document storing the mission data. It includes functions to:
   - Retrieve data for specific missions or overall statistics
   - Get a list of available missions
   - Fetch deployment stats

### How it works with the exported CSV

1. The Python-based Tacview Parser application exports mission data to a CSV file.
2. This CSV file is then manually imported into a Google Sheets document.
3. The Google Sheets document is structured with separate sheets for each mission (named "Mission X") and an "Overall" sheet for cumulative statistics.
4. The Code.gs script reads data from these sheets when requested by the web interface.
5. The index.html file provides a web-based interface to view and interact with this data, making API calls to the Google Apps Script functions.

To use this integration:
1. Export mission data from the Tacview Parser application to CSV.
2. Import the CSV data into a Google Sheets document, maintaining the expected structure.
3. Deploy the Code.gs script as a Google Apps Script project, updating the SPREADSHEET_ID constant with your Google Sheets document ID.
4. Host the index.html file on a web server or use Google Apps Script to serve it.

This integration allows for easy sharing and viewing of mission data through a web interface, complementing the desktop-based Tacview Parser application.
