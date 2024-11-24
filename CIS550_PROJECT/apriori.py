import csv
from collections import defaultdict, Counter
from itertools import combinations

def load_transactions(file):
    """
    Loads transactions from a CSV file object.
    :param file: File object (already opened) containing transaction data.
    :return: List of sets, where each set is a transaction.
    """
    transactions = []
    # Decode the binary file into a text stream
    text_stream = file.read().decode('utf-8').splitlines()
    reader = csv.reader(text_stream)
    for row in reader:
        transactions.append(set(row))
    return transactions


def get_frequent_1_itemsets(transactions, min_support):
    """
    Identifies frequent 1-itemsets based on the minimum support threshold.
    :param transactions: List of transactions.
    :param min_support: Minimum support threshold.
    :return: Dictionary of itemsets with their respective counts.
    """
    item_counts = Counter()
    for transaction in transactions:
        for item in transaction:
            item_counts[frozenset([item])] += 1
    return {itemset: count for itemset, count in item_counts.items() if count >= min_support}

def apriori_gen(itemsets, k):
    """
    Generates candidate k-itemsets from the given frequent itemsets.
    :param itemsets: List of frequent itemsets from the previous iteration.
    :param k: Length of itemsets to generate.
    :return: Set of candidate k-itemsets.
    """
    candidates = set()
    itemsets = list(itemsets)
    for i in range(len(itemsets)):
        for j in range(i + 1, len(itemsets)):
            union_set = itemsets[i] | itemsets[j]
            if len(union_set) == k and not has_infrequent_subset(union_set, itemsets):
                candidates.add(union_set)
    return candidates

def has_infrequent_subset(candidate, frequent_itemsets):
    """
    Checks if a candidate has any infrequent subset.
    :param candidate: Candidate itemset.
    :param frequent_itemsets: Set of frequent itemsets.
    :return: True if an infrequent subset is found, False otherwise.
    """
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in frequent_itemsets:
            return True
    return False

def filter_candidates(transactions, candidates, min_support):
    """
    Filters candidate itemsets by checking their support in the transactions.
    :param transactions: List of transactions.
    :param candidates: Set of candidate itemsets.
    :param min_support: Minimum support threshold.
    :return: Dictionary of itemsets with their respective counts.
    """
    item_counts = defaultdict(int)
    for transaction in transactions:
        for candidate in candidates:
            if candidate.issubset(transaction):
                item_counts[candidate] += 1
    return {itemset: count for itemset, count in item_counts.items() if count >= min_support}

def apriori(transactions, min_support):
    """
    Implements the Apriori algorithm to find frequent itemsets.
    :param transactions: List of transactions.
    :param min_support: Minimum support threshold.
    :return: List of frequent itemsets.
    """
    frequent_itemsets = []
    current_itemsets = get_frequent_1_itemsets(transactions, min_support)
    k = 2
    while current_itemsets:
        frequent_itemsets.extend(current_itemsets.keys())
        candidates = apriori_gen(current_itemsets.keys(), k)
        current_itemsets = filter_candidates(transactions, candidates, min_support)
        k += 1
    return [set(itemset) for itemset in frequent_itemsets]

def get_maximal_frequent_itemsets(frequent_itemsets):
    """
    Identifies maximal frequent itemsets from the list of frequent itemsets.
    :param frequent_itemsets: List of frequent itemsets.
    :return: List of maximal frequent itemsets.
    """
    maximal = []
    for itemset in sorted(frequent_itemsets, key=len, reverse=True):
        if not any(set(itemset).issubset(set(max_itemset)) for max_itemset in maximal):
            maximal.append(itemset)
    return maximal
