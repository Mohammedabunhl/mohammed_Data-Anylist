# Procurement KPI Dashboard

This project presents a procurement performance analysis using Python and Power BI. The goal is to gain insights into order trends, supplier performance, pricing behavior, and item category statistics based on real procurement data.

## 📊 Project Overview

The project consists of two main parts:

1. **Data Cleaning & Processing (Python):**

   - Handled missing values and date inconsistencies.
   - Calculated delivery delays and adjusted incorrect delivery dates.
   - Generated new features such as waiting days and cumulative order trends.
   - Used pandas for all transformations and aggregation.

2. **Dashboard Visualization (Power BI):**
   - Built an interactive dashboard that includes:
     - Filters for order status, supplier, and date range.
     - Yearly trend of negotiated prices.
     - Category-wise total spending.
     - Supplier order counts.
     - Quantity vs. negotiated price correlation.
     - Defect analysis per item category.
     - Cumulative KPIs and price comparison.

## 🧰 Tools Used

- **Python**: Data analysis and cleaning (`pandas`, `matplotlib`)
- **Power BI**: Data visualization and KPI dashboard creation

## 📁 Files

- `data_cleaning.ipynb`: Python notebook with all processing steps.
- `dashboard.pbix`: Final Power BI dashboard file.
- `dashboard.png`: Screenshot of the Power BI report.
- `README.md`: Project documentation.
- `Procurement KPI Analysis Dataset.csv`: intial file.
- `Procurement KPI Analysis Dataset.xlsx`: final file.
## 💡 Key Insights

- Most orders were placed in mid-year months.
- Delivery delays were identified and corrected programmatically.
- Supplier Delta_Logistics had the highest number of orders.
- The average negotiated price per order is around 58.4K.
- MRO and Office Supplies had the highest total spending.

## 🔗 How to Use

1. Run the Jupyter notebook to clean the data and export results.
2. Open `dashboard.pbix` in Power BI Desktop to explore the visuals interactively.

---
