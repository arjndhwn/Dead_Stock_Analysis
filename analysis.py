import sqlite3
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt


# 1. Setup Connection
conn = sqlite3.connect('diamond_analysis.db')

# 2. Import CSVs to SQL
inventory_df = pd.read_csv('diamond_inventory.csv')
sales_df = pd.read_csv('diamond_sales.csv')

inventory_df.to_sql('Inventory', conn, if_exists='replace', index=False)
sales_df.to_sql('Sales', conn, if_exists='replace', index=False)

# 3. The Dead Stock SQL Query
# We identify stones purchased > 180 days ago that don't appear in the Sales table
query = """
SELECT 
    i.Stock_ID, 
    i.Shape, 
    i.Carat, 
    i.Color,
    i.Cost_Price,
    i.Purchase_Date
FROM Inventory i
LEFT JOIN Sales s ON i.Stock_ID = s.Stock_ID
WHERE s.Sale_ID IS NULL 
  AND i.Purchase_Date < date('2026-03-06', '-180 days')
ORDER BY i.Cost_Price DESC;
"""

# 4. Execute and Display
dead_stock = pd.read_sql(query, conn)

print("--- DEAD STOCK ANALYSIS REPORT ---")
print(f"Total Dead Stock Stones Found: {len(dead_stock)}")
print(f"Total Capital Locked: ${dead_stock['Cost_Price'].sum():,}")
print("\nTop 5 High-Value Items to Liquidate:")
print(dead_stock.head(5))


# 1. Prepare data for visualization
chart_data = dead_stock.groupby('Shape')['Cost_Price'].sum()

# 2. Create the plot
plt.figure(figsize=(10, 6))
chart_data.plot(kind='bar', color='skyblue', edgecolor='black')

# 3. Add professional labels
plt.title('Capital Locked in Dead Stock by Diamond Shape', fontsize=14)
plt.xlabel('Diamond Shape', fontsize=12)
plt.ylabel('Total Locked Capital ($)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 4. Save the file for your portfolio
plt.tight_layout()
plt.savefig('dead_stock_report.png')
print("\n[SUCCESS] Visual report saved as 'dead_stock_report.png'")

conn.close()
