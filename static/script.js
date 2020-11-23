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

function createCard(name,image,url){
    let card = document.createElement('div');
    card.className = 'card';

    let cardbody = document.createElement('div');
    cardbody.className = 'card-body';

    let img = document.createElement('img');
    img.src = image;
    img.className = 'card-img-top';


    let title = document.createElement('h5');
    title.innerText = name;
    title.className = 'card-title';

    let short_text = document.createElement('p');
    short_text.className = 'card-text';
    short_text.innerText = "You are able to purchase this item. Feel free to explore other items.";

    let link = document.createElement('a');
    link.className = 'btn btn-primary';
    link.href = url;
    link.textContent = 'Go See Item';

    cardbody.append(title,short_text,link);
    card.appendChild(img);
    card.appendChild(cardbody);

    return card;
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
        document.getElementById("response").innerHTML = '<div class="alert alert-success" role="alert"><strong>Successful!</strong>, see your results below. Extract them to a CSV file as an option.</div>';
        document.getElementById("results").innerHTML = result;
        document.getElementById('csv_button').style.visibility = 'visible';
        setTimeout(() =>{ document.getElementById("response").remove(); },7000)
    } catch (e) {
        document.getElementById("response").innerHTML = '<div class="alert alert-warning" role="alert">Unsuccessful</div>';
    }

    ajaxGetRequest('/overallResult',postOverallResults);
    ajaxGetRequest('/getProductsInfo',postExtractProducts);
}

function postOverallResults(jsonData) {
    try {
        let response = JSON.parse(jsonData);
        let final_budget = response['final_budget'];
        document.getElementById('overall_budget').innerHTML = "<h4>After determining the available products you can buy, you're left with $" + final_budget.toString() + "</h4>";
        document.getElementById('overall_list').style.visibility = 'visible';
    } catch (error) {
        document.getElementById("response").innerHTML = '<div class="alert alert-warning" role="alert">Unsuccessful</div>';
    }
}

function postExtractProducts(jsonData) {
    let response = JSON.parse(jsonData);

    for (var key in response) {
        if (response.hasOwnProperty(key)) {
            resp_array = response[key];
            image = resp_array[1];
            url = resp_array[2];
            card = createCard(key,image,url);
            document.getElementById('card-container').appendChild(card);
        }


    }


}
