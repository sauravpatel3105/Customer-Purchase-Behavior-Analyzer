
# Customer Purchase Behavior Analyzer

##  Project Overview

The **Customer Purchase Behavior Analyzer** is a Python-based data preprocessing and feature engineering project that analyzes customer purchasing patterns using multi-format datasets (Excel, JSON, SQL).
The project transforms raw data into a clean and structured dataset for further analytics or machine learning.

##  Objective
To design a complete data preprocessing pipeline that:

* Cleans and transforms raw data
* Handles missing values and outliers
* Engineers meaningful features
* Prepares a final dataset for analysis

##  Dataset Description

The project uses three datasets:
1. **users.xlsx**

   * Customer details (user_id, name, age, gender, city, registration_date)

2. **sales.json**

   * Transaction data (transaction_id, user_id, product_id, amount, payment_type, date)

3. **inventory.sql**

   * Product data (product_id, product_name, category, price, stock)

##  Technologies Used

* Python
* Pandas
* NumPy
* SQLite3

##  Workflow / Steps

### 1. Data Loading

* Loaded data from Excel, JSON, and SQL sources
* Verified structure using `.head()` and `.info()`

### 2. Data Cleaning

* Handled missing values using mean and mode
* Removed invalid entries (negative amounts, incorrect dates)

### 3. Outlier Handling

* Applied:

  * Z-score method
  * IQR method
* Used Winsorization to cap extreme values

### 4. Data Transformation

* Extracted date features (year, month, day)
* Applied:

  * Label Encoding
  * One-Hot Encoding
* Performed:

  * Binning (Low, Medium, High spending groups)
  * Log transformation

### 5. Feature Scaling

* Standard Scaling
* Min-Max Scaling

### 6. Feature Engineering

Created new features:

* Purchase frequency
* Average monthly spending
* Days since last purchase
* Category-wise total spending

### 7. Final Dataset

* Merged all datasets
* Generated cleaned dataset:
   `final_cleaned_dataset.csv`
##  Key Insights

* Most customers fall into low to medium spending categories
* Digital payment methods are widely used
* Some customers are highly active, while others are inactive
* Certain product categories generate higher revenue

##  Project Structure

```
Customer Purchase Behavior Analyzer/
│── CUSTOMER PURCHASE BEHAVIOR ANALYZER.py
│── users.xlsx
│── sales.json
│── inventory.sql
│── final_cleaned_dataset.csv
│── README.md
```

##  How to Run

1. Clone the repository:

```
git clone <your-repo-link>
```

2. Navigate to the project folder:

```
cd Customer Purchase Behavior Analyzer
```

3. Run the script:

```
python CUSTOMER PURCHASE BEHAVIOR ANALYZER.py
```
##  Output

* Cleaned dataset: `final_cleaned_dataset.csv`
* Console report with:

  * Missing values
  * Outlier analysis
  * Feature summary

##  Conclusion

This project demonstrates a complete data preprocessing pipeline that transforms raw customer transaction data into a structured format.
The engineered features provide valuable insights for customer segmentation, targeted marketing, and business decision-making
