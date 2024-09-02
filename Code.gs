const SPREADSHEET_ID = '1Z7EUD5tTSxRpiheonQqcAe2Tflnny4bnXRpkkyinums'; // Replace with your spreadsheet ID

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData(missionNumber) {
  var spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet;
  
  if (missionNumber === 'Deployment Overall' || missionNumber === 'Overall') {
    sheet = spreadsheet.getSheetByName('Overall');
  } else {
    sheet = spreadsheet.getSheetByName('Mission ' + missionNumber);
  }
  
  if (sheet) {
    var data = sheet.getDataRange().getValues();
    
    var missionInfo = {
      missionName: missionNumber === 'Deployment Overall' ? "Deployment Overall Statistics" :
                   missionNumber === 'Overall' ? "Overall Statistics" : "Mission " + missionNumber,
      missionTime: "N/A",
      missionDuration: "N/A"
    };
    
    var pilotStats = [];
    for (var i = 1; i < data.length; i++) {
      pilotStats.push({
        pilotName: data[i][0],
        aircraft: data[i][1],
        firedArmament: parseInt(data[i][2]),
        killedAircraft: parseInt(data[i][3]),
        killedHelicopter: parseInt(data[i][4]),
        killedShip: parseInt(data[i][5]),
        killedSAM: parseInt(data[i][6]),
        killedTank: parseInt(data[i][7]),
        killedCar: parseInt(data[i][8]),
        killedInfantry: parseInt(data[i][9]),
        teamKills: parseInt(data[i][10]),
        hits: parseInt(data[i][11]),
        destroyed: parseInt(data[i][12])
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
  var missions = ['Deployment Overall', 'Overall'];
  
  for (var i = 0; i < sheets.length; i++) {
    var sheetName = sheets[i].getName();
    if (sheetName.startsWith('Mission ')) {
      var missionNumber = parseInt(sheetName.replace('Mission ', ''));
      missions.push(missionNumber);
    }
  }
  
  return missions;
}
