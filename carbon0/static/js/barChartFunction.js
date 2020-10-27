// make bar chart
export function barChart(plotLabels, plotData) {
  let ctx = document.getElementById("barChart").getContext("2d");
  let barChart = new Chart(ctx, {
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
        xAxes: [
          {
            display: true,
            ticks: {
              max: 20000,
              beginAtZero: true,
            },
          },
        ],
      },
      // turn the legend white
      legend: {
        display: true,
        labels: {
          fontColor: 'rgb(255, 255, 255)'
        }
      }
    },
  });
}
