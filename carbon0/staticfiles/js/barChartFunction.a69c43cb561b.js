// make bar chart
export function carbonCalculator(plotLabels, plotData) {
    let ctx = document.getElementById('carbonCalculator').getContext('2d');
    let carbonCalculator = new Chart(ctx, {
        type: "horizontalBar",
        data: {
            datasets: [{
                label: 'metric tons CO2',
                data: plotData,
                // set options for the chart
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                ],
                borderWidth: 1
            }],
            labels: plotLabels
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}