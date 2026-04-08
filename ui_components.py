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
    """Apply custom CSS styling - Premium Dark Theme"""
    st.markdown("""
        <style>
            /* ===== MAIN BACKGROUND ===== */
            body, [data-testid="stAppViewContainer"] {
                background-color: #0E1117;
                color: #E6EDF3;
            }

            [data-testid="stMain"] {
                background-color: #0E1117;
            }

            /* ===== SIDEBAR ===== */
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #010409 0%, #0D1117 100%);
                border-right: 1px solid #30363d;
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
                color: #E6EDF3;
            }

            /* ===== HEADERS ===== */
            h1 {
                color: #58A6FF;
                text-align: center;
                padding: 30px 0 10px 0;
                font-size: 3em;
                font-weight: 900;
                letter-spacing: 2px;
                animation: fadeIn 0.8s ease;
            }

            h2 {
                color: #79C0FF;
                border-left: 4px solid #58A6FF;
                padding-left: 15px;
                margin: 25px 0 15px 0;
                font-weight: 700;
                animation: slideInLeft 0.6s ease;
            }

            h3 {
                color: #A5D6FF;
                margin-top: 20px;
                font-weight: 600;
            }

            p {
                color: #C9D1D9;
            }

            /* ===== ANIMATIONS ===== */
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            @keyframes slideInLeft {
                from {
                    opacity: 0;
                    transform: translateX(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }

            @keyframes slideInUp {
                from {
                    opacity: 0;
                    transform: translateY(30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            /* ===== KPI CARDS ===== */
            [data-testid="metric-container"] {
                background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
                transition: all 0.3s ease;
                animation: slideInUp 0.6s ease;
            }

            [data-testid="metric-container"]:hover {
                border-color: #58A6FF;
                box-shadow: 0 0 20px rgba(88, 166, 255, 0.15);
                transform: translateY(-5px);
            }

            [data-testid="metric-container"] label {
                color: #8B949E;
                font-weight: 600;
            }

            [data-testid="metric-container"] > div > div > div {
                color: #58A6FF;
                font-size: 2.5em;
                font-weight: 900;
            }

            /* ===== BUTTONS ===== */
            .stButton > button {
                background: linear-gradient(135deg, #238636 0%, #1f6feb 100%);
                color: white;
                border: 1px solid #238636;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 700;
                font-size: 15px;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 12px rgba(88, 166, 255, 0.15);
                animation: fadeIn 0.5s ease;
            }

            .stButton > button:hover {
                background: linear-gradient(135deg, #2ea043 0%, #2679e9 100%);
                border-color: #58A6FF;
                box-shadow: 0 8px 20px rgba(88, 166, 255, 0.25);
                transform: translateY(-2px);
            }

            /* ===== INPUT FIELDS ===== */
            .stTextInput > div > div > input,
            .stNumberInput > div > div > input,
            .stSelectbox > div > div > select {
                background-color: #0D1117 !important;
                border: 1px solid #30363d !important;
                color: #E6EDF3 !important;
                border-radius: 8px !important;
                padding: 12px !important;
                transition: all 0.3s ease !important;
            }

            .stTextInput > div > div > input:focus,
            .stNumberInput > div > div > input:focus,
            .stSelectbox > div > div > select:focus {
                border-color: #58A6FF !important;
                box-shadow: 0 0 12px rgba(88, 166, 255, 0.2) !important;
            }

            /* ===== TABS ===== */
            [data-testid="stTabs"] [role="tablist"] {
                border-bottom: 1px solid #30363d;
                gap: 10px;
            }

            [data-testid="stTabs"] [role="tablist"] button {
                background: transparent;
                color: #8B949E;
                border: none;
                border-bottom: 3px solid transparent;
                padding: 12px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
            }

            [data-testid="stTabs"] [role="tablist"] button:hover {
                color: #58A6FF;
                border-bottom-color: #58A6FF;
            }

            [data-testid="stTabs"] [role="tablist"] button[aria-selected="true"] {
                color: #58A6FF;
                border-bottom-color: #1f6feb;
            }

            /* ===== DIVIDERS ===== */
            hr {
                border: none;
                height: 1px;
                background: linear-gradient(90deg, transparent, #30363d, transparent);
                margin: 25px 0;
            }

            /* ===== ALERTS ===== */
            [data-testid="stAlert"] {
                border-radius: 8px;
                border-left: 4px solid transparent;
                padding: 15px 20px;
                animation: slideInUp 0.5s ease;
            }

            /* ===== SLIDERS ===== */
            .stSlider > div > div > div > div {
                background: linear-gradient(90deg, #238636 0%, #1f6feb 100%);
                border-radius: 10px;
            }

            .stSlider > div > div > div {
                color: #8B949E;
            }

            /* ===== RADIO BUTTONS ===== */
            [data-testid="stRadio"] label {
                color: #E6EDF3;
                font-weight: 500;
                cursor: pointer;
            }

            /* ===== DATAFRAME ===== */
            [data-testid="stDataFrame"] {
                border-radius: 8px;
                overflow: hidden;
                border: 1px solid #30363d;
            }

            /* ===== FILE UPLOADER ===== */
            [data-testid="stFileUploaderDropzone"] {
                border: 2px dashed #30363d;
                border-radius: 8px;
                padding: 30px;
                background: rgba(88, 166, 255, 0.05);
                transition: all 0.3s ease;
            }

            [data-testid="stFileUploaderDropzone"]:hover {
                border-color: #58A6FF;
                background: rgba(88, 166, 255, 0.1);
                box-shadow: 0 0 20px rgba(88, 166, 255, 0.1);
            }

            /* ===== CONTAINER ===== */
            .stContainer {
                background: transparent;
            }

            /* ===== CUSTOM CLASSES ===== */
            .header-container {
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(180deg, rgba(31, 111, 235, 0.05) 0%, transparent 100%);
                border-bottom: 1px solid #30363d;
                margin-bottom: 30px;
                border-radius: 12px;
            }

            .subtitle {
                color: #8B949E;
                font-size: 1.1em;
                margin-top: 10px;
            }

            .kpi-section {
                margin: 30px 0;
            }

            .section-title {
                color: #58A6FF;
                font-size: 1.5em;
                font-weight: 700;
                margin: 30px 0 20px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid #30363d;
            }

            .footer {
                text-align: center;
                padding: 30px;
                margin-top: 50px;
                border-top: 1px solid #30363d;
                color: #8B949E;
                font-size: 0.95em;
            }

            .premium-card {
                background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
                border: 1px solid #30363d;
                border-radius: 12px;
                padding: 20px;
                margin: 15px 0;
                transition: all 0.3s ease;
            }

            .premium-card:hover {
                border-color: #58A6FF;
                box-shadow: 0 0 20px rgba(88, 166, 255, 0.1);
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
    """Display 4 metrics in a row with animations"""
    col1, col2, col3, col4 = st.columns(4)

    metrics_data = [
        (col1, metric1, value1),
        (col2, metric2, value2),
        (col3, metric3, value3),
        (col4, metric4, value4)
    ]

    for col, label, value in metrics_data:
        with col:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
                border: 2px solid rgba(255,255,255,0.1);
                transition: all 0.3s ease;
                animation: slideInUp 0.6s ease;
            " onmouseover="this.style.transform='translateY(-10px)'; this.style.boxShadow='0 12px 40px rgba(102, 126, 234, 0.4)';"
              onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 32px rgba(102, 126, 234, 0.2)';">
                <h3 style="margin: 0 0 10px 0; font-size: 1.2em; font-weight: 600;">{label}</h3>
                <p style="margin: 0; font-size: 2em; font-weight: 900;">
                    {f'{value:,}' if isinstance(value, int) else value}
                </p>
            </div>
            """, unsafe_allow_html=True)


# ==================== FORM COMPONENTS ====================
def create_data_source_selector():
    """Create data source selection in sidebar"""
    st.markdown("## Configuration")
    data_source = st.radio("Data Source", ["Use Default Dataset", "Upload CSV"])

    if data_source == "Use Default Dataset":
        sample_size = st.slider("Sample size (records)", 10000, 100000, 50000, step=10000)
        return data_source, sample_size, None
    else:
        st.markdown("---")
        st.markdown("### 📤 Upload Your Crime Dataset")
        st.markdown("""
        **Supported Format:** CSV (.csv)
        **Maximum File Size:** 300 MB
        """)

        uploaded_file = st.file_uploader(
            "Drag & Drop or Click to Select CSV File",
            type="csv",
            accept_multiple_files=False,
            help="Upload a crime dataset CSV file (max 300MB). The app will automatically process and analyze your data."
        )

        if uploaded_file is not None:
            st.success(f"✅ File selected: {uploaded_file.name} ({uploaded_file.size / (1024**2):.2f} MB)")

        st.markdown("---")
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
    """Show success message with animation"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.3);
        margin: 10px 0;
        animation: slideInUp 0.5s ease;
        font-weight: 500;
    ">
        ✅ {message}
    </div>
    """, unsafe_allow_html=True)


def show_error_message(message):
    """Show error message with animation"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
        margin: 10px 0;
        animation: slideInUp 0.5s ease;
        font-weight: 500;
    ">
        ❌ {message}
    </div>
    """, unsafe_allow_html=True)


def show_info_message(message):
    """Show info message with animation"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        margin: 10px 0;
        animation: slideInUp 0.5s ease;
        font-weight: 500;
    ">
        ℹ️ {message}
    </div>
    """, unsafe_allow_html=True)


def show_warning_message(message):
    """Show warning message with animation"""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(250, 112, 154, 0.3);
        margin: 10px 0;
        animation: slideInUp 0.5s ease;
        font-weight: 500;
    ">
        ⚠️ {message}
    </div>
    """, unsafe_allow_html=True)


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
