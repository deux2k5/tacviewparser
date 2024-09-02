function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData() {
  var spreadsheet = SpreadsheetApp.openById('1Z7EUD5tTSxRpiheonQqcAe2Tflnny4bnXRpkkyinums'); // Replace with your spreadsheet ID
  var missions = {};
  
  var sheets = spreadsheet.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var sheet = sheets[i];
    var sheetName = sheet.getName();
    
    if (sheetName.startsWith('mission')) {
      var missionNumber = sheetName.replace('mission', '');
      var data = sheet.getDataRange().getValues();
      
      var missionInfo = {
        missionName: data[1][1],
        missionTime: data[2][1],
        missionDuration: data[3][1]
      };
      
      var pilotStats = [];
      var j = 6;
      while (j < data.length && data[j][0] !== '') {
        pilotStats.push({
          pilotName: data[j][0],
          aircraft: data[j][1],
          group: data[j][2],
          takeoffs: parseInt(data[j][3]),
          landings: parseInt(data[j][4]),
          firedArmament: parseInt(data[j][5]),
          killedAircraft: parseInt(data[j][6]),
          killedHelicopter: parseInt(data[j][7]),
          killedShip: parseInt(data[j][8]),
          killedSAM: parseInt(data[j][9]),
          killedTank: parseInt(data[j][10]),
          killedCar: parseInt(data[j][11]),
          killedInfantry: parseInt(data[j][12]),
          teamKills: parseInt(data[j][13]),
          hits: parseInt(data[j][14]),
          destroyed: parseInt(data[j][15])
        });
        j++;
      }
      
      var events = [];
      j += 2; // Skip empty row and header
      while (j < data.length && data[j][0] !== '') {
        events.push({
          time: data[j][0],
          type: data[j][1],
          action: data[j][2]
        });
        j++;
      }
      
      missions[missionNumber] = {
        missionInfo: missionInfo,
        pilotStats: pilotStats,
        events: events
      };
    }
  }
  
  return missions;
}

function getAvailableMissions() {
  var spreadsheet = SpreadsheetApp.openById('YOUR_SPREADSHEET_ID'); // Replace with your spreadsheet ID
  var sheets = spreadsheet.getSheets();
  var missions = [];
  
  for (var i = 0; i < sheets.length; i++) {
    var sheetName = sheets[i].getName();
    if (sheetName.startsWith('mission')) {
      missions.push(parseInt(sheetName.replace('mission', '')));
    }
  }
  
  return missions.sort((a, b) => a - b);
}
