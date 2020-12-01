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



function createCard(name,product){
    image = product[1];
    url = product[2];
    review_score = product[3];

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
    short_text.innerText = "You are able to purchase this item. Product score is " + review_score.toString();

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
    let budget = document.querySelector("#budget").value
    let arrayproducts = document.querySelector("#products").value.split('\n');


    let data = { "budget": budget };

    arrayproducts.forEach(function (item, index) {
        data['url' + index.toString()] = item;
    });

    let sendData = JSON.stringify(data);
    document.querySelector("#budget").value = "";
    document.querySelector("#products").value = "";
    ajaxPostRequest("/scanProducts", sendData, postQuickResults);
}



// WORK ON THIS PART TO FILL RESULTS AFTER RUNNING THE SCRAPER
function postQuickResults(jsonData) {

    
    let response = JSON.parse(jsonData);
    if (response['resp'] == 'error'){
        document.querySelector("#response").innerHTML = '<div class="alert alert-danger" role="alert"><strong>Unsuccessful</strong> Try Again!</div>';
        reset_app()
        setTimeout(() =>{ document.querySelector("#response").innerHTML =''; },4000)
    }

    else{
        delete response['resp'];
        let result = "";
        for (var key in response) {
            if (response.hasOwnProperty(key)) {
                result += response[key];
            }
        }
        document.querySelector("#response").innerHTML = '<div class="alert alert-success alert-dismissible fade show" role="alert">' + 
        '<strong>Successful!</strong>, see your results below. Extract them to a CSV file as an option.' +
        '<button type="button" class="close" data-dismiss="alert" aria-label="Close"> <span aria-hidden="true">&times;</span></button> </div> ';

        document.querySelector("#results").innerHTML = result;
        document.querySelector('#csv_button').style.visibility = 'visible';
        //setTimeout(() =>{ document.querySelector("#response").innerHTML =''; },4000)
    

        ajaxGetRequest('/overallResult',postOverallResults);
        ajaxGetRequest('/getProductsInfo',postExtractProducts);
    }
}



function postOverallResults(jsonData) {
   
    let response = JSON.parse(jsonData);
    let final_budget = response['final_budget'];
    document.querySelector('#overall_budget').innerHTML = "<h4>After determining the available product(s) you can buy, you're left with $" + final_budget.toString() + "</h4>";
    document.querySelector('#overall_list').style.visibility = 'visible';

}


function postExtractProducts(jsonData) {
    let response = JSON.parse(jsonData);

    for (var key in response) {
        if (response.hasOwnProperty(key)) {
            resp_array = response[key];
            card = createCard(key,resp_array);
            document.querySelector('.card-columns').appendChild(card);
        }
    }
    document.querySelector('#reset_app').disabled = false;
   
}


function reset_app() {
    ajaxGetRequest('/reset_app',function (jsonData) {
        let response = JSON.parse(jsonData);
        let outcome = response['outcome'];
        if (outcome){
            /* Remove Quick Results */
            document.querySelector('#results').innerHTML = '';
            document.querySelector('#csv_button').style.visibility = 'hidden';
            }

            /* Remove Overall Results and Cards  */
            document.querySelector('#overall_budget').innerHTML = '';
            document.querySelector('#overall_list').style.visibility = 'hidden';
            document.querySelector('.card-columns').innerHTML = '';

            /* Put disable attribute on reset button */
            document.querySelector('#reset_app').disabled = true
            
        }
    )

}


window.addEventListener('load',function () {
    const form = document.querySelector('#submit');
    form.addEventListener('submit',function (event) {
        event.preventDefault();
        getResults();
    });
});

