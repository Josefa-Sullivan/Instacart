import numpy as np
import pandas as pd

products = pd.read_csv('../data/products.csv')
orders = pd.read_csv('../data/orders.csv')
departments = pd.read_csv('../data/departments.csv')
aisles = pd.read_csv('../data/aisles.csv')
train = pd.read_csv('../data/order_products__train.csv')
prior = pd.read_csv('../data/order_products__prior.csv')


# Combine Orders from train and prior set because we are not concerned with the Kaggle Objective
# Shape = (33819106, 4)
priorTrain = pd.concat([prior, train])

# Merge Orders with priorTrain to include product information, Shape = (33819106, 9)
# Contains order_id, product_id, add_to_cart_order, reordered, user_id, order_number, order_dow, order_hour_of_day, days_since_prior_order
all_orders = pd.merge(priorTrain, orders, how="left", left_on="order_id", right_on="order_id").drop(['eval_set'], axis=1)


## Merge aisle, department and products into one "goods" dataframe, Shape = (49688, 6)
goods = pd.merge(left=pd.merge(left=products, right=departments, how='left'), right=aisles, how='left')

# Replace spaces in product name and aisle name with '_' but retain '-' 
goods.product_name = goods.product_name.str.replace(' ', '_').str.lower() 
goods.aisle = goods.aisle.str.replace(' ', '_').str.lower() 
goods.department = goods.department.str.replace(' ', '_').str.lower() 

# Create a dataframe with all information on orders, users, and  products
full_prod_orders = pd.merge(all_orders,goods, on = ['product_id','product_id'])

# Create a dataframe that has the total number of items bought per department for each user
dept_user_df = full_prod_orders.groupby(['user_id','department'], as_index=False).product_id.agg('count')
dept_user_df = dept_user_df.pivot(index='user_id', columns='department', values = 'product_id')
dept_user_df = dept_user_df.fillna(0)

# # Find sub-populations of users who buy baby items, pet items or alcohol
# # 34782 shoppers bought baby items
# # Max = 821, Mean = 12.6, Median = 4 
# parents = dept_user_df[dept_user_df.babies >0]

# # 15484 shoppers who bought pet items
# # Max = 522
# # Median = 3, Mean = 6.6
# pet_owners = dept_user_df[dept_user_df.pets >0]

# # 16104 shoppers bought alcohol
# # One shopper bought 685 alcohol items
# # median = 4, avg = 9.9
# drinkers = dept_user_df[dept_user_df.alcohol >0]