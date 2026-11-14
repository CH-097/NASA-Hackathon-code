import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
from sklearn.preprocessing import MinMaxScaler

# --- Page Configuration ---
st.set_page_config(page_title="Analog Site Selector - Moon/Mars Prototype", layout="wide")
st.title("🚀 Terrestrial Analog Finder for Moon/Mars Bases")
st.markdown("Comparing Earth regional profiles against Martian/Lunar environmental benchmarks.")

# --- 1. Mocking / Loading Dataset (Replace this with real NASA .nc/.tif data later) ---
@st.cache_data
def load_analog_data():
    # Let's create a dummy dataset of potential Earth analog sites (Deserts, Volcanic fields, Dry Valleys)
    data = {
        'site_name': ['Atacama Desert (Core)', 'Death Valley', 'Haughton Crater (Devon Island)', 'McMurdo Dry Valleys', 'Mauna Kea Slopes', 'Rio Tinto Basin'],
        'lat': [-23.8631, 36.5323, 75.3803, -77.8419, 19.8207, 37.6953],
        'lon': [-69.1328, -116.9325, -89.5773, 166.6863, -155.5321, -6.5878],
        'temperature_c': [18.5, 24.0, -15.2, -20.0, 2.0, 16.0],      # Mean annual temp
        'elevation_m': [2400, -86, 50, 100, 4200, 424],              # Elevation
        'slope_deg': [5.2, 1.2, 12.5, 3.1, 28.4, 8.0],               # Surface roughness/slope
        'soil_moisture': [0.01, 0.03, 0.05, 0.02, 0.08, 0.10]        # Volumetric water content
    }
    return pd.DataFrame(data)

df = load_analog_data()

# --- 2. User Controls for Planetary Target ---
st.sidebar.header("Target Environment Profile")
target_choice = st.sidebar.selectbox("Choose Target Body:", ["Lunar Permanently Shadowed Region (PSR)", "Mars Equatorial Region"])

if target_choice == "Lunar Permanently Shadowed Region (PSR)":
    # Extreme cold, zero moisture, high slope variance
    target_vector = np.array([-50.0, 0, 15.0, 0.0]) 
    st.sidebar.info("Target Profile: Temp -50°C | Elev 0m | Slope 15° | Moisture 0%")
else:
    # Cold desert, low pressure/moisture, moderate slope
    target_vector = np.array([-60.0, 1000, 8.0, 0.01])
    st.sidebar.info("Target Profile: Temp -60°C | Elev 1000m | Slope 8° | Moisture 1%")

# --- 3. Machine Learning / Similarity Scoring Engine ---
# Features used for comparison
features = ['temperature_c', 'elevation_m', 'slope_deg', 'soil_moisture']

# Normalize features so large scales (like elevation in meters) don't overpower temperature
scaler = MinMaxScaler()
df_scaled = df.copy()
df_scaled[features] = scaler.fit_transform(df[features])

# Scale target vector using the same scaler bounds
target_scaled = scaler.transform([target_vector])[0]

# Calculate Euclidean Distance similarity (lower distance = higher similarity score 0 to 100%)
distances = np.linalg.norm(df_scaled[features].values - target_scaled, axis=1)
# Convert distance to a similarity percentage
df['similarity_score'] = (1 - (distances / np.max(distances + 1e-6))) * 100

# Sort by best match
df = df.sort_values(by='similarity_score', ascending=False)

# --- 4. Display Findings Table ---
st.subheader("📊 Ranked Analog Sites Match")
st.dataframe(df[['site_name', 'similarity_score', 'temperature_c', 'elevation_m', 'slope_deg', 'soil_moisture']].style.format({"similarity_score": "{:.1f}%"}))

# --- 5. Interactive Web Map Visualisation ---
st.subheader("🗺️ Interactive Analogs Map")
st.markdown("Click on markers to inspect specific site metrics compared to your target.")

# Initialize Folium Map centered around global view
m = folium.Map(location=[20, 0], zoom_start=2)

for _, row in df.iterrows():
    # Color code markers based on similarity
    color = "green" if row['similarity_score'] > 75 else "orange" if row['similarity_score'] > 40 else "red"
    
    popup_html = f"""
    <b>Site:</b> {row['site_name']}<br>
    <b>Similarity Match:</b> {row['similarity_score']:.1f}%<br>
    <b>Temp:</b> {row['temperature_c']}°C<br>
    <b>Elevation:</b> {row['elevation_m']}m<br>
    <b>Soil Moisture:</b> {row['soil_moisture']}<br>
    """
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"{row['site_name']} ({row['similarity_score']:.1f}%)",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# Render map in Streamlit
st_folium(m, width=1000, height=500)