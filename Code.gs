const SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'; // Replace with your spreadsheet ID

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData(missionNumber) {
  var spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = spreadsheet.getSheetByName('Mission ' + missionNumber);
  
  if (sheet) {
    var data = sheet.getDataRange().getValues();
    
    var missionInfo = {
      missionName: "Mission " + missionNumber,
      missionTime: "N/A",
      missionDuration: "N/A"
    };
    
    var pilotStats = [];
    for (var i = 1; i < data.length; i++) {
      pilotStats.push({
        pilotName: data[i][0],
        firedArmament: parseInt(data[i][1]),
        killedAircraft: parseInt(data[i][2]),
        killedHelicopter: parseInt(data[i][3]),
        killedShip: parseInt(data[i][4]),
        killedSAM: parseInt(data[i][5]),
        killedTank: parseInt(data[i][6]),
        killedCar: parseInt(data[i][7]),
        teamKills: parseInt(data[i][8]),
        hits: parseInt(data[i][9]),
        destroyed: parseInt(data[i][10])
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
