# 💻 Streamlit App Script – Ironhack Payments Dashboard
# 📓 Source Notebook: 4_streamlit_app_dev.ipynb
# 🌐 Description: Prepares a web-based dashboard using Streamlit to visualize cohort KPIs.
# 📅 Date: December 13, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila
# 🛠️ Bootcamp: Ironhack Data Science and Machine Learning

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

# ✅ Safe print to avoid encoding issues in non-UTF terminals
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="ignore").decode())

# ✅ Detect if running in Google Colab
def is_colab():
    return 'google.colab' in sys.modules

# ✅ Set up the project base path dynamically
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

    # Try your default Google Drive path
    default_path = 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'
    full_default_path = os.path.join('/content/drive', default_path)

    if os.path.exists(full_default_path):
        project_base_path = full_default_path
        safe_print(f"✅ Colab project path set to: {project_base_path}")
    else:
        # Ask user for input if default fails
        safe_print("\n📂 Default path not found. Please input the relative path to your project inside Google Drive.")
        safe_print("👉 Example: 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'")
        user_path = input("📥 Your path: ").strip()
        project_base_path = os.path.join('/content/drive', user_path)

        if not os.path.exists(project_base_path):
            raise FileNotFoundError(f"❌ Path does not exist: {project_base_path}\nPlease check your input.")

        safe_print(f"✅ Colab project path set to: {project_base_path}")
else:
    # Local or .py execution
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    # Assume the script is inside /scripts/ and go two levels up
    project_base_path = os.path.abspath(os.path.join(script_dir, '..', '..'))
    safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")


# In[2]:


import pandas as pd
import os

# ✅ Define paths to data and plot folders
data_path = os.path.join(project_base_path, 'cohort_outputs', 'data')
plots_path = os.path.join(project_base_path, 'cohort_outputs', 'plots')

# ✅ Load cohort-level CSVs
try:
    cohort_usage = pd.read_csv(os.path.join(data_path, 'cohort_usage_matrix.csv'))
    cohort_retention = pd.read_csv(os.path.join(data_path, 'cohort_retention_matrix.csv'), index_col=0)
    cohort_retention_filtered = pd.read_csv(os.path.join(data_path, 'cohort_retention_matrix_filtered.csv'), index_col=0)
    cohort_incidents = pd.read_csv(os.path.join(data_path, 'cohort_incident_rate.csv'))
    cohort_revenue = pd.read_csv(os.path.join(data_path, 'cohort_revenue.csv'))
    cohort_cumulative_revenue = pd.read_csv(os.path.join(data_path, 'cohort_cumulative_revenue.csv'))
    cohort_arpu = pd.read_csv(os.path.join(data_path, 'cohort_arpu.csv'))
    cohort_clv = pd.read_csv(os.path.join(data_path, 'cohort_clv.csv'))

    safe_print("✅ Cohort data files loaded successfully.")
except Exception as e:
    safe_print(f"❌ Error loading data: {e}")

# ✅ Load plot file paths
try:
    plot_usage_heatmap = os.path.join(plots_path, '01_cohort_usage_heatmap.png')
    plot_retention_heatmap = os.path.join(plots_path, '02_cohort_retention_heatmap.png')
    plot_retention_filtered = os.path.join(plots_path, '03_cohort_retention_heatmap_filtered.png')
    plot_retention_curves = os.path.join(plots_path, '04_cohort_retention_curves_selected.png')
    plot_incident_rate = os.path.join(plots_path, '05_cohort_incident_rate.png')
    plot_revenue_bar = os.path.join(plots_path, '06_cohort_revenue_bar.png')
    plot_revenue_cumulative = os.path.join(plots_path, '07_cohort_revenue_cumulative_line.png')
    plot_arpu = os.path.join(plots_path, '08_cohort_arpu_bar.png')
    plot_clv = os.path.join(plots_path, '09_cohort_clv_bar.png')

    safe_print("🖼️ Plot file paths loaded successfully.")
except Exception as e:
    safe_print(f"❌ Error loading plot paths: {e}")


# In[3]:


# ✅ Only import and run Streamlit code outside of Colab
if not is_colab():
    import streamlit as st

    # ✅ Set Streamlit page configuration
    st.set_page_config(
        page_title="Ironhack Payments – Cohort Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # ✅ Main page title and intro
    st.title("📊 Ironhack Payments – Cohort Dashboard")
    st.markdown("Explore cohort-based metrics including usage, retention, revenue, and more.")

    # ✅ Sidebar navigation
    st.sidebar.header("🔍 Explore Metrics")
    selected_section = st.sidebar.radio(
        "Select a section:",
        ["Usage", "Retention", "Revenue & Value"],
        index=0
    )


# In[4]:


# ✅ Only render Streamlit visuals outside Colab
if not is_colab():
    if selected_section == "Usage":
        st.subheader("🧮 Service Usage by Cohort")
        st.image(plot_usage_heatmap, caption="Cohort Service Usage Frequency")

    elif selected_section == "Retention":
        st.subheader("📈 User Retention")
        st.image(plot_retention_filtered, caption="Filtered Retention Heatmap (Full Cohorts Only)")

    elif selected_section == "Revenue & Value":
        st.subheader("💰 Revenue and User Value Metrics")
        st.image(plot_revenue_bar, caption="Monthly Revenue by Cohort")
        st.image(plot_revenue_cumulative, caption="Cumulative Revenue Over Time")
        st.image(plot_arpu, caption="ARPU (Average Revenue Per User) per Cohort")
        st.image(plot_clv, caption="CLV (Customer Lifetime Value) per Cohort")


# In[5]:


# ✅ Only show Streamlit content if not in Colab
if not is_colab():
    if selected_section == "Usage":
        with st.expander("📋 View Cohort Usage Table"):
            st.dataframe(cohort_usage)

    elif selected_section == "Retention":
        with st.expander("📋 View Filtered Retention Matrix"):
            st.dataframe(cohort_retention_filtered)

    elif selected_section == "Revenue & Value":
        with st.expander("📋 View Monthly Revenue by Cohort"):
            st.dataframe(cohort_revenue)

        with st.expander("📋 View Cumulative Revenue by Cohort"):
            st.dataframe(cohort_cumulative_revenue)

        with st.expander("📋 View ARPU per Cohort"):
            st.dataframe(cohort_arpu)

        with st.expander("📋 View CLV per Cohort"):
            st.dataframe(cohort_clv)


# In[6]:


# ✅ Only show download buttons outside Colab
if not is_colab():
    if selected_section == "Usage":
        with st.expander("📋 View Cohort Usage Table"):
            st.dataframe(cohort_usage)
            csv = cohort_usage.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Usage Data", csv, "cohort_usage_matrix.csv", "text/csv")

    elif selected_section == "Retention":
        with st.expander("📋 View Filtered Retention Matrix"):
            st.dataframe(cohort_retention_filtered)
            csv = cohort_retention_filtered.to_csv().encode('utf-8')
            st.download_button("⬇️ Download Retention Matrix", csv, "cohort_retention_matrix_filtered.csv", "text/csv")

    elif selected_section == "Revenue & Value":
        with st.expander("📋 View Monthly Revenue by Cohort"):
            st.dataframe(cohort_revenue)
            csv = cohort_revenue.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Revenue Data", csv, "cohort_revenue.csv", "text/csv")

        with st.expander("📋 View Cumulative Revenue by Cohort"):
            st.dataframe(cohort_cumulative_revenue)
            csv = cohort_cumulative_revenue.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Cumulative Revenue", csv, "cohort_cumulative_revenue.csv", "text/csv")

        with st.expander("📋 View ARPU per Cohort"):
            st.dataframe(cohort_arpu)
            csv = cohort_arpu.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download ARPU Data", csv, "cohort_arpu.csv", "text/csv")

        with st.expander("📋 View CLV per Cohort"):
            st.dataframe(cohort_clv)
            csv = cohort_clv.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CLV Data", csv, "cohort_clv.csv", "text/csv")



# ------------------------------------------------------------------------------
# 🛡️ License & Attribution
#
# © 2024 Ginosca Alejandro Dávila
# Project: Ironhack Payments – Cohort Analysis
# Bootcamp: Ironhack Data Science and Machine Learning
#
# This work is provided for educational purposes under the MIT License.
# You may reuse, modify, or redistribute with attribution.
# ------------------------------------------------------------------------------
