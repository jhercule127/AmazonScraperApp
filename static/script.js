// path is URI we are sending request
// callback is function to execute once reply received
function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callback(this.response);
        }
    }
    request.open("GET", path);
    request.send();
}

function ajaxPostRequest(path, data, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}

// NEED TO UPDATE THIS
function getResults() {
    let budget = document.getElementById("budget").value
    let arrayproducts = document.getElementById("products").value.split('\n');


    let data = { "budget": budget };

    arrayproducts.forEach(function (item, index) {
        data['url' + index.toString()] = item;
    });

    let sendData = JSON.stringify(data);
    document.getElementById("budget").value = "";
    document.getElementById("products").value = "";
    ajaxPostRequest("/scanProducts", sendData, postQuickResults);
}

// WORK ON THIS PART TO FILL RESULTS AFTER RUNNING THE SCRAPER
function postQuickResults(jsonData) {
    try {
        let response = JSON.parse(jsonData);
        let result = "";

        for (var key in response) {
            if (response.hasOwnProperty(key)) {
                result += response[key];
            }
        }

        document.getElementById("results").innerHTML = result;
        document.getElementById("response").innerHTML = '<div class="alert alert-success" role="alert"><strong>Successful!</strong>, see your results below. Extract them to a CSV file as an option.</div>';
        setTimeout(() =>{ document.getElementById("response").remove(); },7000)
    } catch (e) {
        document.getElementById("response").innerHTML = '<div class="alert alert-warning" role="alert">Unsuccessful</div>';
    }

    //ajaxGetRequest('/overallResults',postOverallResults)
}

function postOverallResults(jsonData) {
    
}
