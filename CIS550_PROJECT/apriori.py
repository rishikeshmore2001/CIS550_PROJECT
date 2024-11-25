import csv
from itertools import combinations, chain
from collections import defaultdict

def find_frequent_1_itemsets(transactions, min_support):
    """Finds the frequent 1-itemsets in the dataset."""
    item_count = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_count[frozenset([item])] += 1
    return {itemset for itemset, count in item_count.items() if count >= min_support}

def apriori_gen(frequent_itemsets, k):
    """Generates candidate k-itemsets from the previous (k-1)-itemsets."""
    candidates = set()
    itemsets = list(frequent_itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            l1, l2 = list(itemsets[i]), list(itemsets[j])
            # Join step: if the first k-2 items are equal, combine to form a k-itemset
            if l1[:k-2] == l2[:k-2] and l1[k-2] < l2[k-2]:
                candidate = frozenset(itemsets[i] | itemsets[j])
                if not has_infrequent_subset(candidate, frequent_itemsets):
                    candidates.add(candidate)
    return candidates

def has_infrequent_subset(candidate, frequent_itemsets):
    """Checks if any subset of the candidate is not frequent."""
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in frequent_itemsets:
            return True
    return False

def apriori(transactions, min_support):
    """Runs the Apriori algorithm and returns the frequent itemsets."""
    L = []
    k = 1
    Lk = find_frequent_1_itemsets(transactions, min_support)
    while Lk:
        L.append(Lk)
        Ck = apriori_gen(Lk, k + 1)
        item_count = defaultdict(int)
        for transaction in transactions:
            # Count candidates that appear in each transaction
            Ct = {candidate for candidate in Ck if candidate.issubset(transaction)}
            for candidate in Ct:
                item_count[candidate] += 1
        # Filter itemsets meeting min support
        Lk = {itemset for itemset, count in item_count.items() if count >= min_support}
        k += 1
    return set(chain.from_iterable(L))

def load_transactions(file):
    """Loads transactions from a FileStorage object."""
    transactions = []
    # Read the file content directly from the FileStorage object
    file_content = file.read().decode('utf-8').splitlines()
    reader = csv.reader(file_content)
    for row in reader:
        transactions.append(set(map(int, row)))  # Convert each row into a set of integers
    return transactions

def get_max_frequentItems(frequent_itemsets):
    """Finds the maximal frequent itemsets."""
    maximal_items = []
    for items in sorted(frequent_itemsets, key=len, reverse=True):
        if not any(set(items).issubset(set(max_item)) for max_item in maximal_items):
            maximal_items.append(items)
    return maximal_items


def format_output(frequent_itemsets, input_file, min_support):
    """Formats output according to the specified format."""
    print(f"Input file: {input_file}")
    print(f"Minimal support: {min_support}")
    formatted_output = "{{" + "}{".join(",".join(map(str, sorted(itemset))) for itemset in sorted(frequent_itemsets, key=lambda x: (len(x), x))) + "}}"
    print(formatted_output)
    print(f"End - total items: {len(frequent_itemsets)}")

# Fix the typo: change _name_ to __name__
if __name__ == '__main__':
    # Parsing command line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file', required=True, help="Input CSV file containing transactions")
    parser.add_argument('-m', '--min_support', type=int, required=True, help="Minimum support count")
    args = parser.parse_args()

    # Load transactions from the input file
    transactions = load_transactions(args.input_file)
    min_support = args.min_support

    # Run Apriori algorithm
    frequent_itemsets = apriori(transactions, min_support)

    # Format and print output
    format_output(frequent_itemsets, args.input_file, min_support)


