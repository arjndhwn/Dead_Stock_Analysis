def suggest_markdown(days_in_stock):
    """
    Suggests a discount percentage based on inventory aging.
    Logic:
    0-90 days: 0% (Fresh stock)
    91-180 days: 5% (Slow mover)
    181-270 days: 15% (Dead stock - Tier 1)
    271+ days: 25% (Dead stock - Tier 2 / Liquidate)
    """
    if days_in_stock <= 90:
        return 0
    elif days_in_stock <= 180:
        return 5
    elif days_in_stock <= 270:
        return 15
    else:
        return 25

# Applying it to your Dead Stock dataframe
dead_stock['Suggested_Discount_%'] = dead_stock['Days_In_Stock'].apply(suggest_markdown)

# Calculate the new 'Clearance Price'
dead_stock['Clearance_Price'] = dead_stock['Cost_Price'] * (1 - dead_stock['Suggested_Discount_%']/100)

print("--- LIQUIDATION STRATEGY GENERATED ---")
print(dead_stock[['Stock_ID', 'Days_In_Stock', 'Suggested_Discount_%', 'Clearance_Price']].head())