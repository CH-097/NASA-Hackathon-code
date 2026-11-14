# Meriem Harrat
# Test run



# 1 - Download MERRA-2 monthly data via API for 2022 and open as xarray dataset:
import earthaccess, xarray as xr

earthaccess.login()   # prompts once, can persist credentials

results = earthaccess.search_data(
    short_name="M2TMNXSLV",
    temporal=("2022-01-01", "2022-12-31"),
)
files = earthaccess.download(results, "./data/merra2")

ds = xr.open_mfdataset(files)      # 12 monthly files -> one dataset
print(ds)                          # inspect variables, dims, units



# 2 - Build features per Earth grid cell

import numpy as np, pandas as pd

T = ds["T2M"]            # Kelvin
P = ds["PS"]             # Pascals

feat = xr.Dataset({
    "temp_mean":  T.mean("time"),
    "temp_range": T.max("time") - T.min("time"),   # seasonal swing
    "pressure":   P.mean("time"),
})
df = feat.to_dataframe().reset_index()   # columns: lat, lon, temp_mean, ...


# 3 - Save to CSV for later use in ML model

MARS = {"temp_mean": 210, "temp_range": 60, "pressure": 700}    # PLACEHOLDERS: replace with REMS-derived values


# 4 -  Compute similarity to Mars using weighted Euclidean distance
from sklearn.preprocessing import StandardScaler

cols = ["temp_mean", "temp_range", "pressure"]
weights = np.array([1.0, 1.0, 0.3])          # downweight pressure since it never matches

scaler = StandardScaler().fit(df[cols])
X = scaler.transform(df[cols])
target = scaler.transform(pd.DataFrame([MARS])[cols])

dist = np.sqrt((((X - target) * weights) ** 2).sum(axis=1))
df["mars_similarity"] = np.exp(-dist)        # 0..1, higher = closer
df.to_csv("earth_vs_mars.csv", index=False)


# 5 - Visualize Earth grid cells with similarity to Mars using Streamlit and PyDeck
import streamlit as st, pandas as pd, pydeck as pdk

df = pd.read_csv("earth_vs_mars.csv")
thr = st.slider("Minimum similarity", 0.0, 1.0, 0.7)
top = df[df.mars_similarity >= thr]

st.pydeck_chart(pdk.Deck(
    layers=[pdk.Layer("ScatterplotLayer", top,
            get_position="[lon, lat]",
            get_radius=40000,
            get_fill_color="[255, 100 + 100*(1-mars_similarity), 50, 160]",
            pickable=True)],
    initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1),
    tooltip={"text": "Similarity: {mars_similarity}\nMean T: {temp_mean} K"},
))
st.dataframe(top.sort_values("mars_similarity", ascending=False).head(20))


# 6 - streamlit run app.py