# 📦 Banggood Product Data Pipeline & Analysis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)

An end-to-end data engineering pipeline that automates the journey from **Web Scraping** to **Interactive Visualization**. This project extracts real-time product data from Banggood.com, cleans it, stores it in a relational database, and presents it via a modern dashboard.

---

## 🎯 Project Overview

This pipeline is designed to solve the problem of manual market research. It automates:
1. **Data Acquisition**: Scraping 5+ product categories.
2. **Data Wrangling**: Cleaning messy web data into structured formats.
3. **Database Management**: Moving CSV data into a robust SQL environment.
4. **Business Intelligence**: Creating a live dashboard for price and rating analysis.

---

## 🛠️ Tech Stack & Workflow

### 1. Web Scraping & Cleaning
- **Scraper**: Built with Python to capture Product Name, Price, Ratings, and Reviews.
- **Cleaning**: Using `Pandas` to handle missing values, remove duplicates, and fix data types.

### 2. Storage & Analysis (SQL & EDA)
- **Database**: `SQLite` integration for structured storage and category-wise table management.
- **EDA**: Statistical analysis using `Matplotlib` and `Seaborn` to find the "Cheapest vs Expensive" and "Rating Trends".

### 3. Dashboard (UI)
- **Streamlit**: An interactive web app to filter products by category and visualize pricing distributions in real-time.

---

## 📁 Project Structure

```text
Banggood_Project/
│
├── data/
│   ├── raw/                # Unprocessed scraped data
│   └── clean/              # Ready-to-use CSV files
│
├── scripts/
│   ├── banggood_scraper.py # Web scraping logic
│   ├── cleaning.py         # Data pre-processing
│   ├── eda.py              # Visual analysis scripts
│   ├── to_sql.py           # SQL database pipeline
│   └── dashboard.py        # Streamlit dashboard UI
│
├── reports/                # Architecture diagrams & screenshots
├── requirements.txt        # Project dependencies
└── main.py                 # Main execution script
