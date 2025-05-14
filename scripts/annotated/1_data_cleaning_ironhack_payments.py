# 🧼 Data Cleaning Script – Ironhack Payments
# 📓 Source Notebook: 1_data_cleaning_ironhack_payments.ipynb
# 🧠 Description: Loads, inspects, and cleans raw cash request and fee datasets.
# 📅 Date: December 13, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila
# 🛠️ Bootcamp: Ironhack Data Science and Machine Learning

#!/usr/bin/env python
# coding: utf-8

# # 🧼 **Data Cleaning for Cohort Analysis of Ironhack Payments Users**
# ### **Ironhack Data Science and Machine Learning Bootcamp**
# 📅 **Date:** December 12, 2024  
# 📅 **Submission Date:** December 13, 2024  
# 👩‍💻 **Author:** Ginosca Alejandro Dávila  
# 
# ---
# 
# ## **📌 Project Overview**
# This project presents a **cohort analysis** of Ironhack Payments users, using real user-level data provided by the company.  
# The main goal is to track **user behavior and business performance over time**, segmented by the month of a user’s **first cash request**.
# 
# Key metrics analyzed across cohorts include:
# - 📈 **Frequency of Service Usage**
# - ⚠️ **Incident Rate** (failed payments, postponements, etc.)
# - 💰 **Revenue Generated**
# - 🧠 **Additional User Behavior Metric** (custom, insightful)
# 
# This analysis enables Ironhack Payments to **understand user trends**, optimize engagement, and make data-informed decisions about their financial services.
# 
# 📓 **This notebook** focuses specifically on the **data preparation phase**:
# - Data loading
# - Context understanding
# - Cleaning, validation, and standardization  
# - Exporting cleaned datasets for use in subsequent notebooks
# 
# ---
# 
# ## **📂 Dataset Description**
# 
# 📁 **Lexique - Data Analyst.xlsx**  
# Contextual file describing fields in the main datasets:
# - **Sheet 1 – context - fees:** Definitions of fee types (e.g. incident, postpone), statuses, charge moments, and incident reasons.
# - **Sheet 2 – context - cash request:** Definitions of cash request lifecycle statuses (e.g. approved, rejected, active), user actions, and reimbursement info.
# 
# 📁 **extract - cash request - data analyst.csv**  
# - Contains one row per cash request, including creation date, amount, status, user ID, reimbursement date, and recovery info.
# 
# 📁 **extract - fees - data analyst - .csv**  
# - Contains one row per fee applied to a cash request. Includes type, status, creation/payment timestamps, and total amount charged.
# 
# All datasets are located in:  
# `/project_datasets/` within the project folder.
# 
# ---
# 
# ## **🎯 Goals**
# ✔ Perform a **thorough data cleaning process** to ensure datasets are analysis-ready
# 
# ✔ Conduct an in-depth **Exploratory Data Analysis (EDA)** to understand trends and distributions
# 
# ✔ Conduct a **cohort analysis** based on the month of the user's **first cash request**.  
# 
# ✔ Track and visualize **key metrics per cohort** to derive actionable insights.  
# 
# ✔ Deliver clean and reproducible **Python code**, a **Tableau dashboard**, and a **concise presentation**.  
# 
# ✔ Optionally, **operationalize** the analysis and build a **Streamlit dashboard**.
# 
# ---
# 
# ## **💾 Project Structure**
# 
# 📂 `project-1-ironhack-payments-2-en/` → Project root folder  
# ├── 📂 `project_datasets
# /` → Provided raw `.csv` and `.xlsx` files for analysis  
# ├── 📂 `cleaned_project_datasets/` → Cleaned and validated datasets exported from notebook 1 (`.csv`)  
# ├── 📂 `eda_outputs/` → Outputs generated during exploratory data analysis  
# │   ├── 📂 `data/` → Aggregated tables and cohort-ready `.csv` files for later analysis  
# │   └── 📂 `plots/` → Static `.png` visualizations generated from EDA  
# ├── 📂 `notebooks/` → Development notebooks for each phase of the project  
# │   ├── 📓 `1_data_cleaning_ironhack_payments.ipynb` → Data loading, cleaning, validation, and export  
# │   ├── 📓 `2_eda_ironhack_payments.ipynb` → Exploratory Data Analysis and cohort setup  
# │   ├── 📓 `3_cohort_analysis_metrics.ipynb` → Calculation of cohort-based metrics (frequency, incidents, revenue, retention)  
# │   ├── 📓 `4_streamlit_app_dev.ipynb` → Streamlit dashboard development (final deliverable interface)  
# │   ├── 📓 `export_ironhack_payments_notebooks_to_py.ipynb` → Automation tool to export `.ipynb` notebooks to `.py` scripts  
# │   └── 📓 `test_clean_scripts_colab.ipynb` → Execution test of all four main project scripts (`.py`) to ensure Colab compatibility  
# ├── 📂 `scripts/` → Operational `.py` versions of notebooks, auto-exported for reuse  
# │   ├── 📂 `annotated/` → Scripts with markdown headers and comments for code review and readability  
# │   └── 📂 `clean/` → Stripped-down production scripts without markdown for lean execution  
# ├── 📂 `reports/` → Data quality reports, EDA summaries, and final presentation files (`.md`, `.pdf`, slides)  
# ├── 📂 `dashboard/` → Tableau dashboard `.twbx` file and Streamlit deployment files (if applicable)
# 
# 
# 
# 
# 
# 
# ---
# 
# 🔍 **Let’s dive into the data!**
# 

# ---
# 
# ## 📑 Full Dataset Context from `Lexique - Data Analyst.xlsx`
# 
# This lexique provides the definitions and descriptions for the columns used in the two main datasets: **fees** and **cash request**.
# 
# ---
# 
# ### 🗂️ `cash request` dataset (`extract - cash request - data analyst.csv`)
# 
# **Column name** | **Description**
# --- | ---
# `id` | Unique ID of Cash Request
# `amount` | Amount of the Cash Request
# `status` | Status of the CR.<br><br>- approved : CR is a 'regular' one (= without fees) and was approved either automatically or manually. Funds will be sent aprox. 7 days after the creation<br>- money_sent : We transferred the fund to the customer account. Will change to active once we detect that the user received the funds (using user's bank history)<br>- rejected : The CR needed a manual review and was rejected<br>- pending : The CR is pending a manual review from an analyst<br>- transaction_declined : We failed to send the funds to the customer<br>- waiting_user_confirmation : The user needs to confirm in-app that he want the CR (for legal reasons)<br>- direct_debit_rejected : Our last attempt of SEPA direct debit to charge the customer was rejected<br>- canceled : The user didn't confirm the cash request in-app, we automatically canceled it<br>- direct_debit_sent : We sent/scheduled a SEPA direct debit to charge the customer account. The result of this debit is not yet confirmed<br>- waiting_reimbursement : We were not able to estimate a date of reimbursement, the user needs to choose one in the app.<br>- active : Funds were received on the customer account.<br>- money_back : The CR was successfully reimbursed.
# `reason` | Filled only if the CR was manually reviewed and rejected. That's the rejection's reason displayed in-app.
# `created_at` | Timestamp of the CR creation
# `updated_at` | Timestamp of the latest CR's details update (= update of at least one column in this table)
# `user_id` | Unique ID of the user who requested the cash advance
# `moderated_at` | Timestamp of the manual review. Only filled if the CR needed a manual review
# `deleted_account_id` | If a user delete his account, we are replacing the user_id by this id. It corresponds to a unique ID in the deleted account table with some keys information saved for fraud-fighting purposes (while respecting GDPR regulation)
# `reimbursement_date` | Planned reimbursement date. The user card will be charged at this date.
# `cash_request_debited_date` | Filled only if a SEPA direct debit was sent. It's the date were the latest direct debit was seen on the user account.
# `cash_request_received_date` | Date of the receipt of the CR. Based on user's bank history.
# `money_back_date` | Date where the CR was considered as money back. It's either the paid_by_card date or the date were we considered that's the direc debit have low odds to be rejected (based on business rules)
# `transfer_type` | <br>- instant : user choose not received the advance instantly. <br>- regular : user choose to not pay and wait for the transfer
# `send_at` | Timestamp of the funds's transfer
# `recovery_status` | Null if the cash request never had a payment incident.<br><br>- completed : the payment incident was resolved (=the cash request was reimbursed)<br>- pending : the payment incident still open<br>- pending_direct_debit : the payment incident still open but a SEPA direct debit is launched
# `reco_creation` | Timestamp of the recovery creation
# `reco_last_update` | Timestamp of the last recovery case update. Can be used to determine the incident closure date.
# 
# ---
# 
# ### 🗂️ `fees` dataset (`extract - fees - data analyst - .csv`)
# 
# **Column name** | **Description**
# --- | ---
# `id` | Unique ID of the fee object
# `type` | Type of fee<br><br>- instant_payment : fees for instant cash request (send directly after user's request, through SEPA Instant Payment)<br>- split_payment : futures fees for split payment (in case of an incident, we'll soon offer the possibility to our users to reimburse in multiples installements)<br>- incident : fees for failed reimbursement. Created after a failed direct debit<br>- postpone : fees created when a user want to postpone the reimbursment of a CR
# `status` | Status of the fees (= does the fees was successfully charged)<br><br>- confirmed : the user made an action who created a fee. It will normally get charged at the moment of the CR's reimbursement. In some rare cases, postpones are confirmed without being charges due to a commercial offer.<br>- rejected : the last attempt to charge the fee failed.<br>- cancelled : fee was created and cancelled for some reasons. It's used to fix issues with fees but it mainly concern postpone fees who failed. We are charging the fees at the moment of the postpone request. If it failed, the postpone is not accepted and the reimbursement date still the same.<br>- accepted : fees were successfully charged
# `category` | Describe the reason of the incident fee.<br><br>- rejected_direct_debit : fees created when user's bank rejects the first direct debit<br>- month_delay_on_payment : fees created every month until the incident is closed
# `reason` | Description of the fee
# `created_at` | Timestamp of the fee's creation
# `updated_at` | Timestamp of the latest fee's details update
# `paid_at` | Timestamp of the fee's payment
# `from_date` | Apply only to postpone fees. Initial date of reimbursement for the CR
# `to_date` | Apply only to postpone fees. New date of reimbursement for the CR
# `cash_request_id` | Unique ID of the CR linked to this fee
# `total_amount` | Amount of the fee (including VAT)
# `charge_moment` | When the fee will be charge.<br><br>- before : the fee should be charged at the moment of its creation<br>- after : the fee should be charged at the moment of the CR's reimbursement
# 
# ---
# 

# ---
# 
# ## 🏦 What Does Ironhack Payments Do?
# 
# Ironhack Payments is a **financial services company** offering **cash advances** to users through a digital platform. Since 2020, their mission has been to provide **transparent**, **accessible**, and **flexible** short-term financing solutions.
# 
# Their key product is the **cash request** (CR) — a quick cash advance that users can apply for and receive, often within the same day.
# 
# The business emphasizes:
# - 💡 **Free or low-cost money advancements**
# - ⚡ **Instant fund transfers** (via SEPA Instant Payment)
# - 🔁 **Flexible repayment options**
# - 📊 **Transparent and trackable fees**
# 
# ---
# 
# ## ⚙️ How the Business Likely Works
# 
# ### 1. 🧾 Cash Request Process
# - Users submit a **cash request (CR)** via the app or platform.
# - They can choose between:
#   - `Regular` transfer: free, takes ~7 days
#   - `Instant` transfer: incurs an **instant_payment fee**
# - Each request is timestamped (`created_at`) and linked to a `user_id`.
# 
# ### 2. 💳 Reimbursement
# - A **reimbursement date** is scheduled for each CR.
# - On this date, the user’s bank account is charged via **SEPA direct debit**.
# - If this debit is successful, the CR is marked as `money_back`.
# 
# ### 3. 🧠 What If Something Goes Wrong?
# 
# #### 📌 Payment Incidents
# If the user's bank **rejects the debit**:
# - An **incident fee** is triggered (`type = incident`)
# - Statuses like `recovery_status` or `direct_debit_rejected` track recovery progress
# - Monthly incident fees may continue until resolved
# 
# #### 📌 Postpone Requests
# Users can request to **postpone** their reimbursement date:
# - This creates a `postpone` fee
# - Involves `from_date` and `to_date` fields to track the extension
# 
# #### 📌 Split Payments *(Coming Soon)*
# - Future option for users to **repay in installments**
# - Will incur `split_payment` fees
# 
# ---
# 
# ### 4. 💰 Fee Types and Business Revenue
# 
# Unlike traditional lenders, **Ironhack Payments does not charge interest** on cash advances.  
# There is no APR, no rate-based accrual, and no interest tied to loan duration or risk level.
# 
# Instead, Ironhack Payments earns revenue from **fees** attached to specific user actions:
# 
# | Fee Type         | Description |
# |------------------|-------------|
# | `instant_payment`| For users who want their funds transferred instantly |
# | `postpone`       | For users who delay their reimbursement date |
# | `incident`       | For users whose payment attempt failed (e.g., rejected direct debit) |
# | `split_payment`  | (Upcoming) For users opting to repay in installments after an incident |
# 
# These fees are recorded in the **`fees` dataset**, and each has key attributes:
# - `type`: The type of fee applied
# - `status`: Indicates the collection result  
#   - `confirmed`: fee was created and expected to be charged  
#   - `accepted`: fee was successfully charged  
#   - `rejected` or `cancelled`: fee was not collected
# - `total_amount`: The full fee amount charged to the user (includes VAT)
# 
# All revenue is generated through these fees — not through interest — which aligns with Ironhack Payments' commitment to **"free and transparent pricing"** as stated in the project brief.
# 
# ---
# 
# 📎 Understanding these business mechanics is essential for analyzing:
# - 📈 User behavior and engagement
# - ⚠️ Risk patterns across user cohorts
# - 💵 Revenue performance over time
# 
# 
# 

# ---
# 
# ## 📂 Step 1: Mounting Google Drive
# 
# Since our datasets are stored in Google Drive, the first step is to mount Google Drive into this notebook. This allows us to access the project files located in:
# 
# `My Drive > Colab Notebooks > Ironhack > Week 2 > Week 2 - Day 4 > project-1-ironhack-payments-2-en > project_datasets`
# 
# We will mount the drive and navigate through the folders to load our datasets in the next step.
# 
# ---
# 

# In[1]:


import sys
import os

# ✅ Define safe_print to avoid crashing in some terminals due to emojis
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', errors='ignore').decode())

# ✅ Function to check if running in Google Colab
def is_colab():
    return 'google.colab' in sys.modules

# 🔧 Set up project_base_path depending on environment (Colab or local)
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

    # ✅ Try default path first
    default_path = 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'
    full_default_path = os.path.join('/content/drive', default_path)

    if os.path.exists(full_default_path):
        project_base_path = full_default_path
        safe_print(f"✅ Colab project path set to: {project_base_path}")
    else:
        # 💬 Prompt user if default path not found
        safe_print("\n📂 Default path not found. Please input the relative path to your project inside Google Drive.")
        safe_print("👉 Example: 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'")
        user_path = input("📥 Your path: ").strip()
        project_base_path = os.path.join('/content/drive', user_path)

        if not os.path.exists(project_base_path):
            raise FileNotFoundError(f"❌ Path does not exist: {project_base_path}\nPlease check your input.")

        safe_print(f"✅ Colab project path set to: {project_base_path}")
else:
    try:
        # Get the absolute path of the current script (for .py execution)
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # Fallback for Jupyter/Colab where __file__ is undefined
        script_dir = os.getcwd()

    # ⬆️ Go two levels up from /scripts/clean to reach the project root
    project_base_path = os.path.abspath(os.path.join(script_dir, '..', '..'))
    safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")


# ---
# 
# ## 📥 Step 2: Importing Libraries and Loading Datasets
# 
# We begin by importing the essential libraries for data analysis and loading the two primary datasets provided by Ironhack Payments:
# 
# - `cash_df`: Contains all cash request records.
# - `fees_df`: Contains all associated fees linked to each cash request.
# 
# These datasets will be used throughout the exploratory analysis and cohort analysis process.
# 
# ---
# 

# In[2]:


# 📦 Import required libraries
import pandas as pd
import numpy as np
import os

# 📁 Define file paths using the unified base path
cash_request_path = os.path.join(project_base_path, 'project_datasets', 'extract - cash request - data analyst.csv')
fees_path = os.path.join(project_base_path, 'project_datasets', 'extract - fees - data analyst - .csv')

# 🔍 Debug: Show full paths being used (use safe_print for emoji compatibility)
safe_print(f"📄 Looking for: {cash_request_path}")
safe_print(f"📄 Looking for: {fees_path}")

# 📥 Load datasets into pandas DataFrames
try:
    cash_df = pd.read_csv(cash_request_path)
    fees_df = pd.read_csv(fees_path)
    safe_print("✅ Datasets loaded successfully.")
except FileNotFoundError as e:
    # 🛑 Handle missing files gracefully
    safe_print("❌ File not found.")
    safe_print(f"🔎 Tried: {cash_request_path}")
    safe_print(f"🔎 Tried: {fees_path}")
    safe_print("📌 Make sure the file names and directories are spelled correctly.")
    raise e


# ---
# 
# ## 🔍 Step 3: Basic Structure & Overview
# 
# Before diving into exploratory analysis, we begin by inspecting the basic structure of each dataset. This step helps us understand the format, size, and content of the data.
# 
# We will review:
# - First and last rows
# - Shape (number of rows and columns)
# - Column names
# - Data types and non-null counts
# 
# ---
# 

# In[3]:


import io

# ✅ Define display fallback for script environments
try:
    display
except NameError:
    def display(x):
        print(x.to_string() if isinstance(x, pd.DataFrame) else x)

# 🔍 Inspect basic structure of a DataFrame with optional row previews
def inspect_basic_structure(df, name="Dataset", preview_rows=5):
    """
    Display structure, sample rows, and schema of a DataFrame.
    Compatible with both notebooks and terminal scripts.
    """
    safe_print(f"🧾 Inspecting: {name}")
    safe_print("=" * 60)

    # 👁️ Preview first N rows
    safe_print(f"🔹 First {preview_rows} Rows:")
    display(df.head(preview_rows))

    # 👁️ Preview last N rows
    safe_print(f"\n🔹 Last {preview_rows} Rows:")
    display(df.tail(preview_rows))

    # 📐 Dataset shape
    safe_print(f"\n🔹 Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    # 🏷️ Column names
    safe_print("\n🔹 Column Names:")
    safe_print(df.columns.tolist())

    # 🧬 Data types and non-null counts
    safe_print("\n🔹 Data Types and Non-Null Counts:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    safe_print(buffer.getvalue())

    safe_print("=" * 60 + "\n")


# In[4]:


# 🧪 Inspect structure and content of the cash_df DataFrame
inspect_basic_structure(cash_df, name="Cash Requests", preview_rows=5)


# In[5]:


# 🧪 Inspect structure and content of the fees_df DataFrame
inspect_basic_structure(fees_df, name="Fees", preview_rows=5)


# ---
# 
# ## ✅ Step 3 Summary: Dataset Structure
# 
# After inspecting both datasets, we now have a clearer understanding of their structure:
# 
# - `cash_df` contains **23,970 rows × 16 columns**, with key information on each cash request, such as status, reimbursement dates, and user identifiers.
# - `fees_df` contains **21,061 rows × 13 columns**, detailing the types, statuses, and amounts of fees linked to cash requests.
# 
# This structural overview helps us prepare for the next steps:
# - Identifying **quantitative** vs **categorical** variables
# - Converting relevant fields (like dates) to the appropriate formats
# - Beginning our **data cleaning and exploratory analysis**
# 
# ---
# 

# ---
# 
# ## 🧩 Step 4: Initial Variable Exploration
# 
# Before assigning variable types (quantitative, categorical, or datetime), we first explore:
# 
# - The number of **unique values** in each column
# - A preview of those **unique values**
# 
# This helps us identify columns that:
# - Are numeric but act as **identifiers or categories**
# - Are objects but contain **structured dates or codes**
# - Should be reclassified before analysis
# 
# ---
# 

# In[6]:


def explore_unique_values(df, name="Dataset"):
    # 🔍 Begin unique value exploration
    safe_print(f"🔍 Unique Value Exploration for: {name}")
    safe_print("=" * 70)

    # 🔁 Loop through each column
    for col in df.columns:
        unique_vals = df[col].dropna().unique()  # Drop NaNs and get unique values
        num_unique = len(unique_vals)
        sample_vals = unique_vals[:5]  # Show up to 5 sample values

        # 🖨️ Output results
        safe_print(f"📌 Column: {col}")
        safe_print(f"   • Unique values: {num_unique}")
        safe_print(f"   • Sample values: {sample_vals}")

        # ⚠️ Flag numeric columns with very few unique values (might be categorical)
        if pd.api.types.is_numeric_dtype(df[col]) and num_unique < 15:
            safe_print("   ⚠️  Warning: Numeric column with few unique values (may be categorical)")

        safe_print("-" * 70)


# In[7]:


# 🔍 Explore unique values in the cash requests dataset
explore_unique_values(cash_df, name="Cash Requests")


# In[8]:


# 🔍 Explore unique values in the fees dataset
explore_unique_values(fees_df, name="Fees")


# ---
# 
# ## 🧠 Step 4 Summary: Initial Variable Exploration
# 
# By reviewing the number and types of unique values per column, we can now make informed decisions on variable classification:
# 
# - Columns like `created_at`, `updated_at`, `paid_at`, etc. are stored as objects but clearly represent **datetime values** and should be converted accordingly.
# - Columns like `status`, `type`, `transfer_type`, and `charge_moment` have a **small number of unique values** and are likely **categorical**.
# - Numeric columns such as `user_id`, `id`, and `cash_request_id` are technically numeric, but functionally act as **identifiers** — not quantitative variables.
# - `total_amount` in the `fees` dataset only has two unique values (5.0 and 10.0), which may require special handling during analysis or visualization.
# 
# This classification will guide us in:
# - Data cleaning and type conversion (e.g., dates, categories)
# - Selecting variables for summary statistics, plotting, and modeling
# - Ensuring we don't misinterpret identifiers as meaningful numbers
# 
# Next, we’ll proceed to **explicitly classify** each variable into:
# - 📊 Quantitative (numeric and continuous)
# - 🔤 Categorical (limited values)
# - 📅 Datetime (time-based)
# 
# ---
# 

# ---
# 
# ## 🧩 Step 5: Classifying Variables
# 
# Based on our unique value exploration, we now classify each column from both datasets into one of the following categories:
# 
# - **📊 Quantitative**: Numeric variables used for calculations or aggregation
# - **🔤 Categorical**: Discrete labels or groups
# - **📅 Datetime**: Columns containing timestamps or dates
# - 🆔 **Identifiers**: Unique values used to join or track records (not used for analysis)
# 
# ---
# 
# ### 📄 `cash_df` — Cash Request Dataset
# 
# | Column Name                 | Variable Type |
# |----------------------------|----------------|
# | `id`                       | Identifier     |
# | `amount`                   | Quantitative   |
# | `status`                   | Categorical    |
# | `created_at`               | Datetime       |
# | `updated_at`               | Datetime       |
# | `user_id`                  | Identifier     |
# | `moderated_at`             | Datetime       |
# | `deleted_account_id`       | Identifier     |
# | `reimbursement_date`       | Datetime       |
# | `cash_request_received_date`| Datetime      |
# | `money_back_date`          | Datetime       |
# | `transfer_type`            | Categorical    |
# | `send_at`                  | Datetime       |
# | `recovery_status`          | Categorical    |
# | `reco_creation`            | Datetime       |
# | `reco_last_update`         | Datetime       |
# 
# ---
# 
# ### 📄 `fees_df` — Fees Dataset
# 
# | Column Name        | Variable Type |
# |--------------------|----------------|
# | `id`               | Identifier     |
# | `cash_request_id`  | Identifier     |
# | `type`             | Categorical    |
# | `status`           | Categorical    |
# | `category`         | Categorical    |
# | `total_amount`     | Quantitative   |
# | `reason`           | Identifier-like (Text) |
# | `created_at`       | Datetime       |
# | `updated_at`       | Datetime       |
# | `paid_at`          | Datetime       |
# | `from_date`        | Datetime       |
# | `to_date`          | Datetime       |
# | `charge_moment`    | Categorical    |
# 
# ---
# 
# This classification will guide:
# - 🧹 Data type conversions
# - 📊 Summary statistics
# - 📈 Visualizations
# - 🧮 Metric calculations
# 
# ---

# In[9]:


# 🧠 Define variable classifications for each dataset using dictionaries
# This structure improves reusability and simplifies looping/filtering later

variable_types = {
    'cash_df': {
        'quantitative': ['amount'],
        'categorical': ['status', 'transfer_type', 'recovery_status'],
        'datetime': [
            'created_at', 'updated_at', 'moderated_at', 'reimbursement_date',
            'cash_request_received_date', 'money_back_date', 'send_at',
            'reco_creation', 'reco_last_update'
        ],
        'identifier': ['id', 'user_id', 'deleted_account_id']
    },
    'fees_df': {
        'quantitative': ['total_amount'],
        'categorical': ['type', 'status', 'category', 'charge_moment'],
        'datetime': ['created_at', 'updated_at', 'paid_at', 'from_date', 'to_date'],
        'identifier': ['id', 'cash_request_id', 'reason']
    }
}

# ✅ Inform the user that the classification is done
safe_print("✅ Variable classification completed for cash_df and fees_df.")


# ---
# 
# ## 🛠️ Step 6: Converting Datetime Columns
# 
# To ensure proper handling of time-based data, we convert all columns classified as `datetime` into the `datetime64` format using `pd.to_datetime()`.
# 
# This is crucial for:
# - Sorting records chronologically
# - Grouping by date or time periods
# - Calculating time deltas
# - Time-based visualizations
# 
# We’ll apply this transformation to both `cash_df` and `fees_df`.
# 
# ---
# 

# In[10]:


# 🛠️ Convert datetime columns to datetime64[ns] using variable_types dictionary

# Loop through each DataFrame and convert its specified datetime columns
for df_name, df in [('cash_df', cash_df), ('fees_df', fees_df)]:
    for col in variable_types[df_name]['datetime']:
        # Use errors='coerce' to safely handle invalid or missing datetime values
        df[col] = pd.to_datetime(df[col], errors='coerce')

# ✅ Confirm completion of conversion
safe_print("✅ Datetime conversion completed for both datasets.")


# ---
# 
# ### 🕓 Step 6A: Normalize Timezones Across Datetime Columns
# 
# Some datetime columns include timezone information (e.g., UTC), while others do not.  
# To ensure consistent comparison, grouping, and plotting, we’ll:
# 
# - Strip timezones from all datetime columns
# - Convert them to **timezone-naive** values (plain `datetime64[ns]`)
# 
# This step avoids errors during date filtering and ensures smooth downstream analysis.
# 
# ---
# 

# In[11]:


# 🔁 Strip timezone info from all datetime columns in both datasets

# Loop through both datasets
for df_name, df in [('cash_df', cash_df), ('fees_df', fees_df)]:
    for col in variable_types[df_name]['datetime']:
        # Check if the column is a datetime dtype before attempting to localize
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            try:
                # Remove timezone information if present
                df[col] = df[col].dt.tz_localize(None)
            except TypeError:
                # If already timezone-naive, ignore the error
                pass

# ✅ Confirm timezone cleanup
safe_print("✅ Timezone info stripped from all datetime columns (if any).")


# ---
# 
# ### 🕒 Step 6B: Check for Invalid or Future Dates
# 
# Next, we validate that all datetime columns contain realistic timestamps.
# 
# We will look for:
# - ❌ Dates accidentally far into the future (e.g., year 2099)
# - ❌ Non-sensical dates that could break our cohort or trend analysis
# 
# This helps us catch entry errors or placeholder values that should be handled before analysis.
# 
# ---
# 

# In[12]:


from datetime import datetime

# ✅ Define a cutoff date to identify incorrect future-dated records
# (Assumes analysis is current as of this date)
future_cutoff = pd.Timestamp("2024-12-12")

# 🧪 Identify rows in cash_df with any datetime column beyond the cutoff
future_cash_dates = cash_df[variable_types['cash_df']['datetime']].gt(future_cutoff).any(axis=1)
safe_print(f"🚨 Rows in `cash_df` with future dates: {future_cash_dates.sum()}")

# 🧪 Identify rows in fees_df with any datetime column beyond the cutoff
future_fees_dates = fees_df[variable_types['fees_df']['datetime']].gt(future_cutoff).any(axis=1)
safe_print(f"🚨 Rows in `fees_df` with future dates: {future_fees_dates.sum()}")

# 🖼️ Optional preview of affected rows (helpful during notebook inspection)
if is_colab():
    if future_cash_dates.any():
        safe_print("\n🔎 Sample future-dated rows in `cash_df`:")
        display(cash_df[future_cash_dates].head())

    if future_fees_dates.any():
        safe_print("\n🔎 Sample future-dated rows in `fees_df`:")
        display(fees_df[future_fees_dates].head())


# ---
# 
# ### ✅ Result: Future Date Validation Complete
# 
# All datetime columns have been successfully checked for invalid or far-future dates (beyond December 12, 2024).
# 
# #### Results:
# - 🚫 `cash_df`: **0** rows with dates beyond the threshold
# - 🚫 `fees_df`: **0** rows with dates beyond the threshold
# 
# This confirms that there are **no unrealistic timestamps** in either dataset.  
# With date validations complete, we now move on to checking for **duplicate records** in both datasets.
# 
# ---
# 

# ---
# 
# ## 🔁 Step 7: Check for Duplicates
# 
# Before cleaning or analyzing the data, we verify whether any duplicate rows or duplicate primary keys exist in the datasets. This step helps ensure:
# 
# - Accuracy of calculated metrics (e.g., revenue, frequency)
# - Uniqueness of primary keys like `id`
# - Elimination of redundant or repeated records
# 
# We will:
# - Count total duplicate rows
# - Count duplicated values in the `id` column
# - Display duplicated entries if any are found
# 
# ---
# 

# In[13]:


def check_duplicates(df, key_column=None, name="Dataset", preview=False):
    # 📍 Report title
    safe_print(f"🔁 Checking Duplicates in: {name}")
    safe_print("=" * 60)

    # 🔍 Count fully duplicated rows
    total_dupes = df.duplicated().sum()
    safe_print(f"📋 Total fully duplicated rows: {total_dupes}")

    # 🖼️ Preview sample full duplicates if requested
    if total_dupes > 0 and preview:
        safe_print("\n🔎 Sample duplicated rows:")
        display(df[df.duplicated()].head())

    # 🔍 Check duplicate values in the primary key column (if provided)
    if key_column:
        id_dupes = df[key_column].duplicated().sum()
        safe_print(f"🆔 Duplicated values in key column `{key_column}`: {id_dupes}")

        # 🖼️ Preview sample duplicate keys
        if id_dupes > 0 and preview:
            safe_print("\n🔎 Sample rows with duplicate IDs:")
            display(df[df[key_column].duplicated(keep=False)].head())
    else:
        safe_print("⚠️ No key column specified for duplicate ID check.")

    safe_print("=" * 60 + "\n")


# In[14]:


# ✅ Check for duplicates in cash_df
check_duplicates(
    cash_df,
    key_column='id',  # Primary key column in cash_df
    name="Cash Requests",
    preview=is_colab()  # Show sample rows only if running in notebook/Colab
)

# ✅ Check for duplicates in fees_df
check_duplicates(
    fees_df,
    key_column='id',  # Primary key column in fees_df
    name="Fees",
    preview=is_colab()
)


# ---
# 
# ### ✅ Summary of Duplicate Checks
# 
# No duplicate issues were found in either dataset:
# 
# - ✅ `cash_df` has **no fully duplicated rows** and **unique `id` values**.
# - ✅ `fees_df` also has **no duplicated rows** and a **unique `id` column**.
# 
# With data integrity confirmed, we can confidently proceed to the next cleaning step: **handling missing values**.
# 
# ---
# 

# ---
# 
# ## 🧹 Step 8: Handle Missing Values
# 
# We now explore and address missing values in both datasets. Handling missing data correctly is essential for ensuring reliable analysis.
# 
# We will:
# - Count missing values per column
# - Assess whether the missing values are acceptable, expected, or need cleaning
# - Make decisions based on business logic and dataset documentation:
#   - Some missing values (e.g. `money_back_date`, `paid_at`) indicate that an action hasn't occurred yet
#   - Others (e.g. `deleted_account_id`) may not be relevant for our analysis and could be dropped
# 
# ---
# 

# In[15]:


# 📊 Function to generate a missing value report
def missing_value_report(df, name="Dataset", max_rows=10):
    safe_print(f"📊 Missing Value Report for: {name}")
    safe_print("=" * 60)

    # Calculate missing value counts and percentages
    total = df.isnull().sum()
    percent = (total / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Values': total,
        'Percent (%)': percent
    })
    missing_df = missing_df[missing_df['Missing Values'] > 0]
    missing_df = missing_df.sort_values(by='Missing Values', ascending=False)

    if missing_df.empty:
        safe_print("✅ No missing values found.")
    else:
        display(missing_df.head(max_rows))  # Always preview

    safe_print("=" * 60 + "\n")


# In[16]:


# 🔍 Generate missing value report for each dataset
missing_value_report(cash_df, name="Cash Requests")
missing_value_report(fees_df, name="Fees")


# ---
# 
# ### 🧼 Summary of Missing Value Analysis
# 
# Based on the missing value report:
# 
# #### 📄 `cash_df` (Cash Requests)
# | Column                     | Missing % | Interpretation / Action |
# |----------------------------|------------|---------------------------|
# | `deleted_account_id`       | 91%        | ✅ Acceptable – only used if user deletes account (likely drop) |
# | `reimbursement_date`       | 87%        | ⚠️ Unexpected – should exist for most approved requests (needs further inspection) |
# | `reco_last_update`, `recovery_status`, `reco_creation` | 86% | ✅ Acceptable – only filled if there was a payment incident |
# | `money_back_date`          | 50%        | ✅ Acceptable – if null, reimbursement hasn’t occurred yet |
# | `moderated_at`             | 34%        | ✅ Acceptable – filled only for manually reviewed requests |
# | `cash_request_received_date`, `send_at` | ~32% | ✅ Acceptable – may be pending or declined |
# | `user_id`                  | 8.7%       | ⚠️ Should be investigated (especially for active requests) |
# 
# #### 📄 `fees_df` (Fees)
# | Column         | Missing % | Interpretation / Action |
# |----------------|------------|---------------------------|
# | `category`     | 89%        | ✅ Acceptable – only applies to `incident` fees |
# | `to_date`, `from_date` | ~68% | ✅ Acceptable – only apply to `postpone` fees |
# | `paid_at`      | 27%        | ✅ Acceptable – fee may not have been paid yet |
# | `cash_request_id` | 0.02%  | ⚠️ Should be inspected (rare, but could affect merges)
# 
# ---
# 
# ### ✅ Conclusion:
# - Most missing values are expected and related to the business logic.
# - Columns like `deleted_account_id`, `reco_creation`, `moderated_at`, etc. may be dropped or excluded from analysis if not needed.
# - Columns with rare nulls like `user_id` or `cash_request_id` should be inspected before dropping.
# 
# Next, we’ll proceed with **standardizing categorical values** and dropping unnecessary columns.
# 
# ---
# 

# ---
# 
# ### 🔍 Step 8A.1: Investigating `user_id` and `deleted_account_id`
# 
# According to the **Lexique - Data Analyst.xlsx**, the `deleted_account_id` field is described as:
# 
# > “If a user deletes their account, we are replacing the `user_id` by this id. It corresponds to a unique ID in the deleted account table with some keys information saved for fraud-fighting purposes (while respecting GDPR regulation).”
# 
# This implies the following:
# - A row should contain **either** a `user_id` or a `deleted_account_id`, **never both**
# - If **both are missing**, the row may be invalid or require further investigation
# - If only `deleted_account_id` is present, it still represents a unique user (a deleted one)
# 
# We will now verify:
# - Whether any rows contain **both** fields filled
# - Whether any rows have **neither** field filled
# - How many rows have **only `user_id`** or **only `deleted_account_id`**
# 
# This validation will allow us to confidently:
# - Treat both columns as a unified user reference
# - Optionally create a new column like `final_user_id`
# - Drop one or both original columns in later cleaning steps
# 
# ---
# 

# In[17]:


# 🔢 Total number of rows in the dataset
total_rows = len(cash_df)
safe_print(f"📦 Total rows in Cash Requests dataset: {total_rows}\n")

# ✅ Count rows where both `user_id` and `deleted_account_id` are present (should be rare or zero)
both_present = cash_df[cash_df['user_id'].notnull() & cash_df['deleted_account_id'].notnull()]
safe_print(f"🧪 Rows where both `user_id` and `deleted_account_id` are present: {len(both_present)}")

# ✅ Count rows where both are missing (should also be rare or zero)
both_missing = cash_df[cash_df['user_id'].isnull() & cash_df['deleted_account_id'].isnull()]
safe_print(f"🧪 Rows where both are missing: {len(both_missing)}")

# ✅ Count rows with only one of the two fields filled in
user_only = cash_df[(cash_df['user_id'].notnull()) & (cash_df['deleted_account_id'].isnull())]
deleted_only = cash_df[(cash_df['user_id'].isnull()) & (cash_df['deleted_account_id'].notnull())]

safe_print(f"✅ Rows with `user_id` only: {len(user_only)}")
safe_print(f"✅ Rows with `deleted_account_id` only: {len(deleted_only)}")


# ---
# 
# ### ✅ Summary: `user_id` vs `deleted_account_id`
# 
# Out of **23,970 rows** in the `cash_df` dataset:
# 
# - ✅ `user_id` only: 21,866 rows
# - ✅ `deleted_account_id` only: 2,103 rows
# - ⚠️ Both present: **1 row** (likely a data inconsistency)
# - ❌ Both missing: 0 rows
# 
# ### 🧠 Interpretation
# 
# The data confirms that `user_id` and `deleted_account_id` are **intended to be mutually exclusive**, with one of them always present. The presence of **1 row where both are filled** slightly violates this rule and may require manual review or correction.
# 
# ---
# 
# ### ✅ Next Step: Create a Unified User ID
# 
# To simplify analysis and maintain a single identifier for each user (active or deleted), we will create a new column called `final_user_id` that:
# 
# - Uses `user_id` when available
# - Falls back to `deleted_account_id` otherwise
# 
# After that, we can optionally **drop the original two columns** if they’re no longer needed.
# 
# ---
# 

# ---
# 
# ### 🔎 Step 8A.2: Inspecting Row with Both `user_id` and `deleted_account_id`
# 
# As per the Lexique context, each row should contain either a `user_id` or a `deleted_account_id`, but **not both**.  
# We found one row in the dataset where both fields are present.
# 
# Let's inspect that row to understand whether it's an error or a special case.
# 
# ---
# 

# In[18]:


# 🔍 Identify and preview rows where both IDs are present
rows_with_both = cash_df[(cash_df['user_id'].notnull()) & (cash_df['deleted_account_id'].notnull())]
safe_print(f"🔎 Rows with both `user_id` and `deleted_account_id`: {len(rows_with_both)}")

# 🖼️ Display the preview if any rows are found
if not rows_with_both.empty:
    display(rows_with_both.head())


# ---
# 
# ### 🧠 Interpretation & Next Step
# 
# The row appears valid — it represents a completed and reimbursed cash request. The presence of both IDs likely reflects that:
# 
# - The request was made when the user account was active (`user_id`)
# - The account was later deleted, and `deleted_account_id` was added for GDPR tracking
# 
# To maintain consistency with the logic that each row should have **only one ID**, we will:
# 
# - ✅ Keep the original `user_id`
# - ❌ Nullify `deleted_account_id` in this row
# 
# This aligns with how the rest of the dataset is structured.
# 
# ---
# 

# ---
# 
# ### 🔧 Step 8A.3: Fixing the Row with Both `user_id` and `deleted_account_id`
# 
# To preserve consistency across the dataset, we will correct the single row where both IDs are present.
# 
# As the request was made while the user was active (and reimbursed), we will:
# - ✅ Keep the `user_id`
# - ❌ Nullify the `deleted_account_id`
# 
# This ensures alignment with the business logic described in the Lexique documentation.
# 
# ---
# 

# In[19]:


# ✅ Nullify deleted_account_id where both IDs are present, keeping user_id
cash_df.loc[
    (cash_df['user_id'].notnull()) & (cash_df['deleted_account_id'].notnull()),
    'deleted_account_id'
] = np.nan

# 🔍 Display the same row to confirm the fix was applied
corrected_row = cash_df[cash_df['id'] == 280]
safe_print("🔍 Confirming fix for row with id = 280:")
display(corrected_row)


# ---
# 
# ### 🧪 Step 8A.4: Do `deleted_account_id` Users Actually Make Requests?
# 
# Before creating a unified user identifier (`final_user_id`), we need to confirm that users identified only by `deleted_account_id` are legitimate — meaning they actually made cash requests.
# 
# We’ll check:
# - The number of unique `deleted_account_id` values
# - How many of them have valid request data (e.g. `amount`, `status`)
# - Whether they appear multiple times in the dataset
# 
# This ensures we don’t introduce noise or system artifacts into the user-level analysis.
# 
# ---
# 

# In[20]:


# 🔍 Number of unique deleted_account_id values (excluding NaN)
unique_deleted_ids = cash_df['deleted_account_id'].dropna().unique()
safe_print(f"🧾 Total unique deleted_account_id values: {len(unique_deleted_ids)}")

# 🔍 How many of them made valid cash requests (non-null amount or status)?
deleted_requests = cash_df[cash_df['deleted_account_id'].notnull() & cash_df['amount'].notnull()]
safe_print(f"✅ Total deleted users with valid cash requests: {deleted_requests['deleted_account_id'].nunique()}")

# 🔍 Check how many cash requests were made per deleted user
deleted_request_counts = deleted_requests['deleted_account_id'].value_counts()

if not deleted_request_counts.empty:
    safe_print("📊 Sample request counts per deleted user:")
    display(deleted_request_counts.head())  # Safe and compact for all environments
else:
    safe_print("ℹ️ No deleted users with valid cash requests found.")


# ---
# 
# ### ✅ Summary of Deleted Users with Requests
# 
# - 🔢 **1140 unique `deleted_account_id` values** found in the dataset
# - ✅ All 1140 of them have at least one valid cash request
# - 🔁 Some deleted users made **multiple requests** — up to 19 times
# 
# ### 🧠 Conclusion:
# Deleted users represent valid former customers who used the platform and should **absolutely be included** in the cohort analysis.
# 
# We can now confidently proceed to create a unified `final_user_id` column that combines `user_id` and `deleted_account_id`.
# 
# ---
# 

# ---
# 
# ### 🛠️ Step 8A.5: Creating `final_user_id` Column
# 
# To unify user identity across the dataset, we now create a new column called `final_user_id`.
# 
# This column will:
# - Use the value from `user_id` when available
# - Fall back to `deleted_account_id` when `user_id` is missing
# 
# This ensures every row has a consistent user identifier, which is essential for:
# - Grouping cash requests by user
# - Defining cohorts
# - Calculating user-level metrics
# 
# ---
# 

# In[21]:


# ✅ Create a unified user ID column prioritizing `user_id`, fallback to `deleted_account_id`
cash_df['final_user_id'] = cash_df['user_id'].fillna(cash_df['deleted_account_id'])

# 🧪 Check for any rows still missing a user ID after combining
missing_final_ids = cash_df['final_user_id'].isnull().sum()
safe_print(f"❗ Rows with missing final_user_id: {missing_final_ids}")

# 🔍 Optional: Show sample rows if any missing remain (safe for .py scripts)
if missing_final_ids > 0:
    safe_print("⚠️ Sample rows with missing final_user_id:")
    display(cash_df[cash_df['final_user_id'].isnull()].head())
else:
    safe_print("✅ All rows have a valid final_user_id.")


# ---
# 
# ### ✅ Result: `final_user_id` Created
# 
# The `final_user_id` column has been successfully created by combining `user_id` and `deleted_account_id`.
# 
# This column will now serve as the **main user identifier** for the rest of the analysis, including:
# - Cohort assignment
# - Usage frequency calculations
# - Revenue and incident tracking per user
# 
# All subsequent grouping and user-level logic will rely on `final_user_id`.
# 
# ---
# 

# ---
# 
# ### 🧐 Step 8B: Investigating Missing `reimbursement_date` Values
# 
# The `reimbursement_date` column indicates the **scheduled date** on which the user is expected to repay their cash advance.
# 
# Over **87% of its values are missing**, which may initially appear concerning. However, based on the business rules, this could be expected in specific cases.
# 
# We’ll analyze which `status` values are most commonly associated with missing `reimbursement_date` to determine if this is a **data quality issue** or simply a result of the platform’s workflow logic.
# 
# ---
# 

# In[22]:


# 🔍 Filter rows with missing reimbursement_date
missing_reimbursement = cash_df[cash_df['reimbursement_date'].isnull()]

if missing_reimbursement.empty:
    safe_print("✅ No rows with missing reimbursement_date.")
else:
    # 📊 Count how many of those fall into each status
    missing_by_status = missing_reimbursement['status'].value_counts()

    # 🖨️ Show breakdown by status (safe for all environments)
    safe_print("📊 Breakdown of Missing `reimbursement_date` by Cash Request Status:")
    display(missing_by_status)


# ---
# 
# ### ✅ Interpretation of Missing `reimbursement_date`
# 
# The majority of missing values are tied to expected business scenarios:
# 
# - `money_back` (14,748) → Already reimbursed; no future reimbursement date needed
# - `rejected` (5,261) → Denied during manual review; never reached the reimbursement stage
# - `direct_debit_rejected` (748) → Reimbursement failed due to bank rejection; repayment must be handled through recovery
# - `canceled` (28) → Request was never confirmed by the user; canceled before approval
# - `transaction_declined` (44) → Transfer failed; reimbursement never scheduled
# - `direct_debit_sent` (33) → Waiting for confirmation of the debit result; reimbursement date may be set later
# - `active` (58) → Funds received by user, but reimbursement not yet scheduled
# 
# ### 🧠 Conclusion:
# 
# - Most missing values are **logically expected** based on the request status.
# - No rows require imputation or removal.
# - We will leave `reimbursement_date` as `NaT` for these records, since this column is **not used for cohort creation or metric calculations**.
# 
# ---
# 

# ---
# 
# ### 🔍 Step 8C.1: Validating `cash_request_id` Before Merge
# 
# To ensure the `fees_df` can be accurately merged with `cash_df`, we must verify that:
# 
# - Every non-null `cash_request_id` in `fees_df` exists in the `id` column of `cash_df`
# - Any unmatched IDs are rare or explainable (e.g., system errors, test records)
# 
# This step ensures merge integrity and prevents loss of data or broken links.
# 
# ---
# 

# In[23]:


# 🔍 Get all valid request IDs from cash_df
valid_cash_ids = set(cash_df['id'])

# 🔍 Identify which cash_request_ids in fees_df are NOT in cash_df
unmatched_ids = fees_df[~fees_df['cash_request_id'].isin(valid_cash_ids)]

# 🖨️ Summary counts
safe_print(f"🔎 Total unmatched `cash_request_id` values: {unmatched_ids['cash_request_id'].nunique()}")
safe_print(f"🔎 Total rows affected in `fees_df`: {len(unmatched_ids)}")

# 👁️ Optional: Preview a few unmatched rows
if not unmatched_ids.empty:
    safe_print("\n🔍 Sample unmatched rows:")
    display(unmatched_ids.head())
else:
    safe_print("✅ No unmatched `cash_request_id` values found.")


# ---
# 
# ### 🔎 Analysis of Missing `cash_request_id` in `fees_df`
# 
# Out of 21,061 rows in `fees_df`, only **4 rows** have a missing `cash_request_id`. Here's what we observed:
# 
# - ✅ All other `cash_request_id` values match valid `id`s in `cash_df` — so merging will be reliable
# - ❌ The 4 unmatched rows are:
#   - Marked as `instant_payment` type
#   - Have `status = cancelled`
#   - Lack any meaningful financial or timestamp information (e.g., no `paid_at`, `from_date`, or `to_date`)
# 
# These rows are likely **aborted or system-generated** fee records and do not provide analytical value.
# 
# ---
# 

# ---
# 
# ### 🧹 Step 8C.2: Dropping Unlinkable Fee Records
# 
# We identified **4 rows** in `fees_df` with missing `cash_request_id`. These cannot be linked to any actual cash request in `cash_df`, making them:
# 
# - Unusable for merging
# - Unusable for cohort or revenue analysis
# - Likely system artifacts (all have `status = cancelled` and no timestamps)
# 
# ### ✅ Action:
# These 4 rows will be dropped to preserve data integrity and streamline future merges.
# 
# ---
# 

# In[24]:


# 🧹 Store original row count to track dropped rows
original_len = len(fees_df)

# 🔍 Keep only rows with a valid (non-null) cash_request_id
fees_df = fees_df[fees_df['cash_request_id'].notnull()].copy()

# 📊 Calculate how many rows were removed
dropped = original_len - len(fees_df)

# ✅ Print results with safe formatting
safe_print(f"✅ New shape of `fees_df`: {fees_df.shape}")
safe_print(f"🗑️ Dropped rows with missing `cash_request_id`: {dropped}")


# ---
# 
# ### ✅ Result: `fees_df` Cleaned and Ready
# 
# - The 4 rows with missing `cash_request_id` have been successfully removed
# - ✅ `fees_df` now contains **21,057 rows** with fully valid `cash_request_id` values
# - This ensures safe and accurate merging with `cash_df` during cohort and revenue analysis
# 
# We’re now ready to proceed with **standardizing categorical values**.
# 
# ---
# 

# ---
# 
# ### 🔤 Step 9: Standardizing Categorical Values
# 
# To ensure clean and consistent analysis, we standardize all key categorical columns by:
# 
# - Lowercasing all string values
# - Removing unwanted whitespace
# - Replacing inconsistent values if needed (e.g., typos or variants)
# 
# This avoids grouping issues and prepares the dataset for clean visualizations and metric calculations.
# 
# The following columns will be standardized:
# - **`cash_df`**: `status`, `transfer_type`, `recovery_status`
# - **`fees_df`**: `type`, `status`, `category`, `charge_moment`
# 
# ---
# 

# ---
# 
# ### 🧰 Step 9A: Define Helper Function for Categorical Standardization
# 
# We define a reusable function that:
# - Converts string values to lowercase
# - Strips leading/trailing whitespace
# - Converts `"nan"` strings (if they appear) back to proper `NaN`
# 
# This helps ensure consistency across multiple categorical columns.
# 
# ---
# 

# In[25]:


# 🧼 Helper function to clean string-based categorical columns
def clean_categorical_column(df, col):
    """
    Standardizes a string-based categorical column:
    - Lowercases text
    - Strips leading/trailing spaces
    - Converts "nan" strings to actual NaN values
    """
    # Normalize text formatting
    df[col] = df[col].astype(str).str.lower().str.strip()

    # Replace literal "nan" strings with proper NaN
    df[col] = df[col].replace("nan", np.nan)

    # ✅ Confirm cleaning
    safe_print(f"🧼 Cleaned column: {col}")


# ---
# 
# ### 🔁 Step 9B: Apply Function to All Relevant Categorical Columns
# 
# We now apply our cleaning function to the categorical columns in both datasets:
# 
# - `cash_df`: `status`, `transfer_type`, `recovery_status`
# - `fees_df`: `type`, `status`, `category`, `charge_moment`
# 
# ---
# 

# In[26]:


# 🔁 Apply cleaning to `cash_df` categorical columns
for col in variable_types['cash_df']['categorical']:
    clean_categorical_column(cash_df, col)

# 🔁 Apply cleaning to `fees_df` categorical columns
for col in variable_types['fees_df']['categorical']:
    clean_categorical_column(fees_df, col)

# ✅ Preview unique values in cleaned categorical columns from cash_df
safe_print("\n✅ Unique values in `cash_df` categorical columns:")
for col in variable_types['cash_df']['categorical']:
    unique_vals = cash_df[col].dropna().unique()
    safe_print(f"🔹 {col} ({len(unique_vals)}): {unique_vals}")

# ✅ Preview unique values in cleaned categorical columns from fees_df
safe_print("\n✅ Unique values in `fees_df` categorical columns:")
for col in variable_types['fees_df']['categorical']:
    unique_vals = fees_df[col].dropna().unique()
    safe_print(f"🔹 {col} ({len(unique_vals)}): {unique_vals}")


# ---
# 
# ### ✅ Result: Categorical Columns Standardized
# 
# All relevant categorical columns have been successfully cleaned.  
# We now have consistent, lowercase values across both datasets:
# 
# #### 🔹 `cash_df` Categorical Columns:
# 
# - **`status`**:
#   - `'rejected'`
#   - `'money_back'`
#   - `'canceled'`
#   - `'active'`
#   - `'direct_debit_rejected'`
#   - `'transaction_declined'`
#   - `'direct_debit_sent'`
# 
# - **`transfer_type`**:
#   - `'regular'`
#   - `'instant'`
# 
# - **`recovery_status`**:
#   - `NaN`
#   - `'completed'`
#   - `'pending'`
#   - `'pending_direct_debit'`
#   - `'cancelled'`
# 
# #### 🔹 `fees_df` Categorical Columns:
# 
# - **`type`**:
#   - `'instant_payment'`
#   - `'incident'`
#   - `'postpone'`
# 
# - **`status`**:
#   - `'rejected'`
#   - `'accepted'`
#   - `'cancelled'`
#   - `'confirmed'`
# 
# - **`category`**:
#   - `NaN`
#   - `'rejected_direct_debit'`
#   - `'month_delay_on_payment'`
# 
# - **`charge_moment`**:
#   - `'after'`
#   - `'before'`
# 
# ---
# 
# ### 🧠 Conclusion:
# These cleaned values are now safe to use for:
# - Grouping users by request status or fee type
# - Calculating cohort-based metrics (frequency, revenue, incident rates)
# - Building visualizations without risk of typos or mismatched strings
# 
# We’re now ready to **finalize data quality checks** before moving to EDA.
# 
# ---
# 

# ---
# 
# ### 🔎 Step 10: Validate Monetary Columns (`amount`, `total_amount`)
# 
# Before beginning EDA, we must confirm that monetary values are:
# - ✅ Stored as numeric data types (`float` or `int`)
# - ✅ Not negative or zero, unless it makes sense for the business
# 
# We'll check:
# - `cash_df['amount']`
# - `fees_df['total_amount']`
# 
# Any unexpected values (e.g., negatives) could indicate data issues or special business rules that need to be flagged.
# 
# ---
# 

# In[27]:


# 🔍 Check if monetary columns are numeric
safe_print(f"📊 `amount` type (cash_df): {cash_df['amount'].dtype}")
safe_print(f"📊 `total_amount` type (fees_df): {fees_df['total_amount'].dtype}")

# ❌ Check for negative or zero values
safe_print(f"\n🚩 `cash_df`: Negative or zero amounts: {(cash_df['amount'] <= 0).sum()}")
safe_print(f"🚩 `fees_df`: Negative or zero total_amount: {(fees_df['total_amount'] <= 0).sum()}")

# ✅ Optional: preview invalid rows if any exist
invalid_cash = cash_df[cash_df['amount'] <= 0]
invalid_fees = fees_df[fees_df['total_amount'] <= 0]

if not invalid_cash.empty:
    safe_print("\n🔎 Sample invalid entries in `cash_df`:")
    display(invalid_cash.head())

if not invalid_fees.empty:
    safe_print("\n🔎 Sample invalid entries in `fees_df`:")
    display(invalid_fees.head())


# ---
# 
# ### ✅ Result: Monetary Columns Validated
# 
# - `cash_df['amount']` and `fees_df['total_amount']` are both correctly typed as `float64`
# - ✅ No negative or zero values found in either column
# 
# This confirms that both monetary columns are clean and ready for analysis.
# 
# ---
# 

# ---
# 
# ### 🗂️ Step 11: Reordering Columns for Better Readability
# 
# To make the datasets easier to navigate during EDA, we’ll reorganize the columns by placing the most important fields (like IDs, dates, and key categorical variables) at the front.
# 
# This step does **not affect the analysis**, but improves visibility and usability when exploring the data.
# 
# ---
# 

# In[28]:


# 🗂️ Define desired column order for cash_df
cash_primary_cols = [
    'id', 'final_user_id', 'amount', 'status', 'transfer_type', 'reimbursement_date', 'created_at'
]

# ➕ Append remaining columns dynamically
remaining_cash_cols = [col for col in cash_df.columns if col not in cash_primary_cols]
cash_df = cash_df[cash_primary_cols + remaining_cash_cols]

# ✅ Preview reordered cash_df
safe_print("✅ Preview of reordered `cash_df`:")
display(cash_df.head())

# 🗂️ Define desired column order for fees_df
fees_primary_cols = [
    'id', 'cash_request_id', 'total_amount', 'type', 'status', 'created_at'
]

# ➕ Append remaining columns dynamically
remaining_fees_cols = [col for col in fees_df.columns if col not in fees_primary_cols]
fees_df = fees_df[fees_primary_cols + remaining_fees_cols]

# ✅ Preview reordered fees_df
safe_print("✅ Preview of reordered `fees_df`:")
display(fees_df.head())


# ---
# 
# ### 🔍 Step 12: Data Type Sanity Check (Column-Level)
# 
# To ensure each variable is correctly interpreted by Pandas, we examine the data type of **every column** in both datasets.
# 
# This step helps confirm:
# - Numerical fields are `int64` or `float64`
# - Categorical fields are `object` or `category`
# - All datetime variables were properly converted to `datetime64[ns]`
# 
# Spotting incorrect types at this stage prevents issues during grouping, merging, and visualizations later.
# 
# ---
# 

# In[29]:


# 🧠 Check column-level data types in both DataFrames

safe_print("📋 Detailed Data Types in `cash_df`:\n")
display(cash_df.dtypes.sort_index())

safe_print("\n📋 Detailed Data Types in `fees_df`:\n")
display(fees_df.dtypes.sort_index())


# ---
# 
# ### ✅ Result: Detailed Data Type Validation Complete
# 
# We reviewed every column in both datasets to confirm that variable types align with their expected role in the analysis.
# 
# #### `cash_df` Highlights:
# - All **date columns** are properly formatted as `datetime64[ns]`
# - **Numerical columns** like `amount`, `user_id`, and `final_user_id` are stored as `float64` or `int64`
# - **Categorical fields** like `status`, `transfer_type`, and `recovery_status` are stored as `object`
# 
# #### `fees_df` Highlights:
# - All **datetime columns** are of type `datetime64[ns]`
# - **Monetary column** `total_amount` is `float64`
# - **Categorical fields** like `type`, `status`, `category`, and `charge_moment` are `object`
# - All columns are correctly typed and ready for analysis
# 
# ✅ No adjustments needed — the datasets are now clean, structured, and analysis-ready.  
# Next, we will **save cleaned versions of both datasets** to avoid repeating the cleaning process in future steps.
# 
# ---
# 

# ---
# 
# ### 💾 Step 13: Saving Cleaned Datasets
# 
# To preserve the cleaned data and avoid repeating cleaning steps, we’ll export both DataFrames to CSV files.
# 
# The files will be saved in a new subfolder called `cleaned_project_datasets` inside the main project directory.
# 
# ---
# 

# In[30]:


import os

# ✅ Toggle to control whether existing CSVs are overwritten
OVERWRITE_CSV = True  # 🔁 Set to False to skip writing if files already exist

# 📁 Define the output folder relative to project base path
output_folder = os.path.join(project_base_path, 'cleaned_project_datasets')
os.makedirs(output_folder, exist_ok=True)  # Ensure the folder exists

# 📄 Define full file paths
cash_output_path = os.path.join(output_folder, 'clean_cash_requests.csv')
fees_output_path = os.path.join(output_folder, 'clean_fees.csv')

# 💾 Save cash_df
if OVERWRITE_CSV or not os.path.exists(cash_output_path):
    cash_df.to_csv(cash_output_path, index=False)
    safe_print(f"✅ Saved: {cash_output_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {cash_output_path}")

# 💾 Save fees_df
if OVERWRITE_CSV or not os.path.exists(fees_output_path):
    fees_df.to_csv(fees_output_path, index=False)
    safe_print(f"✅ Saved: {fees_output_path}")
else:
    safe_print(f"⚠️ Skipped (already exists): {fees_output_path}")


# # 🧩 Optional Script Entry Point
# 
# This block enables the notebook to be used as a standalone script.  
# When the `.py` version of this notebook is executed via CLI, the cleaning process will run automatically.
# 

# In[31]:


# ✅ Optional script execution indicator for CLI use
if __name__ == "__main__":
    safe_print("🚀 Script executed directly as a .py file — all code above has already run in notebook order.")



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
