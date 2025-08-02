# app.py
import streamlit as st
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

from data import load_data

st.set_page_config(page_title="Restaurant Location Analysis", layout="wide")
st.title("📍 Restaurant Location-Based Analysis with Filters")

# Load Data
df = load_data()

# Sidebar Filters
st.sidebar.title("🔎 Filter Restaurants")

city_list = sorted(df['City'].dropna().unique())
selected_city = st.sidebar.selectbox("Select City:", options=["All"] + city_list)
if selected_city != "All":
    df = df[df['City'] == selected_city]

cuisine_list = sorted(df['Cuisines'].dropna().unique())
selected_cuisine = st.sidebar.selectbox("Select Cuisine:", options=["All"] + cuisine_list)
if selected_cuisine != "All":
    df = df[df['Cuisines'].str.contains(selected_cuisine)]

min_rating = st.sidebar.slider("Minimum Aggregate Rating", min_value=0.0, max_value=5.0, value=0.0, step=0.1)
df = df[df['Aggregate rating'] >= min_rating]

price_range = st.sidebar.slider("Price Range", min_value=1, max_value=4, value=(1, 4))
df = df[(df['Price range'] >= price_range[0]) & (df['Price range'] <= price_range[1])]

# Map Output
st.subheader("📌 Filtered Restaurant Locations")
if not df.empty:
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    map_ = folium.Map(location=map_center, zoom_start=12)
    marker_cluster = MarkerCluster().add_to(map_)

    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['Restaurant Name']} ({row['Cuisines']}) - {row['Aggregate rating']}★"
        ).add_to(marker_cluster)

    st_folium(map_, width=700, height=500)
else:
    st.warning("No restaurants match the selected filters.")

# Stats Output
st.subheader("🏙️ Locality Stats for Filtered Results")
if not df.empty:
    top_localities = df['Locality'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=top_localities.values, y=top_localities.index, ax=ax, palette="viridis")
    ax.set_title("Top Localities with Most Restaurants")
    ax.set_xlabel("Count")
    ax.set_ylabel("Locality")
    st.pyplot(fig)

    st.subheader("📊 Locality-wise Statistics")
    stats = df.groupby('Locality').agg({
        'Aggregate rating': 'mean',
        'Price range': 'mean',
        'Restaurant Name': 'count'
    }).rename(columns={'Restaurant Name': 'Restaurant Count'}).sort_values(by='Restaurant Count', ascending=False)

    st.dataframe(stats.head(20).style.format({
        'Aggregate rating': '{:.2f}',
        'Price range': '{:.1f}'
    }))
else:
    st.info("No data to show in stats.")
