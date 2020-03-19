'''
Goal: To return a csv with the association rules with product item_names

This file will ask for the name of the csv within the data folder to use
as the dataframe to create the association rules with. It will also ask
for a minimum support value (between 0 and 1).
'''

import pandas as pd
import numpy as np
from itertools import combinations, groupby
from collections import Counter

# Returns the frequency count from a dataframe
def freq_items(item_df):
    return item_df['product_id'].value_counts().rename('freq')

# Returns the frequency count from a generator
def freq_generator(iterable):
    return pd.Series(Counter(iterable)).rename('freq')

# Returns a generator of item sets
def item_sets(item_df):
    m = item_df[['order_id','product_id']].as_matrix()
    for order_id, order_object in groupby(m, lambda x: x[0]):
        item_list = [item[1] for item in order_object]
        for item_pair in combinations(item_list, 2):
            yield(item_pair)

# Returns frequency and support associated with item
def merge_item_stats(item_pairs, item_stats):
    return (item_pairs
                .merge(item_stats.rename(columns={'freq': 'freqA', 'support': 'supportA'}), left_on='item_A', right_index=True)
                .merge(item_stats.rename(columns={'freq': 'freqB', 'support': 'supportB'}), left_on='item_B', right_index=True))

# Returns name associated with item
def merge_item_name(rules, item_name):
    '''
    Takes the rules dataframe resulting from the association_rules() function
    and also takes the item_names as a dataframe (formated like products.csv)
    '''
    # Renames the columns for products.csv
    item_name = item_name.rename(columns={'product_id':'item_id', 'product_name':'item_name'})

    columns = ['itemA','itemB','freqAB','supportAB','freqA','supportA','freqB','supportB',
               'confidenceAtoB','confidenceBtoA','lift']
    rules = (rules
                .merge(item_name.rename(columns={'item_name': 'itemA'}), left_on='item_A', right_on='item_id')
                .merge(item_name.rename(columns={'item_name': 'itemB'}), left_on='item_B', right_on='item_id'))
    return rules[columns]

# Returns dataframe of association rules with the product_ids
def association_rules(item_df, min_support):
    '''
    Takes a dataframe with columns ['order_id','product_id']
    and min_support as a decimal to output a rules dataframe.
    '''
    # Filters out orders with only one item
    more_than2 = item_df[item_df['order_id'].isin(item_df['order_id'].value_counts()[item_df['order_id'].value_counts()>=2].index)]

    # Calculates the frequency and support of the items
    item_stats = freq_items(more_than2).to_frame('freq')
    item_stats['support'] = item_stats['freq'] / len(more_than2['order_id'].unique())

    # Returns product_ids that pass the min_support
    # Returns the order_ids that contain the products that pass min_support
    qualifying_items = item_stats[item_stats['support'] >= min_support].index
    qualifying_orders = more_than2[more_than2['product_id'].isin(qualifying_items)]['order_id'].unique()

    # Updates the original dataframe, having filtered out orders with one item & those that don't pass min_support
    item_df = item_df[item_df['order_id'].isin(qualifying_orders)]

    # Re-calculates frequency and support of the items
    item_stats = freq_items(item_df).to_frame('freq')
    item_stats['support'] = item_stats['freq'] / len(item_df['order_id'].unique())

    # Calls the generator to grab item pairs
    item_pair_gen = item_sets(item_df)

    # Calculates the frequency and support of item pairs
    item_pair_stats = freq_generator(item_pair_gen).to_frame('freqAB')
    item_pair_stats['supportAB'] = item_pair_stats['freqAB'] / len(qualifying_orders)

    # Filters out the item pairs that do not meet the min_support
    item_pair_stats = item_pair_stats[item_pair_stats['supportAB'] >= min_support]
    item_pair_stats = item_pair_stats.reset_index().rename(columns={'level_0': 'item_A', 'level_1': 'item_B'})

    # Creates table of association rules and compute relevant metrics
    item_pair_stats = merge_item_stats(item_pair_stats, item_stats)

    item_pair_stats['confidenceAtoB'] = item_pair_stats['supportAB'] / item_pair_stats['supportA']
    item_pair_stats['confidenceBtoA'] = item_pair_stats['supportAB'] / item_pair_stats['supportB']
    item_pair_stats['lift']           = item_pair_stats['supportAB'] / (item_pair_stats['supportA'] * item_pair_stats['supportB']) * 100

    # Return association rules sorted by lift in descending order
    return item_pair_stats.sort_values('lift', ascending=False)

################################################################################

fileinput = str(input("Indicate the file you want to use as the input dataframe: "))
min_support_input = input("Indicate the minimum support (value between 0 and 1): ")

if float(min_support_input) > 1.0 or float(min_support_input) < 0.0:
    print("Invalid entry for minimum support. ")

orders_products_df = pd.read_csv(f'../data/{fileinput}')
orders_products_df = orders_products_df[['order_id','product_id']]

rules = association_rules(orders_products_df, float(min_support_input))

rules_final = merge_item_name(rules, product_name).sort_values('lift', ascending=False)
rules_final.to_csv('../data/association_rules_df.csv')
