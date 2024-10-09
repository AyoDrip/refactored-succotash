import streamlit as st
import pandas as pd

file_path = 'drive/MyDrive/OTHERS/Hotel Reviews.csv'
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("Error: The file was not found. Please check the file path.")
    st.stop()

st.title("Hotel Reviews Analysis and Recommendation App")
st.subheader("Hotel Reviews Data")
st.dataframe(df.head())

def analyze_reviews(df):
    if df['Overall score'].isnull().any():
        st.warning("There are missing values in 'Overall score'. They will be ignored in the analysis.")

    average_ratings = df.groupby('name')['Overall score'].mean().reset_index()
    average_ratings = average_ratings.sort_values(by='Overall score', ascending=False)

    top_overall = average_ratings.head(15)
    categories = ['Comfort', 'Facilities', 'Staff', 'Value for money', 'Free WiFi', 'Location'] 
    top_hotels_by_category = {}

    for category in categories:
        if category in df.columns:
            category_top = df.groupby('name')[category].mean().reset_index()
            category_top = category_top.sort_values(by=category, ascending=False).head(15)
            top_hotels_by_category[category] = category_top

    return top_overall, top_hotels_by_category

top_overall, top_hotels_by_category = analyze_reviews(df)

st.subheader("Top 15 Hotels Overall")
st.dataframe(top_overall)

for category, hotels in top_hotels_by_category.items():
    st.subheader(f"Top 15 Hotels in {category}")
    st.dataframe(hotels)

def recommend_hotels(df, preferences):
    recommendations = df.copy()
    for preference in preferences:
        if preference in recommendations.columns:
            recommendations = recommendations[recommendations[preference] >= 7.0]
    recommended_hotels = recommendations.groupby('name')['Overall score'].mean().reset_index()
    recommended_hotels = recommended_hotels.sort_values(by='Overall score', ascending=False)

    return recommended_hotels

st.subheader("Hotel Recommendations Based on Preferences")
available_preferences = ['Comfort', 'Facilities', 'Staff', 'Value for money', 'Free WiFi', 
                         'Location', 'Fitness Center', 'Daily Housekeeping', 'Heating', 
                         'Free Parking', 'Airport Shuttle (free)', 'Private Parking', 
                         'Spa', 'On-site Parking', 'Room Service', 'Family Rooms', 
                         'Parking', 'Airport Shuttle', 'Air Conditioning', 'Laundry', 
                         'Water Park', 'Pet Friendly', 'Outdoor Pool', 'Indoor Pool', 
                         'Elevator', 'Garden', 'Restaurant', '24-Hour Front Desk', 'WiFi']

preferences_input = st.text_input("Enter your preferences separated by commas:")
if preferences_input:
    user_preferences = [pref.strip() for pref in preferences_input.split(',')]
    recommended_hotels = recommend_hotels(df, user_preferences)

    if not recommended_hotels.empty:
        st.write("Recommended Hotels based on your preferences:")
        st.dataframe(recommended_hotels)
    else:
        st.warning("No hotels found matching your preferences.")

