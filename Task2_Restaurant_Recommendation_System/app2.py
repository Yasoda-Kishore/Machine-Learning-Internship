import streamlit as st
from utils import load_and_clean_data

# Load the data
file_path = r"C:\Users\Yashoda\Downloads\Dataset .csv"
df = load_and_clean_data(file_path)

# Streamlit UI
st.title("🍽️ Restaurant Recommendation System")

# Sidebar
st.sidebar.header("🔎 Filter Options")

# Cuisine options
all_cuisines = df['Cuisines'].str.split(', ')
flat_list = [c.strip() for sublist in all_cuisines for c in sublist]
unique_cuisines = sorted(set(flat_list))
user_cuisine = st.sidebar.selectbox("Preferred Cuisine", unique_cuisines)

# Price range
price_range = st.sidebar.selectbox("Select Price Range", sorted(df['Price range'].dropna().unique()))

# Rating text
rating_texts = df['Rating text'].dropna().unique()
selected_rating_text = st.sidebar.selectbox("Rating Text", ['All'] + sorted(rating_texts))

# Top N
top_n = st.sidebar.slider("How many recommendations?", 5, 20, 10)

# Filtering logic
df_filtered = df[df['Price range'] == price_range].copy()

if selected_rating_text != 'All':
    df_filtered = df_filtered[df_filtered['Rating text'] == selected_rating_text]

df_filtered = df_filtered[df_filtered['Cuisines'].str.contains(rf'\b{user_cuisine}\b', case=False, na=False)]

recommended = df_filtered[df_filtered['Aggregate rating'] > 0] \
    .sort_values(by='Aggregate rating', ascending=False).head(top_n)

# Display results
if not recommended.empty:
    st.subheader(f"Top {top_n} Restaurants for '{user_cuisine}' Cuisine")
    for _, row in recommended.iterrows():
        st.markdown(f"### 🍴 {row['Restaurant Name']}")
        st.markdown(f"- 📍 Location: {row['Locality']}")
        st.markdown(f"- ⭐ Rating: {row['Aggregate rating']} | 💬 Votes: {row['Votes']}")
        st.markdown(f"- 🍛 Cuisine: `{row['Cuisines']}`")
        st.markdown("---")
else:
    st.warning("No matching restaurants found. Try changing the filters.")
