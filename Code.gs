function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getMissionData(missionNumber) {
  var folder = DriveApp.getFolderById('YOUR_FOLDER_ID'); // Replace with your folder ID
  var files = folder.getFilesByName('mission' + missionNumber + '.csv');
  
  if (files.hasNext()) {
    var file = files.next();
    var csvData = Utilities.parseCsv(file.getBlob().getDataAsString());
    
    var missionInfo = {
      missionName: csvData[1][1],
      missionTime: csvData[2][1],
      missionDuration: csvData[3][1]
    };
    
    var pilotStats = [];
    var i = 6;
    while (i < csvData.length && csvData[i][0] !== '') {
      pilotStats.push({
        pilotName: csvData[i][0],
        aircraft: csvData[i][1],
        group: csvData[i][2],
        takeoffs: parseInt(csvData[i][3]),
        landings: parseInt(csvData[i][4]),
        firedArmament: parseInt(csvData[i][5]),
        killedAircraft: parseInt(csvData[i][6]),
        killedHelicopter: parseInt(csvData[i][7]),
        killedShip: parseInt(csvData[i][8]),
        killedSAM: parseInt(csvData[i][9]),
        killedTank: parseInt(csvData[i][10]),
        killedCar: parseInt(csvData[i][11]),
        killedInfantry: parseInt(csvData[i][12]),
        teamKills: parseInt(csvData[i][13]),
        hits: parseInt(csvData[i][14]),
        destroyed: parseInt(csvData[i][15])
      });
      i++;
    }
    
    var events = [];
    i += 2; // Skip empty row and header
    while (i < csvData.length && csvData[i][0] !== '') {
      events.push({
        time: csvData[i][0],
        type: csvData[i][1],
        action: csvData[i][2]
      });
      i++;
    }
    
    return {
      missionInfo: missionInfo,
      pilotStats: pilotStats,
      events: events
    };
  } else {
    return null;
  }
}

function getAvailableMissions() {
  var folder = DriveApp.getFolderById('YOUR_FOLDER_ID'); // Replace with your folder ID
  var files = folder.getFilesByType(MimeType.CSV);
  var missions = [];
  
  while (files.hasNext()) {
    var file = files.next();
    var match = file.getName().match(/mission(\d+)\.csv/);
    if (match) {
      missions.push(parseInt(match[1]));
    }
  }
  
  return missions.sort((a, b) => a - b);
}
