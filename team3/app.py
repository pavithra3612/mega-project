"""
Cost of Living Index Streamlit Application

This application analyzes and visualizes cost of living data by country.
It provides interactive charts and insights into various cost factors
across different countries worldwide.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os

# Page configuration
st.set_page_config(
    page_title="Cost of Living Index by Country",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define cohesive color palette
COLOR_PALETTE = {
    'primary': '#1f77b4',      # Professional blue
    'secondary': '#ff7f0e',    # Warm orange
    'accent1': '#2ca02c',      # Green
    'accent2': '#d62728',      # Red
    'accent3': '#9467bd',      # Purple
    'accent4': '#8c564b',      # Brown
    'accent5': '#e377c2',      # Pink
    'background': '#f0f2f6',   # Light gray background
    'text': '#262730',         # Dark text
}

# Cohesive color scales
COLOR_SCALE_SEQUENTIAL = ['#f0f9ff', '#bae6fd', '#7dd3fc', '#38bdf8', '#0ea5e9', '#0284c7', '#0369a1', '#075985']  # Blues
COLOR_SCALE_DIVERGING = ['#0369a1', '#0284c7', '#0ea5e9', '#f0f9ff', '#fef08a', '#fbbf24', '#f59e0b', '#d97706']  # Blue to Amber
COLOR_SCALE_CATEGORICAL = ['#0ea5e9', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6', '#6366f1']  # Vibrant set

# Apply custom styling
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #e0f2fe 100%);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0c4a6e;
        font-weight: 600;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #0369a1;
        font-size: 2rem;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #475569;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3);
        transform: translateY(-2px);
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        border-radius: 6px;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border-color: #cbd5e1;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Cards effect for columns */
    [data-testid="column"] > div {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("💰 Cost of Living Index by Country")
st.markdown("""
<div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
            padding: 1.5rem; 
            border-radius: 12px; 
            border-left: 4px solid #0ea5e9;
            margin-bottom: 2rem;'>
    <p style='margin: 0; color: #334155; font-size: 1.1rem;'>
    This application provides insights into the cost of living across different countries.
    The data includes various indices such as Cost of Living, Rent, Groceries, Restaurant Prices, and Local Purchasing Power.
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load sample cost of living data"""
    countries = [
        'Switzerland', 'Norway', 'Iceland', 'Denmark', 'Luxembourg',
        'Singapore', 'United States', 'Ireland', 'Netherlands', 'Australia',
        'Germany', 'France', 'United Kingdom', 'Canada', 'Japan',
        'South Korea', 'Spain', 'Italy', 'Portugal', 'Poland',
        'Czech Republic', 'Hungary', 'Mexico', 'Brazil', 'India',
        'Thailand', 'Vietnam', 'Philippines', 'Indonesia', 'Malaysia'
    ]
    
    np.random.seed(42)  # For reproducible results
    
    data = {
        'Country': countries,
        'Cost of Living Index': np.random.uniform(20, 120, len(countries)),
        'Rent Index': np.random.uniform(10, 100, len(countries)),
        'Cost of Living Plus Rent Index': np.random.uniform(20, 110, len(countries)),
        'Groceries Index': np.random.uniform(15, 130, len(countries)),
        'Restaurant Price Index': np.random.uniform(10, 140, len(countries)),
        'Local Purchasing Power Index': np.random.uniform(30, 150, len(countries))
    }
    
    df = pd.DataFrame(data)
    
    # Make data more realistic
    df.loc[df['Country'] == 'Switzerland', 'Cost of Living Index'] = 115.2
    df.loc[df['Country'] == 'Norway', 'Cost of Living Index'] = 108.5
    df.loc[df['Country'] == 'India', 'Cost of Living Index'] = 22.1
    df.loc[df['Country'] == 'Vietnam', 'Cost of Living Index'] = 24.8
    
    return df

# --- NEW: Housing Costs Visualization Section ---
@st.cache_data
def load_housing_costs():
    """Load housing costs dataset from JSON file in data/ directory"""
    try:
        file_path = os.path.join("data", "housing_costs.json")
        with open(file_path) as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.warning(f"Could not load housing costs dataset from {file_path}: {e}")
        return None

def show_housing_costs():
    st.header("💰 Monthly Housing Cost Breakdown")

    data = load_housing_costs()
    if not data:
        st.info("No housing costs data found.")
        return

    categories = data["categories"]
    costs = data["costs"]
    expenses = data["expenses"]

    df_housing = pd.DataFrame({
        "Category": categories,
        "Cost": costs
    })

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("📈 Line Chart")
        fig = px.line(
            df_housing, 
            x="Category", 
            y="Cost", 
            markers=True, 
            title="Monthly Cost by Category"
        )
        fig.update_traces(
            line_color=COLOR_PALETTE['primary'],
            marker=dict(size=10, color=COLOR_PALETTE['secondary'])
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_PALETTE['text']),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("🥧 Pie Chart")
        fig = px.pie(
            df_housing, 
            names="Category", 
            values="Cost", 
            title="Cost Distribution",
            color_discrete_sequence=COLOR_SCALE_CATEGORICAL
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_PALETTE['text']),
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.subheader("📊 Bar Chart")
        fig = px.bar(
            df_housing, 
            x="Category", 
            y="Cost", 
            title="Monthly Cost by Category", 
            color="Category",
            color_discrete_sequence=COLOR_SCALE_CATEGORICAL
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_PALETTE['text']),
            showlegend=False,
            title_font_size=16
        )
        st.plotly_chart(fig, use_container_width=True)

    # Histogram
    st.subheader("📊 Histogram of Monthly Expenses")
    fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
    ax_hist.hist(expenses, bins=10, color=COLOR_PALETTE['primary'], edgecolor=COLOR_PALETTE['text'], alpha=0.7)
    ax_hist.set_xlabel('Expense Amount (USD)', fontsize=12, color=COLOR_PALETTE['text'])
    ax_hist.set_ylabel('Frequency', fontsize=12, color=COLOR_PALETTE['text'])
    ax_hist.tick_params(colors=COLOR_PALETTE['text'])
    ax_hist.spines['top'].set_visible(False)
    ax_hist.spines['right'].set_visible(False)
    ax_hist.spines['left'].set_color(COLOR_PALETTE['text'])
    ax_hist.spines['bottom'].set_color(COLOR_PALETTE['text'])
    fig_hist.patch.set_alpha(0)
    ax_hist.set_facecolor('white')
    plt.tight_layout()
    st.pyplot(fig_hist)

    # Raw Data
    st.subheader("📋 Raw Housing Cost Data")
    st.dataframe(df_housing, use_container_width=True)

def main():
    """Main application function"""
    
    # Load data
    df = load_sample_data()
    
    # Sidebar
    st.sidebar.header("🎛️ Filters and Options")
    
    # Country selection
    selected_countries = st.sidebar.multiselect(
        "Select Countries to Compare:",
        options=df['Country'].tolist(),
        default=df['Country'][:10].tolist(),
        key="country_multiselect"
    )
    
    # Index selection
    index_options = [col for col in df.columns if col != 'Country']
    selected_index = st.sidebar.selectbox(
        "Select Index to Display:",
        options=index_options,
        index=0,
        key="index_select"
    )
    
    # Filter data
    filtered_df = df[df['Country'].isin(selected_countries)]
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Bar chart
        st.subheader(f"📊 {selected_index} by Country")
        fig_bar = px.bar(
            filtered_df.sort_values(selected_index, ascending=False),
            x='Country',
            y=selected_index,
            title=f"{selected_index} Comparison",
            color=selected_index,
            color_continuous_scale=COLOR_SCALE_SEQUENTIAL
        )
        fig_bar.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_PALETTE['text']),
            title_font_size=16
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        if not filtered_df.empty:
            st.metric("Average", f"{filtered_df[selected_index].mean():.1f}")
            st.metric("Highest", f"{filtered_df[selected_index].max():.1f}")
            st.metric("Lowest", f"{filtered_df[selected_index].min():.1f}")
            st.metric("Countries", len(filtered_df))
    
    # World map visualization
    st.subheader("🌍 Global Cost of Living Map")
    fig_map = px.choropleth(
        df,
        locations='Country',
        locationmode='country names',
        color='Cost of Living Index',
        hover_name='Country',
        hover_data={'Cost of Living Index': ':.1f'},
        color_continuous_scale=COLOR_SCALE_SEQUENTIAL,
        title="Cost of Living Index Worldwide"
    )
    fig_map.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_PALETTE['text']),
        title_font_size=16
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Correlation matrix
    st.subheader("🔗 Index Correlations")
    correlation_data = df.select_dtypes(include=[np.number]).corr()
    fig_corr = px.imshow(
        correlation_data,
        title="Correlation Between Different Indices",
        color_continuous_scale=COLOR_SCALE_DIVERGING,
        aspect='auto',
        text_auto='.2f'
    )
    fig_corr.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_PALETTE['text']),
        title_font_size=16
    )
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Data table
    st.subheader("📋 Raw Data")
    st.dataframe(
        filtered_df.sort_values(selected_index, ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Download data
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Complete Dataset",
        data=csv,
        file_name=f"cost_of_living_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
    
    # Show housing costs visualizations
    show_housing_costs()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                padding: 1rem; 
                border-radius: 8px; 
                text-align: center;
                color: #475569;'>
        <p style='margin: 0; font-size: 0.9rem;'>
        <strong>📊 Data Note:</strong> This application uses sample data for demonstration purposes. 
        In a production environment, this would connect to real cost of living data sources 
        such as Numbeo, World Bank, or other economic databases.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
