from flask import Flask, render_template, request, make_response
from scrape import Scraper
import json
app = Flask(__name__)
scraper = Scraper()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanProducts', methods=['POST'])
def crawl():

    results = {}
    if request.method == 'POST':
        
        response = request.data
        obj = json.loads(response)

        budget = float(obj['budget'])
        del obj['budget']
        scraper.set_limit(budget)

        validation = all([scraper.is_valid(value) for key,value in obj.items()])
        if validation:
            scraper.set_driver()
            for key,value in obj.items():
                result = scraper.get_purchase_outcome(value)
                if 'Oops sorry' not in result:
                    results[key] =result
                else:
                    results[key] =result
                    break
        else:
            return json.dumps({'resp':'error'})

        results['resp'] = 'success'
        scraper.quit_driver()
        return json.dumps(results)

@app.route('/overallResult',methods=['GET'])
def overall():
    final_budget = scraper.get_limit()
    results = {'final_budget':final_budget}
    return json.dumps(results)
   
@app.route('/getProductsInfo',methods=['GET'])
def get_info():
    info = scraper.get_products()
    if not bool(info):
        return 
    else:
        return json.dumps(info)


@app.route('/getCSVFile',methods=['GET'])
def csv():
    file = scraper.extract_to_CSV()
    output = make_response(file.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=results.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/reset_app',methods= ['GET'])
def reset_app():
    outcome = scraper.reset()
    return {'outcome':outcome}


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
