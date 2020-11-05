// make bar chart
export function barChart(plotLabels, plotData) {
  let ctx = document.getElementById("barChart").getContext("2d");

  // configuration for gauge chart
  const configGaugeChart = {
    type: 'gauge',
    data: {
      //labels: ['Success', 'Warning', 'Warning', 'Error'],
      datasets: [{
        data: [1000, 5000, 10000, 20000],
        value: plotData,
        backgroundColor: ['green', 'yellow', 'orange', 'red'],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      // title: {
      //   display: true,
      //   text: 'metric tons CO2'
      // },
      layout: {
        padding: {
          bottom: 30
        }
      },
      needle: {
        // Needle circle radius as the percentage of the chart area width
        radiusPercentage: 2,
        // Needle width as the percentage of the chart area width
        widthPercentage: 3.2,
        // Needle length as the percentage of the interval between inner radius (0%) and outer radius (100%) of the arc
        lengthPercentage: 80,
        // The color of the needle
        color: 'rgba(0, 0, 0, 1)'
      },
      valueLabel: {
        formatter: Math.round,
        display: true,
      },
      plugins: {
        datalabels: {
          display: true,
          formatter: function (value, context) {
            return '< ' + Math.round(value);
          },
          color: function (context) {
            return context.dataset.backgroundColor;
          },
          //color: 'rgba(255, 255, 255, 1.0)',
          backgroundColor: 'rgba(0, 0, 0, 1.0)',
          borderWidth: 0,
          borderRadius: 5,
          font: {
            weight: 'bold'
          }
        }
      }
    }
  };

// configuration for horizontal bar chart
  const configBarChart = {
    type: "horizontalBar",
    data: {
      datasets: [
        {
          label: "metric tons CO2",
          data: plotData,
          // set options for the chart
          backgroundColor: ["rgba(255, 99, 132, 0.2)"],
          borderColor: ["rgba(255, 99, 132, 1)"],
          borderWidth: 1,
        },
      ],
      labels: plotLabels,
    },
    options: {
      responsive: true,
      scales: {
        xAxes: [{
          display: true,
          ticks: {
            max: 20000,
            beginAtZero: true,
            // turn the tick markers white
            fontColor: 'rgb(255, 255, 255)'
          },
          gridLines: {
            color: "white"
          }
        }],
        yAxes: [{
          ticks: {
            // color the plot label white
            fontColor: "white",
          }
        }],
      },
      // turn the legend white
      legend: {
        display: true,
        labels: {
          fontColor: 'rgb(255, 255, 255)',
        }
      },
    },
  };

// to enable either gauge or horizontal bar chart; either or and not both!
new Chart(ctx, configGaugeChart)
// new Chart(ctx, configBarChart)

}
