import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Configuration
NUM_INVENTORY = 500  # Total stones ever purchased
NUM_SALES = 350      # Stones actually sold
SEED_DATE = datetime(2026, 3, 6) # Current Date for calculations

# Helper to generate random dates
def random_date(start_year=2024):
    start = datetime(start_year, 1, 1)
    end = SEED_DATE
    return start + timedelta(days=random.randint(0, (end - start).days))

# 1. Generate Inventory Data
shapes = ['Round', 'Princess', 'Emerald', 'Oval', 'Pear']
colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
clarities = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2']

inventory_data = []
for i in range(1, NUM_INVENTORY + 1):
    stock_id = f"DIA-{1000 + i}"
    carat = round(random.uniform(0.3, 3.0), 2)
    # Price logic: Roughly $3000 per carat + random variance
    cost_price = int((carat * 3000) * random.uniform(0.8, 1.2))
    
    inventory_data.append({
        'Stock_ID': stock_id,
        'Shape': random.choice(shapes),
        'Carat': carat,
        'Color': random.choice(colors),
        'Clarity': random.choice(clarities),
        'Purchase_Date': random_date(2024).strftime('%Y-%m-%d'),
        'Cost_Price': cost_price
    })

df_inventory = pd.DataFrame(inventory_data)

# 2. Generate Sales Data (Subset of Inventory)
# We pick 350 random items from the inventory to "sell"
sold_items = df_inventory.sample(n=NUM_SALES)
sales_data = []

for idx, row in sold_items.iterrows():
    # Sale date must be AFTER purchase date
    p_date = datetime.strptime(row['Purchase_Date'], '%Y-%m-%d')
    sale_date = p_date + timedelta(days=random.randint(1, 90))
    
    # Ensure we don't sell in the future relative to our seed date
    if sale_date > SEED_DATE:
        sale_date = SEED_DATE
        
    sales_data.append({
        'Sale_ID': f"SAL-{5000 + idx}",
        'Stock_ID': row['Stock_ID'],
        'Sale_Date': sale_date.strftime('%Y-%m-%d'),
        'Sale_Price': int(row['Cost_Price'] * random.uniform(1.1, 1.5)), # 10-50% markup
        'Customer_Type': random.choice(['Retail', 'Wholesale'])
    })

df_sales = pd.DataFrame(sales_data)

# Export to CSV
df_inventory.to_csv('diamond_inventory.csv', index=False)
df_sales.to_csv('diamond_sales.csv', index=False)

print("Files created: 'diamond_inventory.csv' and 'diamond_sales.csv'")
print(f"Total Inventory: {len(df_inventory)} | Total Sales: {len(df_sales)}")