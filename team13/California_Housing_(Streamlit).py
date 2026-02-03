import streamlit as st
import pandas as pd

st.title("California Housing Prices")

# Load datasets
data_updated = pd.read_csv('california_housing_updated.csv')
data_1990 = pd.read_csv('california_housing_1990.csv')

# Display number of entries before cleaning
st.write(f"Number of entries in 1990 dataset: {len(data_1990)}")
st.write(f"Number of entries in updated dataset: {len(data_updated)}")

# Show summary of data
st.subheader("Summary – 1990 Dataset")
st.write(data_1990.describe(include='all'))

st.subheader("Summary – Updated Dataset")
st.write(data_updated.describe(include='all'))

# Remove entries with missing data
data_updated = data_updated.dropna()
data_1990 = data_1990.dropna()

# Remove rows with -666666666
rows_to_delete = (data_updated.iloc[:, 1:10] == -666666666).any(axis=1)
if rows_to_delete.any():
    data_updated = data_updated[~rows_to_delete]

# Replace "ISLAND" with "NEAR OCEAN" in ocean_proximity column (1990 dataset)
if 'ocean_proximity' in data_1990.columns:
    data_1990['ocean_proximity'] = data_1990['ocean_proximity'].replace("ISLAND", "NEAR OCEAN")

# Display number of entries after cleaning
st.write(f"Number of entries in cleaned 1990 dataset: {len(data_1990)}")
st.write(f"Number of entries in cleaned updated dataset: {len(data_updated)}")

# Show new summary
st.subheader("Cleaned Summary – 1990 Dataset")
st.write(data_1990.describe(include='all'))

st.subheader("Cleaned Summary – Updated Dataset")
st.write(data_updated.describe(include='all'))

# Write cleaned data sets
data_updated.to_csv('cleaned_california_housing_updated.csv', index=False)
data_1990.to_csv('cleaned_california_housing_1990.csv', index=False)

st.success("Cleaned data files saved successfully!")
