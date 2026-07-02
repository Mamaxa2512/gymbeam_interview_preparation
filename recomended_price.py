import pandas as pd

internal_sales = pd.read_csv('internal_sales.csv')
competitor_prices = pd.read_csv('competitor_prices.csv')

#print(internal_sales.shape, internal_sales.dtypes, internal_sales.head(5))
#print(competitor_prices.shape, competitor_prices.dtypes, competitor_prices.head(5))

compare_table = pd.merge(internal_sales, competitor_prices, on="product_id", how="inner")


#print(compare_table)

compare_table["margin"] = ((compare_table["current_retail_price"] - compare_table["cost_price"])/compare_table["current_retail_price"])*100


def recommended_price(row):
    marge_if_match = ((row["competitor_price"] - row["cost_price"]) / row["competitor_price"]) * 100
    if row['current_retail_price'] <= row['competitor_price']:
        row['recommended_price'] = row['current_retail_price']
    elif row['cost_price'] > row['competitor_price']:
        row['recommended_price'] = row['current_retail_price']
    elif marge_if_match >= 15:
        row['recommended_price'] = row['competitor_price']
    else:
         row['recommended_price'] = row["cost_price"]/0.85
    return row['recommended_price']


compare_table["recommended_price"] = compare_table.apply(recommended_price, axis=1)

print(compare_table)
