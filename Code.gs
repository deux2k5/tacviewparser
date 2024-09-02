const SPREADSHEET_ID = '1Z7EUD5tTSxRpiheonQqcAe2Tflnny4bnXRpkkyinums'; // Replace with your spreadsheet ID

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData(missionNumber) {
  var spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet;
  
  if (missionNumber === 'Overall') {
    sheet = spreadsheet.getSheetByName('Overall');
  } else {
    sheet = spreadsheet.getSheetByName('Mission ' + missionNumber);
  }
  
  if (sheet) {
    var data = sheet.getDataRange().getValues();
    
    var missionInfo = {
      missionName: missionNumber === 'Overall' ? "Overall Statistics" : "Mission " + missionNumber,
      missionTime: "N/A",
      missionDuration: "N/A"
    };
    
    var pilotStats = [];
    for (var i = 1; i < data.length; i++) {
      var row = data[i];
      if (row[0] !== "") {  // Skip empty rows
        pilotStats.push({
          pilotName: row[0],
          aircraft: row[1] || "0",
          firedArmament: parseInt(row[2]) || 0,
          killedAircraft: parseInt(row[3]) || 0,
          killedHelicopter: parseInt(row[4]) || 0,
          killedShip: parseInt(row[5]) || 0,
          killedSAM: parseInt(row[6]) || 0,
          killedTank: parseInt(row[7]) || 0,
          killedCar: parseInt(row[8]) || 0,
          killedInfantry: parseInt(row[9]) || 0,
          teamKills: parseInt(row[10]) || 0,
          hits: parseInt(row[11]) || 0,
          destroyed: parseInt(row[12]) || 0
        });
      }
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
  var missions = ['Overall'];
  
  for (var i = 0; i < sheets.length; i++) {
    var sheetName = sheets[i].getName();
    if (sheetName.startsWith('Mission ')) {
      var missionNumber = parseInt(sheetName.replace('Mission ', ''));
      missions.push(missionNumber);
    }
  }
  
  return missions;
}
