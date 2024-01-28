function fetchTrendsData() {
    var keyword = document.getElementById('keywordInput').value;
    if (keyword) {
        fetch('http://127.0.0.1:5000/get_trends?keyword=' + encodeURIComponent(keyword))
            .then(response => response.json())
            .then(data => {
                console.log("Received data:", data); // For debugging
                updateChart(data, keyword);
            })
            .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter a keyword');
    }
}

var ctx = document.getElementById('trendsChart').getContext('2d');
var trendsChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Trend Over Time',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: true,
        maintainAspectRatio: false
    }
});

function updateChart(data, keyword) {
    trendsChart.data.labels = data.map(d => d.date.substring(0, 10)); // Extracting just the date part
    trendsChart.data.datasets[0].data = data.map(d => d[keyword]);
    trendsChart.data.datasets[0].label = 'Trend for ' + keyword; // Update the chart label
    trendsChart.update();
}