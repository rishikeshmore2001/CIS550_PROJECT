from flask import Flask, render_template, request
from apriori import load_transactions, apriori
import time

app = Flask(__name__)

def get_max_frequentItems(frequent_itemsets):
    """Finds the maximal frequent itemsets."""
    max_items = []
    for items in sorted(frequent_itemsets, key=len, reverse=True):
        if not any(set(items).issubset(set(max_item)) for max_item in max_items):
            max_items.append(items)
    return max_items

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

    # Find maximal frequent itemsets
    maximal_items = get_max_frequentItems(frequent_itemsets)

    # Sort maximal itemsets by length and lexicographical order
    maximal_items.sort(key=lambda x: (len(x), sorted(x)))

    # Format frequent itemsets to match the desired output format
    formatted_itemsets = [f"{{{','.join(map(str, sorted(itemset)))}}}" for itemset in maximal_items]
    result_string = "{" + "".join(formatted_itemsets) + "}"

    # Measure runtime
    runtime = time.time() - start_time

    return render_template(
        'result.html',
        input_file=input_filename,
        min_support=min_support,
        frequent_itemsets=result_string,
        total_items=len(maximal_items),
        runtime=round(runtime, 6)
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

