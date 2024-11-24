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
    maximal_frequent_itemsets = get_maximal_frequent_itemsets(frequent_itemsets)
    
    # Calculate runtime
    runtime = time.time() - start_time
    
    # Prepare frequent itemsets in the desired format
    formatted_itemsets = [f"{{{','.join(map(str, itemset))}}}" for itemset in frequent_itemsets]
    
    return render_template(
        'result.html',
        input_file=input_filename,
        min_support=min_support,
        frequent_itemsets=formatted_itemsets,
        total_items=len(frequent_itemsets),
        runtime=round(runtime, 6)
    )
