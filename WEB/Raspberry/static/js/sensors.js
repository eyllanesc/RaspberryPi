$(document).ready(function () {
    var temperature = {
        x: [],
        y: [],
        fill: 'tonexty',
        type: 'scatter',
        name: 'Temperatura'
    };


    var humidity = {
        x: [],
        y: [],
        fill: 'tonexty',
        type: 'scatter',
        name: 'Humedad',
        yaxis: 'y2'
    };

    var layout = {
        title: 'Sensores',
        showlegend: true,
        legend: {
            x: 0,
            y: 1,
            traceorder: 'normal',
            font: {
                family: 'sans-serif',
                size: 12,
                color: '#000'
            },
            bgcolor: '#E2E2E2',
        },
        yaxis: {
            title: '°C',
            range: [0, 100]
        },
        yaxis2: {
            title: '%',
            side: 'right',
            overlaying: 'y',
            range: [0, 100]
        }
    };

    var data = [humidity, temperature];

    var updateInterval = 1000;
    // Load all posts on page load
    function GetData() {
        $.ajax({
            url: "/api/sensors/", // the endpoint
            type: "GET", // http method
            // handle a successful response
            success: function (data) {
            	results = data['results'];
                temperature['x'] = [];
                temperature['y'] = [];

                humidity['x'] = [];
                humidity['y'] = [];

                $.each(results, function (index, value) {
                    temperature['x'].push(new Date(value['date_created']));
                    temperature['y'].push(value['temperature']);

                    humidity['x'].push(new Date(value['date_created']));
                    humidity['y'].push(value['humidity']);
                });
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {

            }
        });

    };

    function update() {
        GetData();

        if (document.getElementById("myCheck").checked) {
            Plotly.newPlot('placeholder', data, layout);
            document.getElementById('lblLast').innerHTML = "Temperatura Actual: " +
                temperature['y'][0] + "<br>Humedad Actual: " + humidity['y'][0];
        }
        var interval = Number(document.getElementById("interval").value);
        if (!isNaN(interval)) {
            updateInterval = interval;
        }
        setTimeout(update, updateInterval);
    }

    update();

});