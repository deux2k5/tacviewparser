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
