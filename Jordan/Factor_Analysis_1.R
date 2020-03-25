

library(psych)

##################
### EVERYTHING ###
##################

#Too computationallly heavy

df = read.csv('../data/user_summary.csv')

df = subset(df, select = -c(total_prod_day_grouping, total_prod_day,total_prod_hour_grouping))

df[is.na(df)] = 0
head(df)

describe(df)

scree(df)

fa.parallel(df)

fa(df,11,fm='minres',rotate='oblimin')

print(fa(df,11,fm='minres',rotate='oblimin')$loadings,cut=.2)


###############
### Parents ###
###############

# All Features
parents = read.csv('../data/parents_all.csv')
parents = subset(parents, select = -c(user_id))
head(parents)
describe(parents)

scree(parents)

fa.parallel(parents)

fa(parents,12,fm='minres',rotate='oblimin')

print(fa(parents,12,fm='minres',rotate='oblimin')$loadings,cut=.2)


# Time Features
parents_time = read.csv('../data/parents_all.csv')
parents_time = subset(parents, select = c(total_prod_morning, total_prod_lunch, total_prod_afternoon,
                                          total_prod_evening, total_prod_afterhours, total_prod_early_week,
                                          total_prod_late_week,total_prod_weekend, med_products, 
                                          med_days, med_reordered))
head(parents_time)

scree(parents_time)

fa.parallel(parents_time)

fa(parents_time,3,fm='minres',rotate='oblimin')

print(fa(parents_time,3,fm='minres',rotate='oblimin')$loadings,cut=.2)



# Time and Products
parents_time_prods = read.csv('../data/parents_all.csv')
parents_time_prods = subset(parents, select = c(alcohol,babies,bakery,beverages,breakfast,bulk,canned_goods,
                                                dairy_eggs,deli,dry_goods_pasta,frozen,household,international,
                                                meat_seafood,missing,other,pantry,personal_care,pets,produce,
                                                snacks,total_prod_morning, total_prod_lunch,
                                                total_prod_afternoon,total_prod_evening, total_prod_afterhours,
                                                total_prod_early_week,total_prod_late_week,total_prod_weekend,
                                                med_products,med_days, med_reordered))

scree(parents_time_prods)

fa.parallel(parents_time_prods)

fa(parents_time_prods,5,fm='minres',rotate='oblimin')

print(fa(parents_time_prods,5,fm='minres',rotate='oblimin')$loadings,cut=.2)



# Days, Hours, Products
parents_dhp = read.csv('../data/parents_all.csv')
parents_dhp = subset(parents, select = c(alcohol, babies, bakery, beverages, breakfast, 
                                         bulk, canned_goods, dairy_eggs, deli, dry_goods_pasta, 
                                         frozen, household, international, meat_seafood, missing, 
                                         other, pantry, personal_care, pets, produce, snacks, 
                                         per_prod_sat, per_prod_sun, per_prod_mon, per_prod_tues, 
                                         per_prod_wed, per_prod_thur, per_prod_fri, per_prod_0, 
                                         per_prod_1, per_prod_2, per_prod_3, per_prod_4, per_prod_5, 
                                         per_prod_6, per_prod_7, per_prod_8, per_prod_9, per_prod_10, 
                                         per_prod_11, per_prod_12, per_prod_13, per_prod_14, 
                                         per_prod_15, per_prod_16, per_prod_17, per_prod_18, 
                                         per_prod_19, per_prod_20, per_prod_21, per_prod_22, per_prod_23))

scree(parents_dhp)

fa.parallel(parents_dhp)

fa(parents_dhp,10,fm='minres',rotate='oblimin')

print(fa(parents_dhp,10,fm='minres',rotate='oblimin')$loadings,cut=.2)














