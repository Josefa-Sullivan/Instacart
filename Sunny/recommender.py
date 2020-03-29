import random

def recommender(str_list):
  '''
  Takes a list of product items as strings and returns
  three recommended products
  '''
  str_list = list(map(str.lower, str_list))
  aisles = pd.Series([prod_aisles.loc[prod_aisles['product_name'] == i, 'aisle_id'].iat[0] for i in str_list]).value_counts()

  # Finding the majority aisle from the basket of items
  if (aisles.iloc[0] == aisles.iloc[1:]).all() == True:
    maj_aisle = random.choice(aisles.index)
  else:
    maj_aisle = aisles.idxmax(axis=0)

  # Random sampling recommended aisles out of the top 10 highest lift-value aisles
  max_sample = len(cluster_top10_test[cluster_top10_test['aisle_id_x'] == maj_aisle]['aisle_id_y'])
  if max_sample == 0:
    # if there were no strong association rules produced, sample from majority aisle
    return list(top100_w_margins[top100_w_margins['aisle_id'] == maj_aisle].sample(3, weights='high_margin')['product_name'])
  elif max_sample < 3:
    #if there are less than 3 aisle lift rules
    rec_aisle = cluster_top10_test[cluster_top10_test['aisle_id_x'] == maj_aisle].sample(max_sample, weights='weights')['aisle_id_y']
  else:
    #if there are more than 3 aisle lift rules
    rec_aisle = cluster_top10_test[cluster_top10_test['aisle_id_x'] == maj_aisle].sample(3, weights='weights')['aisle_id_y']

  # Random sample three items from recommended aisles
  if len(rec_aisle) < 3:
    return list(top100_w_margins[top100_w_margins['aisle_id'].isin(list(rec_aisle))].sample(3, weights='high_margin')['product_name'])
  else:
    return [top100_w_margins[top100_w_margins['aisle_id'] == i].sample(1, weights='high_margin')['product_name'].iloc[0] for i in rec_aisle]
