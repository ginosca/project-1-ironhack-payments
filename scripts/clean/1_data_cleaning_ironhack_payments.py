# 🧼 Data Cleaning Script – Ironhack Payments
# 📓 Source Notebook: 1_data_cleaning_ironhack_payments.ipynb
# 🧠 Description: Loads, inspects, and cleans raw cash request and fee datasets.
# 📅 Date: December 13, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila
# 🛠️ Bootcamp: Ironhack Data Science and Machine Learning

#!/usr/bin/env python
# coding: utf-8

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


# In[10]:


# 🛠️ Convert datetime columns to datetime64[ns] using variable_types dictionary

# Loop through each DataFrame and convert its specified datetime columns
for df_name, df in [('cash_df', cash_df), ('fees_df', fees_df)]:
    for col in variable_types[df_name]['datetime']:
        # Use errors='coerce' to safely handle invalid or missing datetime values
        df[col] = pd.to_datetime(df[col], errors='coerce')

# ✅ Confirm completion of conversion
safe_print("✅ Datetime conversion completed for both datasets.")


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


# In[18]:


# 🔍 Identify and preview rows where both IDs are present
rows_with_both = cash_df[(cash_df['user_id'].notnull()) & (cash_df['deleted_account_id'].notnull())]
safe_print(f"🔎 Rows with both `user_id` and `deleted_account_id`: {len(rows_with_both)}")

# 🖼️ Display the preview if any rows are found
if not rows_with_both.empty:
    display(rows_with_both.head())


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


# In[29]:


# 🧠 Check column-level data types in both DataFrames

safe_print("📋 Detailed Data Types in `cash_df`:\n")
display(cash_df.dtypes.sort_index())

safe_print("\n📋 Detailed Data Types in `fees_df`:\n")
display(fees_df.dtypes.sort_index())


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
