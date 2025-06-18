from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Entry point: index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Dashboard page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

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

# Sidebar routes
@app.route('/executions')
def executions():
    return render_template('executions.html')
    # return "<h2>Executions Page - Under Construction</h2>"

@app.route('/default-config')
def default_config():
    return "<h2>Default Configuration Page - Under Construction</h2>"

@app.route('/generate-config')
def generate_config():
    return "<h2>Generate Config YAML Page - Under Construction</h2>"

if __name__ == '__main__':
    app.run(debug=True)
