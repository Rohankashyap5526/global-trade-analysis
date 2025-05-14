import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# ------------------- PAGE CONFIG -------------------
st.set_page_config(page_title="🌍 Global Trade Dashboard", layout="wide")
st.title("🌍 Global Commodity Trade Dashboard")

# ------------------- LOAD DATA -------------------
DATA_PATH = "commodity_trade_statistics_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

try:
    df = load_data()

    # ------------------- SIDEBAR FILTERS -------------------
    st.sidebar.header("🔎 Filter Data")
    years = sorted(df["year"].dropna().unique())
    selected_year = st.sidebar.selectbox("Select Year", years, index=len(years) - 1)
    flows = df["flow"].dropna().unique().tolist()
    selected_flows = st.sidebar.multiselect("Select Trade Flow", flows, default=flows)
    countries = ["All"] + sorted(df["country_or_area"].dropna().unique())
    selected_country = st.sidebar.selectbox("Select Country", countries)

    # Apply filters
    filtered_df = df[(df["year"] == selected_year) & (df["flow"].isin(selected_flows))]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df["country_or_area"] == selected_country]

    # ------------------- METRICS DISPLAY -------------------
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Trade (USD)", f"${filtered_df['trade_usd'].sum():,.0f}" if 'trade_usd' in filtered_df else "N/A")
    col2.metric("Total Weight (kg)", f"{filtered_df['weight_kg'].sum():,.0f}")
    col3.metric("Total Quantity", f"{filtered_df['quantity'].sum():,.0f}")

    # ------------------- TABS FOR SECTIONS -------------------
    tab1, tab2, tab3 = st.tabs(["📄 Data Snapshot", "📈 Visual Analytics", "📌 Summary"])

    with tab1:
        st.subheader(f"Data Preview - {selected_year}")
        st.dataframe(filtered_df.head(20), use_container_width=True)

        with st.expander("🔍 Missing Data Overview"):
            st.dataframe(filtered_df.isnull().sum().reset_index().rename(columns={0: "Missing Count"}))

    with tab2:
        # LINE CHART: GLOBAL TRENDS
        st.subheader("📈 Global Trade Trends Over Time")
        df_yearly = df[df["flow"].isin(selected_flows)].groupby("year")[["weight_kg", "quantity"]].sum().reset_index()

        fig_line = go.Figure([
            go.Scatter(x=df_yearly["year"], y=df_yearly["weight_kg"], mode="lines+markers", name="Weight (kg)", line=dict(color="royalblue")),
            go.Scatter(x=df_yearly["year"], y=df_yearly["quantity"], mode="lines+markers", name="Quantity", line=dict(color="darkorange")),
        ])
        fig_line.update_layout(title="Yearly Global Trade by Weight & Quantity", xaxis_title="Year", yaxis_title="Total", template="plotly_white")
        st.plotly_chart(fig_line, use_container_width=True)

        # BAR CHART SUBPLOTS
        st.subheader("📊 Yearly Trade Comparison")
        df_agg = df[df["flow"].isin(selected_flows)].groupby("year")[["weight_kg", "quantity"]].sum().reset_index()

        fig_bar = make_subplots(rows=1, cols=2, subplot_titles=("Weight (kg)", "Quantity"))
        fig_bar.add_trace(go.Bar(x=df_agg["year"], y=df_agg["weight_kg"], marker_color="royalblue"), row=1, col=1)
        fig_bar.add_trace(go.Bar(x=df_agg["year"], y=df_agg["quantity"], marker_color="orange"), row=1, col=2)
        fig_bar.update_layout(height=450, showlegend=False, title_text="Comparative Trade Overview")
        st.plotly_chart(fig_bar, use_container_width=True)

        # PIE CHART: TOP EXPORTERS
        if "trade_usd" in df.columns:
            st.subheader(f"🌍 Top 10 Exporters by USD - {selected_year}")
            top_exporters = filtered_df[filtered_df["flow"] == "Export"].groupby("country_or_area")["trade_usd"].sum().nlargest(10)

            fig_pie = go.Figure(data=[go.Pie(labels=top_exporters.index, values=top_exporters.values, hole=0.4, textinfo="label+percent")])
            fig_pie.update_layout(title="Top Exporting Countries", template="seaborn")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("⚠️ 'trade_usd' column not found in the dataset.")

        # SCATTER PLOT
        st.subheader("📉 Trade Volume: Quantity vs Weight")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.scatterplot(data=filtered_df, x="quantity", y="weight_kg", hue="flow", alpha=0.6)
        ax.set_title("Trade Volume by Flow Type")
        st.pyplot(fig)

    with tab3:
        st.subheader("📌 Descriptive Statistics")
        st.dataframe(filtered_df.describe(include="all"), use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ File not found at `{DATA_PATH}`. Please verify the path and try again.")
