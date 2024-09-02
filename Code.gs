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
      missionName: "Mission " + missionNumber,
      missionTime: "N/A",
      missionDuration: "N/A"
    };
    
    var pilotStats = [];
    for (var i = 1; i < csvData.length; i++) {
      pilotStats.push({
        pilotName: csvData[i][0],
        firedArmament: parseInt(csvData[i][1]),
        killedAircraft: parseInt(csvData[i][2]),
        killedHelicopter: parseInt(csvData[i][3]),
        killedShip: parseInt(csvData[i][4]),
        killedSAM: parseInt(csvData[i][5]),
        killedTank: parseInt(csvData[i][6]),
        killedCar: parseInt(csvData[i][7]),
        teamKills: parseInt(csvData[i][8]),
        hits: parseInt(csvData[i][9]),
        destroyed: parseInt(csvData[i][10])
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
  var folder = DriveApp.getFolderById('YOUR_FOLDER_ID'); // Replace with your folder ID
  var files = folder.getFilesByName('mission*.csv');
  var missions = [];
  
  while (files.hasNext()) {
    var fileName = files.next().getName();
    var missionNumber = parseInt(fileName.replace('mission', '').replace('.csv', ''));
    missions.push(missionNumber);
  }
  
  return missions.sort((a, b) => a - b);
}
