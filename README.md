🌍 Global Commodity Trade Dashboard
This project is an interactive Streamlit web application for exploring and visualizing global commodity trade data. It allows users to filter data by year, trade flow type, and country, and provides rich visual analytics and descriptive statistics.

📂 Project Structure
bash
Copy
Edit
📁 Your Project/
│
├── 📄 app.py              # Streamlit application script (the provided code)
├── 📄 commodity_trade_statistics_data.csv  # Required dataset
├── 📄 README.md           # Project documentation
🚀 Features
✅ Interactive Sidebar Filters

Filter by Year, Trade Flow (Import/Export/Re-Export, etc.), and Country.

✅ Key Metrics

Shows total trade value (USD), total weight (kg), and total quantity for the selected filters.

✅ Visual Analytics

Line Chart: Yearly global trade trends for weight & quantity.

Bar Charts: Yearly comparison of total weight and quantity.

Pie Chart: Top 10 exporters by trade USD.

Scatter Plot: Quantity vs. Weight colored by trade flow.

✅ Data Snapshot

View the filtered dataset.

Inspect missing data.

✅ Descriptive Statistics

Summary statistics of the filtered dataset.

✅ User-friendly Tabs

Navigate between Data Snapshot, Visual Analytics, and Summary.

📊 Requirements
Make sure you have the following Python libraries installed:

bash
Copy
Edit
pip install streamlit pandas seaborn matplotlib plotly
📁 Dataset
The app expects a CSV file named commodity_trade_statistics_data.csv in the same directory as the script.

The dataset must include columns like:

year

flow

country_or_area

trade_usd

weight_kg

quantity

✅ Tip: Double-check your file path if you see a FileNotFoundError.

⚡ How to Run
Clone or download this repository.

Place your commodity_trade_statistics_data.csv in the same directory as app.py.

Open a terminal and run:

bash
Copy
Edit
streamlit run app.py
Your default web browser will open the dashboard.
If not, copy the provided local URL and open it manually.

🛠️ Customization
Replace commodity_trade_statistics_data.csv with your own trade dataset with the required columns.

Extend the charts or filters to match your analysis needs.

Customize styling using Streamlit’s theming or custom CSS.

✅ Example Screenshots
(Optional: Add screenshots of your dashboard here)

📜 License
This project is for educational and personal use. Feel free to adapt it to your needs.

✨ Author
Created with ❤️ using Streamlit.
Feel free to modify and expand!

