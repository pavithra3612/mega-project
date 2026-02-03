import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Insurance Claims Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. DATA LOADING (Uses Caching for Performance) ---
# This function loads either the uploaded file or generates dummy data.
@st.cache_data
def load_data(uploaded_file):
    """Loads data from CSV or generates synthetic data if none is provided."""
    
    # Define required columns for the Insurance dataset
    required_cols = ['age', 'gender', 'bmi', 'children', 'smoker', 'region', 'claim']
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Standardize column names (lower-case for consistency)
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]

            # Check for required columns
            if not all(col in df.columns for col in required_cols):
                 missing_cols = [col for col in required_cols if col not in df.columns]
                 st.error(f"Uploaded CSV must contain all these columns: {', '.join(required_cols)}. Missing: {', '.join(missing_cols)}")
                 return pd.DataFrame() 
            
            # Ensure numeric types
            df['claim'] = pd.to_numeric(df['claim'], errors='coerce')
            df['age'] = pd.to_numeric(df['age'], errors='coerce')
            df.dropna(subset=['claim', 'age'], inplace=True)

            return df
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return pd.DataFrame()
    else:
        # Generate Synthetic Insurance Data for demonstration
        N = 500
        
        data = {
            'age': np.random.randint(18, 65, N),
            'gender': np.random.choice(['male', 'female'], N),
            'bmi': np.random.uniform(18, 45, N).round(1),
            'children': np.random.randint(0, 5, N),
            'smoker': np.random.choice(['yes', 'no'], N, p=[0.2, 0.8]),
            'region': np.random.choice(['northeast', 'southeast', 'southwest', 'northwest'], N),
            'claim': np.random.uniform(1000, 50000, N).round(2),
        }
        
        df = pd.DataFrame(data)
        # Add a major impact of smoking on claims for realistic visualization
        df['claim'] = df.apply(lambda row: row['claim'] * 3.5 if row['smoker'] == 'yes' else row['claim'], axis=1)
        
        st.info("💡 Using synthetic Insurance data. Upload your cleaned CSV file in the sidebar!")
        return df

# --- 3. Sidebar and Data Load Initialization ---
st.sidebar.header("Data Source")
uploaded_file = st.sidebar.file_uploader("Upload your cleaned CSV file here:", type=['csv'])

df = load_data(uploaded_file)

if df.empty:
    st.stop()

# --- 4. Filtering Widgets ---
st.sidebar.header("Filter Data")

# Get unique values for filters
all_regions = df['region'].unique().tolist()
all_smokers = df['smoker'].unique().tolist()
all_genders = df['gender'].unique().tolist()

# Filters
selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=all_regions,
    default=all_regions
)

selected_smokers = st.sidebar.multiselect(
    "Smoker Status",
    options=all_smokers,
    default=all_smokers
)

selected_genders = st.sidebar.multiselect(
    "Select Gender",
    options=all_genders,
    default=all_genders
)

# Apply filters
df_filtered = df[
    df['region'].isin(selected_regions) &
    df['smoker'].isin(selected_smokers) &
    df['gender'].isin(selected_genders)
]

# Stop if no data matches the filters
if df_filtered.empty:
    st.error("No data matches the current filter selection. Please adjust your filters.")
    st.stop()


# --- 5. MAIN PAGE LAYOUT AND VISUALIZATIONS ---

st.title("🏥 Insurance Claims Analysis Dashboard")
st.markdown("### Analyzing the factors affecting claim costs using your cleaned data.")

# Row 1: Key Metrics (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_count = len(df_filtered)
avg_claim = df_filtered['claim'].mean()
smokers_percent = (df_filtered['smoker'] == 'yes').sum() / total_count * 100 if total_count > 0 else 0
avg_age = df_filtered['age'].mean()

col1.metric("Total Records", total_count)
col2.metric("Average Claim Cost", f"${avg_claim:,.0f}")
col3.metric("Avg. Age", f"{avg_age:,.1f} years")
col4.metric("% of Smokers", f"{smokers_percent:,.1f}%")


st.markdown("---")


# Row 2: Claim vs. Age/Smoker & Claim by Region
col_scatter, col_region_bar = st.columns([3, 2])

# Define custom color map for consistency
smoker_color_map = {
    'yes': '#ef4444', # Red for Smoker
    'no': '#10b981',  # Green for Non-Smoker
}

# VIZ 1: Claim vs. Age (Scatter Plot, colored by Smoker)
with col_scatter:
    st.subheader("Claim Cost vs. Age (Colored by Smoker Status)")
    
    fig_scatter = px.scatter(
        df_filtered,
        x="age",
        y="claim",
        color="smoker",
        hover_data=['bmi', 'children', 'region'],
        color_discrete_map=smoker_color_map,
        title="Impact of Smoker Status on Claims Across Ages",
        height=500
    )

    fig_scatter.update_layout(xaxis_title="Age", yaxis_title="Claim Cost ($)")
    st.plotly_chart(fig_scatter, use_container_width=True)


# VIZ 2: Average Claim by Region (Bar Chart)
with col_region_bar:
    st.subheader("Average Claim Cost by Region")
    
    avg_claim_region = df_filtered.groupby('region')['claim'].mean().reset_index(name='Avg_Claim')
    
    fig_region = px.bar(
        avg_claim_region,
        x="region",
        y="Avg_Claim",
        title="Regional Claim Costs",
        height=500,
        color='region', # Automatically assign a color to each region
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_region.update_layout(xaxis_title=None, yaxis_title="Average Claim Cost ($)")
    st.plotly_chart(fig_region, use_container_width=True)


# Row 3: Claim Distribution & Claim by Children
st.markdown("## Distribution and Family Impact")

col_hist, col_children_bar = st.columns([3, 2])

# VIZ 3: Claim Cost Distribution (Histogram)
with col_hist:
    st.subheader("Distribution of Claim Costs")
    
    fig_hist = px.histogram(
        df_filtered,
        x='claim',
        nbins=40,
        title='Frequency of Different Claim Amounts',
        color='smoker',
        color_discrete_map=smoker_color_map,
        height=500,
        opacity=0.7,
        marginal="box" # Adds a box plot on top for better summary
    )
    fig_hist.update_layout(xaxis_title="Claim Cost ($)", yaxis_title="Number of Records")
    st.plotly_chart(fig_hist, use_container_width=True)

# VIZ 4: Average Claim by Children (Bar Chart)
with col_children_bar:
    st.subheader("Average Claim by Number of Dependents")
    
    avg_claim_children = df_filtered.groupby('children')['claim'].mean().reset_index(name='Avg_Claim')
    
    fig_children = px.bar(
        avg_claim_children,
        x="children",
        y="Avg_Claim",
        title="Claim Cost by Dependents (0 to 4+)",
        height=500,
        color='children',
        color_continuous_scale=px.colors.sequential.Teal
    )
    fig_children.update_layout(xaxis_title="Number of Children/Dependents", yaxis_title="Average Claim Cost ($)")
    fig_children.update_traces(marker_color='#2c7be5') # Set a nice blue color
    st.plotly_chart(fig_children, use_container_width=True)


# Row 4: Filtered Data Table
st.markdown("---")
st.markdown("## Filtered Data Table")
st.dataframe(df_filtered, use_container_width=True)