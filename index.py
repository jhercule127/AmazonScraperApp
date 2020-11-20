from flask import Flask, render_template, request, flash
from scrape import Scraper
import json
app = Flask(__name__)
scraper = Scraper()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanProducts', methods=['POST'])
def scan():
    scraper.set_driver()
    results = {}
    if request.method == 'POST':
        
        response = request.data
        obj = json.loads(response)

        budget = float(obj['budget'])
        del obj['budget']
        scraper.set_limit(budget)

        for key,value in obj.items():
            result = scraper.get_purchase_outcome(value)
            if 'Oops sorry' not in result:
                results[key] =result
            else:
                results[key] =result
                break

        scraper.quit_driver()
        return json.dumps(results)

@app.route('/overallResult',methods=['GET'])
def overall():
    names = scraper.get_product_names()
    final_budget = scraper.get_limit()
    results = {'names':names,'final_budget':final_budget}
    return json.dumps(results)
   
@app.route('/getProductsInfo',methods=['GET'])
def get_info():
    info = scraper.get_products()
    if not bool(info):
        return
    else:
        return json.dumps(info)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
