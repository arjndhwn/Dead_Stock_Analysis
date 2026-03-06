Diamond Inventory Capital Optimization
An End-to-End SQL & Python Data Pipeline

Project Goal
The primary objective of this project is to identify "Dead Stock"—diamonds held in inventory for over 180 days without a sale. By isolating these items, businesses can make data-driven decisions to adjust pricing, liquidate assets, and improve cash flow.

The Business Problem
In the diamond industry, carrying costs are high. Capital tied up in slow-moving inventory (e.g., specific shapes or colors that are currently out of fashion) prevents the business from reinvesting in high-demand stock. This project automates the detection of these "Dust Collectors."

Technical Workflow
Data Generation (data_gen.py): A Python script that simulates a professional ERP system, generating 500+ records of inventory (carat, cut, color, clarity, cost) and corresponding sales data.

Database Management (analysis.py): Uses SQLite to create a relational database. It handles the ETL process by importing CSV data into structured SQL tables.

Data Analysis (SQL): Employs Left Joins and Date Arithmetic to compare inventory against sales and identify aging stock.

Key SQL Logic
The heart of the project is the "Dead Stock" identifier:

SQL
SELECT i.Stock_ID, i.Shape, i.Cost_Price
FROM Inventory i
LEFT JOIN Sales s ON i.Stock_ID = s.Stock_ID
WHERE s.Sale_ID IS NULL 
  AND i.Purchase_Date < date('now', '-180 days');
How to Run
Clone the repository to your local machine or mobile IDE.

Generate the data: Run python data_gen.py.

Run the analysis: Run python analysis.py.

View Results: The script will output a summary of total "Locked Capital" and the top 5 highest-value items that need immediate attention.
