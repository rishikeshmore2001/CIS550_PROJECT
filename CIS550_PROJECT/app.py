from flask import Flask, render_template, request
from apriori import load_transactions, apriori, get_maximal_frequent_itemsets
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_apriori():
    # Retrieve the uploaded file and minimum support value
    file = request.files['file']
    min_support = int(request.form['min_support'])
    
    # Load transactions from the file
    transactions = load_transactions(file)
    
    # Measure start time
    start_time = time.time()
    
    # Run Apriori algorithm
    frequent_itemsets = apriori(transactions, min_support)
    maximal_frequent_itemsets = get_maximal_frequent_itemsets(frequent_itemsets)
    
    # Calculate runtime
    runtime = time.time() - start_time
    
    # Render results to the template
    return render_template(
        'result.html',
        frequent=frequent_itemsets,
        maximal=maximal_frequent_itemsets,
        runtime=runtime
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    # Specify the host and port
    app.run(host='0.0.0.0', port=5000, debug=True)

