from flask import Flask, render_template, request
from apriori import load_transactions, apriori
import time

app = Flask(__name__)

def get_max_frequentItems(frequent_itemsets):
    max = []
    for items in sorted(frequent_itemsets,key=len, reverse=true):
        if not any(set(items).issubset(set(max_items)) for max_items in max):
            max.append(items)
    return max
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_apriori():
    # Retrieve the uploaded file and minimum support value
    file = request.files['file']
    min_support = int(request.form['min_support'])
    input_filename = file.filename  # Capture input file name
    
    # Load transactions from the file
    transactions = load_transactions(file)
    
    # Measure start time
    start_time = time.time()
    
    # Run Apriori algorithm
    frequent_itemsets = apriori(transactions, min_support)
    
    # Calculate runtime
    runtime = time.time() - start_time
    maximal_items = get_max_frequentItems(frequent_itemsets)
    maximal_items.sort(key=lambda x:(len(x), x))
    
    # Format frequent itemsets to match output
    formatted_itemsets = [f"{{{','.join(map(str, sorted(itemset)))}}}" for itemset in maximal_items]
    result_string = "{" + "".join(formatted_itemsets) + "}"
    
    return render_template(
        'result.html',
        input_file=input_filename,
        min_support=min_support,
        frequent_itemsets=result_string,
        total_items=len(maximal_items),
        runtime=round(runtime, 6)
    )

# Add this block to ensure the app runs
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


# Add this block to ensure the app runs
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

