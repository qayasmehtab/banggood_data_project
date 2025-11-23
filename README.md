📦 Banggood Product Data Pipeline & Analysis

A complete end-to-end data pipeline for scraping, cleaning, analyzing, and visualizing product data from Banggood.com.

This project covers everything from web scraping → cleaning → EDA → SQL storage → dashboard visualization built using Python, Pandas, Matplotlib, Seaborn, SQLite, and Streamlit.

 Project Overview

This pipeline automates a full data workflow:

1. Web Scraping

Scrapes product data from 5 Banggood categories

Captures:

Product Name

Price

Rating

Reviews

Product URL

2. Data Cleaning

Handles missing values

Converts data types

Cleans prices & ratings

Removes duplicates

3. Exploratory Data Analysis (EDA)

Top-rated products
<img width="1024" height="1536" alt="- Architecture Diagram" src="https://github.com/user-attachments/assets/3bf98313-db1c-487d-b708-70dc0114df4c" />
<img width="1024" height="1536" alt="- Architecture Diagram" src="https://github.com/user-attachments/assets/6853638c-76d1-42d4-8b11-2e9f7adadc57" />
![Uploading Architecture Diagram.png…]()

Most expensive & cheapest products

Pricing distribution

Category insights (ratings, reviews, etc.)

 4. SQL Pipeline

Stores clean data in SQLite

Creates category-wise tables

Performs SQL aggregation queries

 5. Dashboard (Streamlit)

Interactive product analysis

Bar charts, histograms, category comparisons

Price–rating insights

📁 Project Structure
Banggood_Project/
│
├── data/
│   ├── raw/
│   └── clean/
│
├── scripts/
│   ├── banggood_scraper.py
│   ├── cleaning.py
│   ├── eda.py
│   ├── to_sql.py
│   └── dashboard.py
│
├── reports/
│   └── architecture_diagram.png
│
├── requirements.txt
├── README.md
└── main.py

🛠️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/YourUsername/Banggood_Project.git
cd Banggood_Project

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate Virtual Environment

Windows:

venv\Scripts\activate

source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

▶️ How to Run the Project
🕸️ Run the Scraper
python scripts/banggood_scraper.py

🧼 Clean the Data
python scripts/cleaning.py

📊 Run EDA
python scripts/eda.py

🗄️ Store in SQL
python scripts/to_sql.py

📈 Launch Dashboard
streamlit run scripts/dashboard.py

📸 Architecture Diagram

A high-level overview of the full pipeline.

(Add your architecture diagram here)

🤝 Contributing

Pull requests and suggestions are welcome!
Feel free to open an issue or submit improvements.

⭐ If You Like This Project

Don’t forget to Star ⭐ the repository on GitHub!
Your support motivates continuous improvement.

👨‍💻 Author

Qayas Abbasi
Cloud Data Engineer | Python Developer | Data Pipeline Enthusiast


