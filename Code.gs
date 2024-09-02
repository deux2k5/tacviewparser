function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('Tacview Mission Data')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getData() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var data = sheet.getDataRange().getValues();
  
  var missionInfo = {
    missionName: data[1][1],
    missionTime: data[2][1],
    missionDuration: data[3][1]
  };
  
  var pilotStats = [];
  for (var i = 6; i < data.length; i++) {
    if (data[i][0] === '') break;
    pilotStats.push({
      pilotName: data[i][0],
      kills: parseInt(data[i][6]) + parseInt(data[i][7]) + parseInt(data[i][8]) + parseInt(data[i][9]) + parseInt(data[i][10]) + parseInt(data[i][11]),
      deaths: parseInt(data[i][15])
    });
  }
  
  var events = [];
  var eventStartRow = pilotStats.length + 8;
  for (var i = eventStartRow; i < data.length; i++) {
    if (data[i][0] === '') break;
    events.push({
      time: data[i][0],
      type: data[i][1],
      action: data[i][2]
    });
  }
  
  return {
    missionInfo: missionInfo,
    pilotStats: pilotStats,
    events: events
  };
}
