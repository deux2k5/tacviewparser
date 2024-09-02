const SPREADSHEET_ID = '1Z7EUD5tTSxRpiheonQqcAe2Tflnny4bnXRpkkyinums'; // Replace with your spreadsheet ID

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData(missionNumber) {
  var folder = DriveApp.getFolderById('YOUR_FOLDER_ID'); // Replace with the ID of the folder containing your CSV files
  var files = folder.getFilesByName('mission_' + missionNumber + '.csv');
  
  if (files.hasNext()) {
    var file = files.next();
    var csvData = Utilities.parseCsv(file.getBlob().getDataAsString());
    
    var missionInfo = {
      missionName: "Mission " + missionNumber,
      missionTime: "N/A",
      missionDuration: "N/A"
    };
    
    var pilotStats = [];
    for (var i = 1; i < csvData.length; i++) {
      pilotStats.push({
        pilotName: csvData[i][0],
        aircraft: csvData[i][1],
        firedArmament: parseInt(csvData[i][2]),
        killedAircraft: parseInt(csvData[i][3]),
        killedHelicopter: parseInt(csvData[i][4]),
        killedShip: parseInt(csvData[i][5]),
        killedSAM: parseInt(csvData[i][6]),
        killedTank: parseInt(csvData[i][7]),
        killedCar: parseInt(csvData[i][8]),
        killedInfantry: parseInt(csvData[i][9]),
        teamKills: parseInt(csvData[i][10]),
        hits: parseInt(csvData[i][11]),
        destroyed: parseInt(csvData[i][12])
      });
    }
    
    return {
      missionInfo: missionInfo,
      pilotStats: pilotStats
    };
  }
  
  return null;
}

function getAvailableMissions() {
  var spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheets = spreadsheet.getSheets();
  var missions = [];
  
  for (var i = 0; i < sheets.length; i++) {
    var sheetName = sheets[i].getName();
    if (sheetName.startsWith('Mission ')) {
      var missionNumber = parseInt(sheetName.replace('Mission ', ''));
      missions.push(missionNumber);
    }
  }
  
  return missions.sort((a, b) => a - b);
}
