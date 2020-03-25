library(psych)
library(tidyverse)
library(GPArotation)

df = read.csv('../data/orders_fa.csv', header = T, stringsAsFactors = F)
df %>% head()


# Fill NA with arbitrary value 100, indicates first order of  customer
df$days_since_prior_order = replace_na(df$days_since_prior_order,100)


scree(df)
cor(df)

# Choose 2 factors based on Scree
fa.parallel(df)

# RMSEA value is below 0.06 (0.01 for df excluding depts) 
fa(r = df, nfactors = 6, rotate = 'oblimin', fm ='minres')

fa(r = df, nfactors = 3, rotate = 'oblimin', fm ='minres')


print( fa( r = df, nfactors = 2, rotate = 'oblimin', fm ='minres')$loadings, cut=0.2)
# Factor 1 contains order_number, days since last order and 
# the percentage of items in an order that are reordered
# Factor 2 seems to be simply the number of items per order


df$snacks %>% unique()

df = df %>% select(-bulk)

sapply(df, class) 


fa(r = df, nfactors = 11, rotate = 'oblimin', fm ='minres')

print( fa( r = df, nfactors = 11, rotate = 'oblimin', fm ='minres')$loadings, cut=0.2)
