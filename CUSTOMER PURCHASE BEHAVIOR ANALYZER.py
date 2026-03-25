# ==========================================
# CUSTOMER PURCHASE BEHAVIOR ANALYZER
# (FINAL VERSION - ALL TASKS COMPLETED)
# ==========================================

import pandas as pd
import numpy as np
import sqlite3
import os

# -------- 1. SET PATH --------
folder_path = r"C:\Users\Lenovo\Documents\Study\Data Preprocessing and Feature Engineering\Customer Purchase Behavior Analyzer"
os.chdir(folder_path)

print("Files:", os.listdir())

# -------- 2. LOAD DATA --------

# Users (Excel safe)
try:
    users = pd.read_excel("users.xlsx")
    print("✅ users.xlsx loaded")
except:
    users = pd.read_csv("users.csv")
    print("⚠️ Loaded users.csv")

# Sales
sales = pd.read_json("sales.json")

# Inventory
conn = sqlite3.connect(":memory:")
with open("inventory.sql", "r") as f:
    conn.executescript(f.read())

products = pd.read_sql("SELECT * FROM products", conn)

# -------- 3. DATA UNDERSTANDING --------
print(users.head())
print(sales.head())
print(products.head())

print(users.info())
print(sales.info())
print(products.info())

initial_records = len(sales)

# -------- 4. DATA CLEANING --------

users.fillna(users.mean(numeric_only=True), inplace=True)
users.fillna(users.mode().iloc[0], inplace=True)

sales['date'] = pd.to_datetime(sales['date'], errors='coerce')
sales = sales[sales['amount'] > 0]

# -------- 5. OUTLIER HANDLING --------

# Z-score
sales['zscore'] = (sales['amount'] - sales['amount'].mean()) / sales['amount'].std()
sales_z = sales[np.abs(sales['zscore']) < 3]

# IQR
Q1 = sales['amount'].quantile(0.25)
Q3 = sales['amount'].quantile(0.75)
IQR = Q3 - Q1

sales_iqr = sales[(sales['amount'] >= Q1 - 1.5 * IQR) &
                  (sales['amount'] <= Q3 + 1.5 * IQR)]

# Winsorization
lower = sales_iqr['amount'].quantile(0.05)
upper = sales_iqr['amount'].quantile(0.95)
sales_iqr['amount_wins'] = sales_iqr['amount'].clip(lower, upper)

# -------- 6. DATA TRANSFORMATION --------

# Date features
sales_iqr['year'] = sales_iqr['date'].dt.year
sales_iqr['month'] = sales_iqr['date'].dt.month
sales_iqr['day'] = sales_iqr['date'].dt.day

# Encoding
sales_iqr['payment_encoded'] = sales_iqr['payment_type'].astype('category').cat.codes

# One-hot encoding
sales_iqr = pd.get_dummies(sales_iqr, columns=['payment_type'])

# Binning
sales_iqr['spending_group'] = pd.cut(
    sales_iqr['amount'],
    bins=[0, 50, 100, 1000],
    labels=['Low', 'Medium', 'High']
)

# Log transform
sales_iqr['log_amount'] = np.log1p(sales_iqr['amount'])

# -------- 7. FEATURE SCALING --------

sales_iqr['amount_std'] = (sales_iqr['amount'] - sales_iqr['amount'].mean()) / sales_iqr['amount'].std()

sales_iqr['amount_minmax'] = (sales_iqr['amount'] - sales_iqr['amount'].min()) / (
    sales_iqr['amount'].max() - sales_iqr['amount'].min()
)

# -------- 8. FEATURE ENGINEERING --------

# Merge datasets
df = sales_iqr.merge(users, on='user_id', how='left')
df = df.merge(products, on='product_id', how='left')

# 1. Purchase frequency
frequency = df.groupby('user_id')['transaction_id'].count().reset_index()
frequency.rename(columns={'transaction_id': 'purchase_frequency'}, inplace=True)

# 2. Average monthly spend
monthly_spend = df.groupby(['user_id', 'month'])['amount'].mean().reset_index()
monthly_spend.rename(columns={'amount': 'avg_monthly_spend'}, inplace=True)

# 3. Days since last purchase
df['last_purchase'] = df.groupby('user_id')['date'].transform('max')
df['days_since_last_purchase'] = (pd.Timestamp.today() - df['last_purchase']).dt.days

# 4. Category-wise spend
category_spend = df.groupby(['user_id', 'category'])['amount'].sum().reset_index()
category_spend.rename(columns={'amount': 'category_total_spend'}, inplace=True)

# -------- MERGE ALL FEATURES --------

df = df.merge(frequency, on='user_id', how='left')
df = df.merge(monthly_spend, on=['user_id', 'month'], how='left')
df = df.merge(category_spend, on=['user_id', 'category'], how='left')

# -------- 9. FINAL DATASET --------

final_df = df.copy()

# -------- 10. FINAL REPORT --------

print("\n===== FINAL REPORT =====")

print("Records Before Cleaning:", initial_records)
print("Records After Cleaning:", len(sales_iqr))

print("\nMissing Values:\n", final_df.isnull().sum())

print("\nTotal Features:", final_df.shape[1])

print("\nOutliers Removed (Z-score):", initial_records - len(sales_z))
print("Outliers Removed (IQR):", initial_records - len(sales_iqr))

# -------- 11. SAVE --------

final_df.to_csv("final_cleaned_dataset.csv", index=False)

print("\n✅ FINAL DATASET CREATED SUCCESSFULLY")

# ==========================================
# END
# ==========================================