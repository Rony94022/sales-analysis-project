import pandas as pd

# Load dataset
df = pd.read_csv("train.csv")

# Show first 5 rows
print(df.head())
# print(df.columns)
# print(df.info())
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

print("Missing values:\n", df.isnull().sum())
df = df.drop_duplicates()
print("Shape after cleaning: ",df.shape)
# Create Month column
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)
# Create Year column
df['Year'] = df['Order Date'].dt.year
print(df[['Order Date', 'Month', 'Year']].head())
total_sales = df['Sales'].sum()
print("Total Sales:", total_sales)
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
print(region_sales)
category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
print(category_sales)
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
print(top_products)
top_cities = df.groupby('City')['Sales'].sum().sort_values(ascending=False).head(5)
print(top_cities)
segment_sales = df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
print(segment_sales)
monthly_sales = df.groupby('Month')['Sales'].sum()
print(monthly_sales)
last_3_months = monthly_sales.tail(3)

predicted_sales = last_3_months.mean()

print("Predicted Next Month Sales:", predicted_sales)
df.to_csv("cleaned_sales_data.csv", index=False)

#SQL
import sqlite3

# Create connection
conn = sqlite3.connect("sales.db")

# Save dataframe to SQL table
df.to_sql("sales_data", conn, if_exists="replace", index=False)

print("Data loaded into SQLite successfully!")

query = """
SELECT SUM(Sales) AS Total_Sales
FROM sales_data;
"""

result = pd.read_sql(query, conn)
print(result)

#Region-wise Sales Query
query = """
SELECT Region, SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY Region
ORDER BY Total_Sales DESC;
"""
result = pd.read_sql(query, conn)
print(result)

#Top Products Query
query = """
SELECT [Product Name], SUM(Sales) AS Total_Sales
FROM sales_data
GROUP BY [Product Name]
ORDER BY Total_Sales DESC
LIMIT 5;
"""

result = pd.read_sql(query, conn)
print(result)

conn.close()
df.to_csv("cleaned_sales.csv", index=False)