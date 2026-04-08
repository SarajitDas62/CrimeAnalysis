"""
UI_COMPONENTS.PY - UI/UX Styling & Components
Handles all visual elements, styling, and reusable UI components
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# ==================== STYLING ====================
def apply_custom_styling():
    """Apply custom CSS styling to Streamlit app"""
    st.markdown("""
        <style>
            /* Main background and text */
            .main {
                background-color: #f8f9fa;
            }

            /* Metric styling */
            [data-testid="metric-container"] {
                background-color: #ffffff;
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }

            /* Header styling */
            h1 {
                color: #dc3545;
                text-align: center;
                padding: 20px 0;
            }

            h2 {
                color: #343a40;
                border-bottom: 3px solid #dc3545;
                padding-bottom: 10px;
            }

            h3 {
                color: #495057;
                margin-top: 20px;
            }

            /* Button styling */
            .stButton > button {
                background-color: #dc3545;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                border: none;
                font-weight: bold;
            }

            .stButton > button:hover {
                background-color: #c82333;
            }

            /* Sidebar styling */
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }

            /* Dataframe styling */
            .stDataFrame {
                border-radius: 10px;
                overflow: hidden;
            }
        </style>
    """, unsafe_allow_html=True)


def set_page_configuration():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Crime Data Analysis",
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    apply_custom_styling()


# ==================== VISUALIZATION COMPONENTS ====================
def create_bar_chart(data, title, xlabel, ylabel, color='steelblue', kind='bar'):
    """Reusable bar chart component"""
    fig, ax = plt.subplots(figsize=(10, 5))
    if kind == 'bar':
        data.plot(kind='bar', ax=ax, color=color, edgecolor='black', linewidth=0.5)
    else:
        data.plot(kind='barh', ax=ax, color=color, edgecolor='black', linewidth=0.5)

    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    return fig


def create_pie_chart(data, title):
    """Reusable pie chart component"""
    fig, ax = plt.subplots(figsize=(6, 4))
    colors = plt.cm.Set3(range(len(data)))
    data.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_ylabel("")
    ax.set_title(title, fontsize=12, fontweight='bold')
    plt.tight_layout()

    return fig


def create_line_chart(data, title, xlabel, ylabel):
    """Reusable line chart component"""
    fig, ax = plt.subplots(figsize=(10, 5))
    data.plot(ax=ax, color='#dc3545', linewidth=2, marker='o', markersize=5)
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    return fig


def create_scatter_plot(df, lon_col, lat_col, color_col, title, centers=None):
    """Reusable scatter plot for geographic data"""
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(df[lon_col], df[lat_col], c=df[color_col],
                        cmap='tab20', alpha=0.6, s=20, edgecolors='none')

    if centers is not None:
        ax.scatter(centers[:, 1], centers[:, 0], c='red', marker='X',
                  s=300, edgecolors='black', linewidth=2, label='Centers', zorder=5)

    ax.set_xlabel('Longitude', fontsize=11, fontweight='bold')
    ax.set_ylabel('Latitude', fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.legend()
    plt.colorbar(scatter, ax=ax, label='Cluster')
    plt.tight_layout()

    return fig


def create_histogram(data, bins=30, title='', xlabel='', ylabel='Count'):
    """Reusable histogram component"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(data, bins=bins, color='green', edgecolor='black', alpha=0.7)
    ax.set_xlabel(xlabel, fontsize=11, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=11, fontweight='bold')
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    return fig


# ==================== METRIC COMPONENTS ====================
def display_metrics(metrics_dict):
    """Display multiple metrics in a row"""
    cols = st.columns(len(metrics_dict))
    for i, (label, value) in enumerate(metrics_dict.items()):
        with cols[i]:
            st.metric(label, value)


def display_metrics_4col(metric1, value1, metric2, value2, metric3, value3, metric4, value4):
    """Display 4 metrics in a row"""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(metric1, f"{value1:,}" if isinstance(value1, int) else value1)
    with col2:
        st.metric(metric2, f"{value2:,}" if isinstance(value2, int) else value2)
    with col3:
        st.metric(metric3, f"{value3:,}" if isinstance(value3, int) else value3)
    with col4:
        st.metric(metric4, value4)


# ==================== FORM COMPONENTS ====================
def create_data_source_selector():
    """Create data source selection in sidebar"""
    st.markdown("## Configuration")
    data_source = st.radio("Data Source", ["Use Default Dataset", "Upload CSV"])

    if data_source == "Use Default Dataset":
        sample_size = st.slider("Sample size (records)", 10000, 100000, 50000, step=10000)
        return data_source, sample_size, None
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type="csv")
        return data_source, None, uploaded_file


def create_prediction_inputs():
    """Create input fields for crime prediction"""
    col1, col2 = st.columns(2)

    with col1:
        hour = st.slider("Hour of Day", 0, 23, 12)
        lat = st.number_input("Latitude", value=34.0522, format="%.4f")

    with col2:
        lon = st.number_input("Longitude", value=-118.2437, format="%.4f")

    return hour, lat, lon


# ==================== INFO COMPONENTS ====================
def display_dataset_info(df):
    """Display dataset information"""
    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Records:** {len(df):,}")
        st.write(f"**Columns:** {len(df.columns)}")
        st.write(f"**Missing Values:** {df.isnull().sum().sum():,}")

    with col2:
        if 'date_occ' in df.columns:
            st.write(f"**Start Date:** {df['date_occ'].min()}")
            st.write(f"**End Date:** {df['date_occ'].max()}")
        st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")


def display_hotspot_table(clusters, centers):
    """Display hotspot information in table"""
    hotspot_data = pd.DataFrame({
        'Hotspot ID': range(len(centers)),
        'Latitude': centers[:, 0].round(4),
        'Longitude': centers[:, 1].round(4),
        'Crime Count': [sum(clusters == i) for i in range(len(centers))]
    })

    st.dataframe(hotspot_data, use_container_width=True)
    return hotspot_data


# ==================== STATUS COMPONENTS ====================
def show_loading_spinner(message):
    """Show loading spinner"""
    with st.spinner(message):
        return True


def show_success_message(message):
    """Show success message"""
    st.success(message)


def show_error_message(message):
    """Show error message"""
    st.error(message)


def show_info_message(message):
    """Show info message"""
    st.info(message)


def show_warning_message(message):
    """Show warning message"""
    st.warning(message)


# ==================== CHART STYLING ====================
def configure_chart_style():
    """Configure matplotlib and seaborn styling"""
    sns.set_style("darkgrid")
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['figure.figsize'] = (12, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 11
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
