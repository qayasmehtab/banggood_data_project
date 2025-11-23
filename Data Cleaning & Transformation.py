# ==============================
# Banggood Full Pipeline
# Scraping → Cleaning → EDA → SQL
# Author: Qayas Abbasi
# Date: 2025
# ==============================

import os
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pyodbc

# -----------------------------
# CONFIG
# -----------------------------
RAW_DIR = "D:/Banggood_Project/data/raw"
CLEAN_DIR = "D:/Banggood_Project/data/cleaned"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(CLEAN_DIR, exist_ok=True)

CATEGORIES = {
    "phones": "https://www.banggood.com/search/phones.html?from=nav&page={}",
    "smartwatches": "https://www.banggood.com/search/smartwatches.html?from=nav&page={}",
    "laptops": "https://www.banggood.com/search/laptops.html?from=nav&page={}",
    "rc_drones": "https://www.banggood.com/search/rc-drones.html?from=nav&page={}",
    "home_appliances": "https://www.banggood.com/search/home-appliances.html?from=nav&page={}"
}

MAX_PAGES = 5

SQL_CONFIG = {
    "driver": "{ODBC Driver 17 for SQL Server}",
    "server": "DESKTOP-CJ2TM4F",
    "database": "BanggoodDB"
}

# -----------------------------
# Selenium driver
# -----------------------------
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


# -----------------------------
# Scraping
# -----------------------------
def scrape_category(category_name, url_template):
    driver = get_driver()
    all_products = []

    print(f"\nScraping category: {category_name}")

    for page in tqdm(range(1, MAX_PAGES + 1), desc=f"{category_name} pages"):
        driver.get(url_template.format(page))
        time.sleep(random.uniform(2, 4))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        items = driver.find_elements(By.CSS_SELECTOR, "div.p-wrap")
        if not items:
            break

        for item in items:
            try:
                t = item.find_element(By.CSS_SELECTOR, "a.title")
                name = t.text.strip()
                url = t.get_attribute("href")
            except:
                name, url = None, None

            def get(css):
                try:
                    return item.find_element(By.CSS_SELECTOR, css).text.strip()
                except:
                    return None

            all_products.append({
                "category": category_name,
                "product_name": name,
                "product_url": url,
                "price": get("span.price"),
                "old_price": get("span.price-old"),
                "discount": get("span.price-discount"),
                "reviews": get("a.review"),
                "rating": get("span.review-text"),
            })

    driver.quit()

    output_file = os.path.join(RAW_DIR, f"{category_name}_raw.csv")
    df = pd.DataFrame(all_products)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} items → {output_file}")
    return df


# -----------------------------
# Cleaning
# -----------------------------
def clean_data(df):
    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
    df["old_price"] = pd.to_numeric(df["old_price"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
    df["discount"] = pd.to_numeric(df["discount"].astype(str).str.replace(r"[^\d.]", "", regex=True), errors="coerce")
    df["reviews"] = pd.to_numeric(df["reviews"].astype(str).str.extract(r"(\d+)")[0], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"].astype(str).str.extract(r"([\d.]+)")[0], errors="coerce")

    df.fillna({
        "old_price": df["price"],
        "discount": 0,
        "reviews": 0,
        "rating": 0,
    }, inplace=True)

    df["price_drop"] = df["old_price"] - df["price"]
    df["value_score"] = df["rating"] * df["reviews"] / (df["price"] + 1)

    return df


# -----------------------------
# Professional EDA
# -----------------------------
def exploratory_analysis(df):
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("Set2")

    # 1 Price Distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x="price", hue="category", bins=50, kde=True, palette=palette, multiple="stack")
    plt.title("📊 Price Distribution by Category", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(CLEAN_DIR, "price_distribution.png"))
    plt.close()

    # 2 Rating vs Price
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x="price", y="rating", hue="category", palette=palette, s=80, alpha=0.7)
    plt.title("⭐ Rating vs Price", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(CLEAN_DIR, "rating_vs_price.png"))
    plt.close()

    # 3 Top 10 Reviewed Products
    top10 = df.sort_values("reviews", ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top10, x="reviews", y="product_name", palette="viridis")
    plt.title("🏆 Top 10 Reviewed Products", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(CLEAN_DIR, "top10_reviews.png"))
    plt.close()

    # 4 Price Drop by Category
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="category", y="price_drop", palette=palette)
    plt.title("💰 Price Drop Distribution", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(CLEAN_DIR, "price_drop.png"))
    plt.close()

    # 5 Value Score by Category
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="category", y="value_score", palette=palette)
    plt.title("📈 Value Score Distribution", fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(CLEAN_DIR, "value_score.png"))
    plt.close()

    print("✔ Professional EDA charts saved!")


# -----------------------------
# SQL Deployment
# -----------------------------
def deploy_to_sql(df):
    conn_master = pyodbc.connect(
        f"DRIVER={SQL_CONFIG['driver']};SERVER={SQL_CONFIG['server']};Trusted_Connection=yes;",
        autocommit=True,
    )
    cur = conn_master.cursor()
    cur.execute(f"IF DB_ID('{SQL_CONFIG['database']}') IS NULL CREATE DATABASE {SQL_CONFIG['database']};")
    conn_master.close()

    conn = pyodbc.connect(
        f"DRIVER={SQL_CONFIG['driver']};SERVER={SQL_CONFIG['server']};DATABASE={SQL_CONFIG['database']};Trusted_Connection=yes;"
    )
    cur = conn.cursor()

    cur.execute("""
        IF OBJECT_ID('banggood_products') IS NULL
        CREATE TABLE banggood_products(
            id INT IDENTITY(1,1) PRIMARY KEY,
            category VARCHAR(100),
            product_name VARCHAR(255),
            product_url VARCHAR(500) UNIQUE,
            price FLOAT,
            old_price FLOAT,
            discount INT,
            reviews INT,
            rating FLOAT,
            price_drop FLOAT,
            value_score FLOAT
        )
    """)
    conn.commit()

    for _, row in df.iterrows():
        try:
            cur.execute("""
                INSERT INTO banggood_products
                (category, product_name, product_url, price, old_price, discount, reviews, rating, price_drop, value_score)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, row["category"], row["product_name"], row["product_url"], row["price"],
               row["old_price"], row["discount"], row["reviews"], row["rating"],
               row["price_drop"], row["value_score"])
        except:
            pass

    conn.commit()
    conn.close()
    print("✔ SQL Upload Completed!")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def main_pipeline():
    all_dfs = []

    for cat, url in CATEGORIES.items():
        df_raw = scrape_category(cat, url)
        df_clean = clean_data(df_raw)
        all_dfs.append(df_clean)

    df_final = pd.concat(all_dfs, ignore_index=True)
    df_final.to_csv(os.path.join(CLEAN_DIR, "banggood_cleaned.csv"), index=False)

    exploratory_analysis(df_final)
    deploy_to_sql(df_final)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    main_pipeline()
