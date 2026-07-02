import pandas as pd
import matplotlib.pyplot as plt

internal_sales = pd.read_csv('internal_sales.csv')
competitor_prices = pd.read_csv('competitor_prices.csv')

df = pd.merge(internal_sales, competitor_prices, on="product_id", how="inner")

df["current_margin_pct"] = ((df["current_retail_price"] - df["cost_price"]) / df["current_retail_price"]) * 100

MIN_MARGIN = 0.15


def calculate_recommended_price(row):
    cost = row["cost_price"]
    retail = row["current_retail_price"]
    competitor = row["competitor_price"]

    margin_if_match = (competitor - cost) / competitor

    if retail <= competitor:
        return retail
    elif cost > competitor:
        return retail
    elif margin_if_match >= MIN_MARGIN:
        return competitor
    else:
        return round(cost / (1 - MIN_MARGIN), 2)


def classify_action(row):
    cost = row["cost_price"]
    retail = row["current_retail_price"]
    competitor = row["competitor_price"]

    margin_if_match = (competitor - cost) / competitor

    if retail <= competitor:
        return "no_change"
    elif cost > competitor:
        return "competitor_below_cost"
    elif margin_if_match >= MIN_MARGIN:
        return "price_reduced"
    else:
        return "price_at_floor"


df["recommended_price"] = df.apply(calculate_recommended_price, axis=1)
df["action"] = df.apply(classify_action, axis=1)

df["new_margin_pct"] = ((df["recommended_price"] - df["cost_price"]) / df["recommended_price"]) * 100
df["price_change"] = df["recommended_price"] - df["current_retail_price"]

df.to_csv("recommended_prices_output.csv", index=False)

print("=" * 60)
print("PRICING ANALYSIS RESULTS")
print("=" * 60)

print("\n--- Action Summary ---")
print(df["action"].value_counts().to_string())

total_margin_before = ((df["current_retail_price"] - df["cost_price"]) * df["stock_quantity"]).sum()
total_margin_after = ((df["recommended_price"] - df["cost_price"]) * df["stock_quantity"]).sum()
margin_change = total_margin_after - total_margin_before

print(f"\n--- Margin Impact ---")
print(f"Total margin BEFORE repricing: €{total_margin_before:,.2f}")
print(f"Total margin AFTER  repricing: €{total_margin_after:,.2f}")
print(f"Change: €{margin_change:,.2f} ({margin_change / total_margin_before * 100:.1f}%)")

print(f"\n--- Full Results ---")
print(df[["product_id", "product_name", "cost_price", "current_retail_price", "current_margin_pct",
          "competitor_price", "recommended_price", "new_margin_pct", "price_change", "action"]].to_string())

df["action"].value_counts().plot(kind="bar")
plt.title("Action_results")
plt.ylabel("Count")
plt.savefig('action_distribution.png', bbox_inches='tight')
plt.close()


df["total_margin_before"] = (df["current_retail_price"] - df["cost_price"])*df["stock_quantity"]
df["total_margin_after"] = (df["recommended_price"] - df["cost_price"])*df["stock_quantity"]

margin_by_category = df.groupby("category")[["total_margin_before", "total_margin_after"]].sum()

margin_by_category.plot(kind="bar", figsize=(10, 6))

plt.title("Margin_results")
plt.ylabel("Margin")
plt.xticks(rotation=0)
plt.savefig('margin_distribution.png', bbox_inches='tight')
plt.close()



df.plot(x = 'product_name', y = ['current_margin_pct', "new_margin_pct"],kind="bar", figsize=(10, 6))
plt.title("Margin_results")
plt.ylabel("Margin in %")
plt.xticks(rotation=45, ha='right')
plt.savefig('margin_diference.png', bbox_inches='tight')
plt.close()





