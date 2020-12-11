
/**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 * 
 * For more information visit:
 * https://www.amcharts.com/
 * 
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

export function footprintPlot(from, to) {
// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chartMax 
var data

var chartMin = 0;
if (to > 20000) {
  chartMax = to * 1.02
  data = {
    score: from,
    gradingData: [
      {
        title: "Low",
        color: "green",
        lowScore: 0,
        highScore: 2000
      },
      {
        title: "Med",
        color: "yellow",
        lowScore: 2000,
        highScore: 7000
      },
      {
        title: "High",
        color: "red",
        lowScore: 7000,
        highScore: 20000
      },
      {
        title: "Extreme",
        color: "#c1003a",
        lowScore: 20000,
        highScore: chartMax
      },
    ]
  };

} else {
  chartMax = 20000;
  data = {
    score: from,
    gradingData: [
      {
        title: "Low",
        color: "green",
        lowScore: 0,
        highScore: 2000
      },
      {
        title: "Med",
        color: "yellow",
        lowScore: 2000,
        highScore: 7000
      },
      {
        title: "High",
        color: "red",
        lowScore: 7000,
        highScore: 20000
      },
    ]
  };

}

/**
Grading Lookup
 */
function lookUpGrade(lookupScore, grades) {
  // Only change code below this line
  for (var i = 0; i < grades.length; i++) {
    if (
      grades[i].lowScore < lookupScore &&
      grades[i].highScore >= lookupScore
    ) {
      return grades[i];
    }
  }
  return null;
}

// create chart
var chart = am4core.create("chartdiv", am4charts.GaugeChart);
chart.hiddenState.properties.opacity = 0;
chart.fontSize = 11;
chart.innerRadius = am4core.percent(60);
chart.resizable = true;

/**
 * Normal axis -  ticks
 */

var axis = chart.xAxes.push(new am4charts.ValueAxis());
axis.min = chartMin;
axis.max = chartMax;
axis.hide()


/**
 * Axis for ranges - block ranges
 */

var axis2 = chart.xAxes.push(new am4charts.ValueAxis());
axis2.min = chartMin;
axis2.max = chartMax;
axis2.strictMinMax = true;
axis2.renderer.labels.template.disabled = true;
axis2.renderer.ticks.template.disabled = true;
axis2.renderer.grid.template.disabled = true;
axis2.renderer.grid.template.opacity = 0.5;
axis2.renderer.labels.template.bent = true;
axis2.renderer.labels.template.fill = am4core.color("#000");
axis2.renderer.labels.template.fontWeight = "bold";
axis2.renderer.labels.template.fillOpacity = 0.7;

/**
Ranges
*/

for (let grading of data.gradingData) {
  var range = axis2.axisRanges.create();
  range.axisFill.fill = am4core.color(grading.color);
  range.axisFill.fillOpacity = 0.8;
  range.axisFill.zIndex = -1;
  range.value = grading.lowScore > chartMin ? grading.lowScore : chartMin;
  range.endValue = grading.highScore < chartMax ? grading.highScore : chartMax;
  range.grid.strokeOpacity = 0;
  range.stroke = am4core.color(grading.color).lighten(-0.1);
  range.label.inside = true;
  range.label.text = grading.title.toUpperCase();
  range.label.inside = true;
  range.label.location = 0.5;
  range.label.inside = true;
  range.label.radius = am4core.percent(20);
  range.label.paddingBottom = -5; // ~half font size
  range.label.fontSize = "1.2em";
}

var matchingGrade = lookUpGrade(data.score, data.gradingData);

/**
 * Label 1 - value
 */

var label = chart.radarContainer.createChild(am4core.Label);
label.isMeasured = false;
label.fontSize = "4em";
label.x = am4core.percent(50);
label.paddingBottom = 15;
label.horizontalCenter = "middle";
label.verticalCenter = "bottom";
//label.dataItem = data;
label.text = data.score.toFixed(1);
//label.text = "{score}";
label.fill = am4core.color(matchingGrade.color);

/**
 * Label 2 - title
 */

var label2 = chart.radarContainer.createChild(am4core.Label);
label2.isMeasured = false;
label2.fontSize = "2em";
label2.horizontalCenter = "middle";
label2.verticalCenter = "bottom";
label2.text = matchingGrade.title.toUpperCase();
label2.fill = am4core.color(matchingGrade.color);

/**
 * Hand
 */

var hand = chart.hands.push(new am4charts.ClockHand());
hand.axis = axis2;
hand.innerRadius = am4core.percent(55);
hand.startWidth = 8;
hand.pin.disabled = true;
hand.value = data.score;
hand.fill = am4core.color("#444");
hand.stroke = am4core.color("#000");

hand.events.on("positionchanged", function(){
  label.text = axis2.positionToValue(hand.currentPosition).toFixed(1);
  var value2 = axis.positionToValue(hand.currentPosition);
  var matchingGrade = lookUpGrade(axis.positionToValue(hand.currentPosition), data.gradingData);
  label2.text = matchingGrade.title.toUpperCase();
  label2.fill = am4core.color(matchingGrade.color);
  label2.stroke = am4core.color(matchingGrade.color);  
  label.fill = am4core.color(matchingGrade.color);
})

setInterval(function() {
    var value = to;
    hand.showValue(value, 1000, am4core.ease.cubicOut);
}, 1000);

}