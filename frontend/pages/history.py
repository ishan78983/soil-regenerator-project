import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Recommendation History", page_icon="📜", layout="wide")

st.title("📜 Recommendation History")
st.markdown("Browse through all previously generated soil health recommendations.")

# --- Backend API URL ---
API_URL = "http://127.0.0.1:8000"

try:
    # Make a GET request to the /history endpoint
    response = requests.get(f"{API_URL}/history")
    response.raise_for_status()
    history_data = response.json()

    if not history_data:
        st.info("No history found. Generate your first recommendation on the main page!")
    else:
        df = pd.DataFrame(history_data)
        st.dataframe(df[['timestamp', 'location', 'ph_level', 'organic_matter']], use_container_width=True)

        st.markdown("---")
        st.subheader("Detailed View")
        selected_id = st.selectbox(
            "Select a recommendation to view details", 
            options=df['id'], 
            format_func=lambda x: f"Rec ID: {x} on {pd.to_datetime(df.loc[df['id'] == x, 'timestamp'].iloc[0]).strftime('%Y-%m-%d %H:%M')}"
        )
        
        if selected_id:
            selected_row = df[df['id'] == selected_id].iloc[0]
            with st.expander(f"Details for Recommendation ID: {selected_id}", expanded=True):
                st.markdown(selected_row['recommendation_text'])

except requests.exceptions.RequestException as e:
    st.error(f"Failed to fetch history from the backend: {e}")