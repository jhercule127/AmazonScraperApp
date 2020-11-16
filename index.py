from flask import Flask, render_template, request, flash
from scrape import Scraper
import json
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scanProducts', methods=['POST'])
def scan():
    results = {}
    if request.method == 'POST':
        
        response = request.data
        obj = json.loads(response)

        budget = float(obj['budget'])
        del obj['budget']
        scraper = Scraper()
        scraper.set_limit(budget)

        for key,value in obj.items():
            result = scraper.get_purchase_outcome(value)
            if 'Oops sorry' not in result:
                results[key] =result
                product_image = scraper.get_product_image(value)
            else:
                results[key] =result
                break

        scraper.quit_driver()
        return json.dumps(results)

@app.route('/overallResults',methods=['GET'])
def overall():
    pass
   

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 
