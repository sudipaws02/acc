from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/column-map', methods=['GET', 'POST'])
def column_map():
    return render_template('column-map.html')

@app.route('/filter-fields', methods=['GET', 'POST'])
def filter_fields():
    return render_template('filter_fields.html')

@app.route('/run-specs', methods=['GET', 'POST'])
def run_specs():
    return render_template('run-specs.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    return render_template('review.html', billing_type="EA", filename="billing.csv",
                           column_mappings={"ProductId": "productId", "MeterId": "meterId"},
                           filter_fields=["productId", "location", "priceType"],
                           threads=4, retries=2)

if __name__ == '__main__':
    app.run(debug=True)
