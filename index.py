from flask import Flask, render_template, request, flash
from scrape import Scraper
import json
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# UPDATES NEEDED HERE
@app.route('/scanProducts', methods=['GET', 'POST'])
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
            result = scraper.get_outcome(value)
            results[key] =result
        return json.dumps(results)
    
   

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 