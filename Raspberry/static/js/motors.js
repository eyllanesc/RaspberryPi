var ip = location.host;
document.getElementById("ip_link").src = "http://" + ip + ":8081";

// Load all posts on page load
function move(state) {
    $.ajax({
        url: "/api/motors/", // the endpoint
        type: "POST", // http method
        // handle a successful response
        success: function (data) {

        },
        data: {
            'status': state
        },
        // handle a non-successful response
        error: function (xhr, errmsg, err) {

        }
    });

};

function forward() {
    move('F');
};

function backward() {
    move('B');
};

function left() {
    move('L');
};

function right() {
    move('R');
};

function stop() {
    move('S');
};