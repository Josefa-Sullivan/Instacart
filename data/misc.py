orders_weekend = orders_weekend[orders_weekend['user_id'].isin(weekend_userids)]
weekend_ordersid = orders_weekend['order_id'].unique()
order_products_weekend = order_products[order_products['order_id'].isin(weekend_ordersid)]
weekend_apriori = order_products_weekend[['order_id','product_id']]
weekend_apriori_aisles = weekend_apriori.merge(products, how='left', left_on='product_id', right_on='product_id')
weekend_apriori_aisles = weekend_apriori_aisles[['order_id','aisle_id']]

weekend_rules = association_rules(weekend_apriori_aisles, min_support=0.001)
weekend_buyer_rules = merge_item_name(weekend_rules, aisles)
wkndbr1 = weekend_buyer_rules[weekend_buyer_rules['lift'] > 1.0]

'''
Input: 'Bananas','Strawberries','Organic Coconut Milk'

- Majority aisle = fresh fruit 
- Look at the highest lift aisle for majority aisle
- Then suggest random item in that aisle? (random, top 3, etc.)

'''

orders = pd.read_csv('orders.csv')
groupby_user = orders.groupby('user_id')['order_dow'].agg(lambda x: set(x)).reset_index()
groupby_user['set_length'] = groupby_user['order_dow'].apply(len)
weekend_userids = list(groupby_user[groupby_user['order_dow'] == {0, 1}]['user_id'].unique())
weekend_orderids = orders[orders['user_id'].isin(weekend_userids)]['order_id']
weekend_apriori_df = order_prod[order_prod['order_id'].isin(weekend_orderids)][['order_id','product_id']]

'''
Where weekend_final = final association rules that were mined
- Get rid of same aisles in itemA & item_B
- Filter out lift above 1.02
- Grab the top10 in each group
'''
weekend_final.drop( weekend_final[weekend_final['itemA'] == weekend_final['itemB']].index, inplace=True )
weekend_final.drop( weekend_final[weekend_final['lift'] <= 1.02].index, inplace=True )
weekend_top10 = weekend_final.sort_values('lift',ascending = False).groupby('itemA').head(10)
# Adding weights
weekend_top10['weights'] = weekend_top10.sort_values(by='lift', ascending=True).groupby('itemA').cumcount()+1
# Need to add in the aisle_ids for itemA, itemB
