# 📈 Cohort Metrics Script – Ironhack Payments
# 📓 Source Notebook: 3_cohort_analysis_metrics.ipynb
# 📊 Description: Calculates monthly cohort KPIs: user retention, frequency, incidents, and revenue.
# 📅 Date: December 13, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila
# 🛠️ Bootcamp: Ironhack Data Science and Machine Learning

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os

# ✅ Safe print to avoid encoding issues
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="ignore").decode())

# ✅ Check for Colab environment
def is_colab():
    return 'google.colab' in sys.modules

# ✅ Set base path dynamically
if is_colab():
    from google.colab import drive
    drive.mount('/content/drive')

    # Try default user path (adjustable)
    default_path = 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'
    full_default_path = os.path.join('/content/drive', default_path)

    if os.path.exists(full_default_path):
        project_base_path = full_default_path
        safe_print(f"✅ Colab project path set to: {project_base_path}")
    else:
        safe_print("\n📂 Default path not found. Please input the relative path to your project inside Google Drive.")
        safe_print("👉 Example: 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'")
        user_path = input("📥 Your path: ").strip()
        project_base_path = os.path.join('/content/drive', user_path)

        if not os.path.exists(project_base_path):
            raise FileNotFoundError(f"❌ Path does not exist: {project_base_path}\nPlease check your input.")

        safe_print(f"✅ Colab project path set to: {project_base_path}")
else:
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        script_dir = os.getcwd()

    # Assume script is inside /scripts/ and go two levels up
    project_base_path = os.path.abspath(os.path.join(script_dir, '..', '..'))
    safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")


# In[2]:


import pandas as pd
import os

# 📂 Define EDA output directory path
eda_data_path = os.path.join(project_base_path, 'eda_outputs', 'data')

# 🗂️ Define file paths
eda_files = {
    'user_first_request': 'user_first_request.csv',
    'monthly_active_users': 'monthly_active_users.csv',
    'transfer_type_share': 'transfer_type_share.csv',
    'merged_cash_fee': 'merged_cash_fee.csv',
}

# 📥 Load each file into a DataFrame with error handling
dataframes = {}
safe_print("📄 Loading EDA output files...\n")

for key, filename in eda_files.items():
    file_path = os.path.join(eda_data_path, filename)
    safe_print(f"📁 Looking for: {file_path}")

    try:
        df = pd.read_csv(file_path)
        dataframes[key] = df
        safe_print(f"✅ Loaded {filename} → Shape: {df.shape}")
    except FileNotFoundError:
        safe_print(f"❌ File not found: {file_path}")
        safe_print("📌 Check that the file exists and the name is spelled correctly.")
        raise

# 🔄 Unpack dataframes for easy access
user_first_request_df = dataframes['user_first_request']
monthly_active_users_df = dataframes['monthly_active_users']
transfer_type_share_df = dataframes['transfer_type_share']
merged_df = dataframes['merged_cash_fee']


# In[3]:


import io

# ✅ Define display fallback for script environments
try:
    display
except NameError:
    def display(x):
        print(x.to_string() if isinstance(x, pd.DataFrame) else x)

# 🔍 Inspect basic structure of a DataFrame with optional previews and toggles
def inspect_basic_structure(df, name="Dataset", preview_rows=5, full=False):
    """
    Display structure, sample rows, schema, and optional full view of a DataFrame.
    Compatible with notebooks and terminal scripts.

    Parameters:
    - df: pandas DataFrame
    - name: Custom name to identify the DataFrame
    - preview_rows: Number of rows to show from head and tail
    - full: If True, display the entire DataFrame
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
    safe_print(f"\n🔹 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # 🏷️ Column names
    safe_print("\n🔹 Column Names:")
    safe_print(df.columns.tolist())

    # 🧬 Data types and non-null counts
    safe_print("\n🔹 Data Types and Non-Null Counts:")
    buffer = io.StringIO()
    df.info(buf=buffer)
    safe_print(buffer.getvalue())

    # 🧼 Missing values
    safe_print("\n🔹 Missing Values (Null Counts):")
    display(df.isnull().sum())

    # 👁️ Optional: Full DataFrame display
    if full:
        safe_print("\n🔹 Full Data Preview:")
        display(df)

    safe_print("=" * 60 + "\n")


# In[4]:


# 🔍 Inspect the user-to-cohort mapping dataset
inspect_basic_structure(user_first_request_df, name="user_first_request.csv")


# In[5]:


# 🔍 Inspect the Monthly Active Users dataset
inspect_basic_structure(monthly_active_users_df, name="monthly_active_users.csv")


# In[6]:


# 🔍 Inspect the monthly transfer type distribution dataset
inspect_basic_structure(transfer_type_share_df, name="transfer_type_share.csv")


# In[7]:


# 🔍 Inspect the merged dataset containing cash requests and associated fees
inspect_basic_structure(merged_df, name="merged_cash_fee.csv")


# In[8]:


# 📎 Merge cohort data into merged_df using final_user_id
safe_print("🔄 Merging cohort_month into merged_df based on final_user_id...\n")

try:
    # ✅ Merge on final_user_id to assign each request its cohort
    merged_cash_fee_cohort = pd.merge(
        merged_df,
        user_first_request_df[['final_user_id', 'cohort_month', 'cohort_year_month']],
        on='final_user_id',
        how='left'
    )

    # ✅ Confirm the merge was successful
    safe_print("✅ Merge completed. Cohort assigned to each cash request.")
    safe_print(f"📐 Updated merged_cash_fee_cohort shape: {merged_cash_fee_cohort.shape}")

except Exception as e:
    safe_print("❌ Merge failed. Please check the input datasets.")
    raise e


# In[9]:


# ✅ Cohort Assignment Validation
safe_print("\n✅ Validating cohort assignment...\n")

# 📏 Total number of rows
total_rows = merged_cash_fee_cohort.shape[0]
safe_print(f"📐 Total rows in merged dataset: {total_rows}")

# ❓ Check for missing cohort_month values
missing_cohort_rows = merged_cash_fee_cohort['cohort_month'].isna().sum()
safe_print(f"❓ Rows with missing cohort_month: {missing_cohort_rows}")

# 👀 If missing values exist, show preview
if missing_cohort_rows > 0:
    safe_print("\n⚠️ Preview of rows with missing cohort_month:")
    display(merged_cash_fee_cohort[merged_cash_fee_cohort['cohort_month'].isna()].head())
else:
    safe_print("✅ All records have been successfully assigned to a cohort.")

# 🔁 Check if any users are linked to multiple cohort_months
safe_print("\n🔎 Verifying cohort consistency across user transactions...")
user_cohort_counts = merged_cash_fee_cohort.groupby('final_user_id')['cohort_month'].nunique()
inconsistent_users = user_cohort_counts[user_cohort_counts > 1]

if inconsistent_users.empty:
    safe_print("✅ Cohort assignment is consistent: Each user maps to a single cohort_month.")
else:
    safe_print(f"❌ Found {len(inconsistent_users)} users with multiple cohort_month values!")
    safe_print("🧪 Sample of affected users and cohort counts:")
    display(inconsistent_users.head())


# In[10]:


# 👁️ Compact summary preview of merged dataset
safe_print("👁️ Previewing merged_cash_fee_cohort (compact summary)...")

# Show selective key columns only
safe_print("\n📄 First 3 rows (partial columns):")
display(merged_cash_fee_cohort.head(3)[['cash_request_id', 'final_user_id', 'amount', 'cash_status', 'cohort_month']])

safe_print("\n📄 Last 3 rows (partial columns):")
display(merged_cash_fee_cohort.tail(3)[['cash_request_id', 'final_user_id', 'amount', 'cash_status', 'cohort_month']])

# Print column names
safe_print("\n📋 Column names in merged_cash_fee_cohort:")
safe_print(merged_cash_fee_cohort.columns.tolist())

# Show shape
safe_print(f"\n📐 Shape: {merged_cash_fee_cohort.shape[0]} rows × {merged_cash_fee_cohort.shape[1]} columns\n")


# In[11]:


# ✅ Define the custom column order for cohort analysis
new_column_order = [
    # 🧩 Cohort metadata
    'final_user_id', 'cohort_month', 'cohort_year_month',

    # 💳 Cash request details
    'cash_request_id', 'amount', 'cash_status', 'transfer_type',
    'reimbursement_date', 'cash_created_at', 'cash_updated_at',
    'user_id', 'moderated_at', 'deleted_account_id',
    'cash_request_received_date', 'money_back_date', 'send_at',
    'recovery_status', 'reco_creation', 'reco_last_update',
    'year_month', 'month_label', 'recovery_status_clean', 'incident_flag',

    # 💸 Fee-related columns
    'fee_id', 'total_amount', 'type', 'fee_status', 'fee_created_at',
    'category', 'reason', 'fee_updated_at', 'paid_at',
    'from_date', 'to_date', 'charge_moment'
]


# 🛠️ Apply the reordering if all columns exist
missing_columns = [col for col in new_column_order if col not in merged_cash_fee_cohort.columns]

if not missing_columns:
    merged_cash_fee_cohort = merged_cash_fee_cohort[new_column_order]
    safe_print("✅ Columns reordered successfully.\n")

    # 👁️ Preview updated layout (compact, 3 rows)
    safe_print("👁️ Preview after reordering (first 3 rows):")
    try:
        display(merged_cash_fee_cohort.head(3))
    except NameError:
        safe_print("(🔍 Preview skipped – display not available in .py execution mode)")

    # 💾 Save the reordered dataset
    save_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'merged_cash_fee_cohort.csv')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    try:
        merged_cash_fee_cohort.to_csv(save_path, index=False)
        safe_print(f"💾 Reordered dataset saved to: {save_path}")
    except Exception as e:
        safe_print("❌ Failed to save the reordered dataset.")
        raise e

else:
    safe_print("⚠️ Some expected columns are missing. Could not reorder.")
    safe_print(f"Missing columns: {missing_columns}")


# In[12]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 📌 First plot of the notebook
PLOT_INDEX = 1
OVERWRITE_PLOTS = True  # Set to False if you don't want to overwrite existing plots

# 📊 Frequency of service usage per cohort
safe_print("📊 Calculating frequency of service usage per cohort...\n")

try:
    # ✅ Group by cohort and usage month
    cohort_usage = (
        merged_cash_fee_cohort
        .groupby(['cohort_year_month', 'year_month'])
        .size()
        .reset_index(name='num_requests')
    )

    # 🔄 Pivot to form cohort usage matrix
    cohort_usage_matrix = cohort_usage.pivot(
        index='cohort_year_month',
        columns='year_month',
        values='num_requests'
    ).fillna(0).astype(int)

    # ✅ Display full matrix
    safe_print("📋 Cohort usage matrix (cash request counts):")
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        display(cohort_usage_matrix)

    # 💾 Save cohort matrix to output folder
    output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_usage_matrix.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cohort_usage_matrix.to_csv(output_path)
    safe_print(f"\n💾 Cohort usage matrix saved to: {output_path}")

    # 🎨 Plot the cohort usage heatmap
    plt.figure(figsize=(14, 8))
    sns.heatmap(
        cohort_usage_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        linecolor='gray',
        cbar_kws={"label": "Number of Requests"}
    )

    plt.title("Cash Request Frequency per User Cohort", fontsize=16, pad=20)
    plt.xlabel("Activity Month (year_month)")
    plt.ylabel("Cohort (cohort_year_month)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.grid(False)

    # ✅ Adjust layout before adding footnote
    plt.tight_layout()

    # ✅ Add the footnote (after tight_layout)
    plt.figtext(
        0.5, -0.05,
        "Note: Nov 2019 and Nov 2020 are partial months – values may be underrepresented.",
        wrap=True,
        horizontalalignment='center',
        fontsize=10,
        color='gray'
    )

    # 💾 Save plot with indexed filename (ensure note is saved using bbox_inches='tight')
    plot_filename = f"{PLOT_INDEX:02d}_cohort_usage_heatmap.png"
    plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
    os.makedirs(os.path.dirname(plot_path), exist_ok=True)

    if OVERWRITE_PLOTS or not os.path.exists(plot_path):
        plt.savefig(plot_path, bbox_inches='tight')  # ✅ Save with footnote
        safe_print(f"✅ Cohort usage heatmap saved to: {plot_path}")
    else:
        safe_print(f"⚠️ Skipped saving (already exists): {plot_path}")

    plt.show()

    # 🔁 Increment plot index
    PLOT_INDEX += 1

except Exception as e:
    safe_print("❌ Failed to calculate or plot cohort usage matrix.")
    raise e


# In[13]:


# 📊 Calculate retention rate matrix with dtype compatibility fix
safe_print("\n📊 Calculating monthly retention rates per cohort...\n")

try:
    # ✅ Load the cohort usage matrix if not already available
    if 'cohort_usage_matrix' not in globals():
        cohort_matrix_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_usage_matrix.csv')
        cohort_usage_matrix = pd.read_csv(cohort_matrix_path, index_col=0)

    # ✅ Create a new DataFrame for retention as float type
    retention_matrix = cohort_usage_matrix.astype(float)

    # ✅ Normalize each row by its first non-zero value (first month of cohort)
    for idx, row in retention_matrix.iterrows():
        first_value = row[row > 0].iloc[0] if any(row > 0) else None
        if first_value and first_value != 0:
            retention_matrix.loc[idx] = (row / first_value).round(3)
        else:
            retention_matrix.loc[idx] = 0.0

    # ✅ Display the matrix
    safe_print("📋 Retention rate matrix (proportions):")
    display(retention_matrix)

    # 💾 Save to file
    retention_output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_retention_matrix.csv')
    os.makedirs(os.path.dirname(retention_output_path), exist_ok=True)
    retention_matrix.to_csv(retention_output_path)
    safe_print(f"\n💾 Retention matrix saved to: {retention_output_path}")

except Exception as e:
    safe_print("❌ Failed to compute retention matrix.")
    raise e


# In[14]:


import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# 🔧 Plot-saving config
OVERWRITE_PLOTS = True  # Set False to skip re-saving existing images

# 🔄 Load the retention matrix
retention_matrix_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_retention_matrix.csv')
retention_matrix = pd.read_csv(retention_matrix_path, index_col=0)

# 🎨 Plot the heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(
    retention_matrix,
    annot=True,
    fmt=".2f",
    cmap="YlGnBu",
    linewidths=0.5,
    linecolor='gray',
    cbar_kws={"label": "Retention Rate"}
)

plt.title("Monthly Retention Rate per User Cohort", fontsize=16, pad=20)
plt.xlabel("Activity Month (year_month)")
plt.ylabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.grid(False)

# ✅ Adjust layout BEFORE adding figtext
plt.tight_layout()

# ✅ Add footnote (after tight_layout)
plt.figtext(
    0.5, -0.05,
    "Note: Nov 2019 and Nov 2020 are partial months – values may be underrepresented.",
    wrap=True,
    horizontalalignment='center',
    fontsize=10,
    color='gray'
)

# 💾 Save the heatmap with indexed filename and bbox to include footnote
plot_filename = f"{PLOT_INDEX:02d}_cohort_retention_heatmap.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path, bbox_inches='tight')  # ✅ This includes the note!
    safe_print(f"✅ Retention heatmap saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving (already exists): {plot_path}")

plt.show()

# 🔁 Increment plot index
PLOT_INDEX += 1


# In[15]:


import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

safe_print("📊 Recalculating retention matrix and generating heatmap (excluding partial cohorts and months)...\n")

# 🔻 Remove partial cohort rows and observation columns
partial_months = ['2019-11', '2020-11']
filtered_usage = cohort_usage_matrix.drop(index=partial_months, columns=partial_months, errors='ignore')

# 🔁 Normalize each cohort row by its first value
filtered_retention_matrix = filtered_usage.astype(float).copy()

for idx, row in filtered_retention_matrix.iterrows():
    first_value = row.loc[idx] if idx in row else None
    if pd.notna(first_value) and first_value > 0:
        filtered_retention_matrix.loc[idx] = (row / first_value).round(3)
    else:
        filtered_retention_matrix.loc[idx] = 0.0

# ✅ Preview
safe_print("📋 Filtered retention matrix (proportions):")
display(filtered_retention_matrix)

# 💾 Save the filtered matrix
filtered_retention_path = os.path.join(
    project_base_path,
    'cohort_outputs', 'data', 'cohort_retention_matrix_filtered.csv'
)
os.makedirs(os.path.dirname(filtered_retention_path), exist_ok=True)
filtered_retention_matrix.to_csv(filtered_retention_path)
safe_print(f"💾 Filtered retention matrix saved to: {filtered_retention_path}")

# 🎨 Plot heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(
    filtered_retention_matrix,
    annot=True,
    fmt='.2f',
    cmap='YlGnBu',
    linewidths=0.5,
    cbar_kws={'label': 'Retention Rate'}
)

plt.title("Monthly Retention Rate per User Cohort (Excludes Nov 2019 & Nov 2020 – Partial Months)")
plt.xlabel("Activity Month (year_month)")
plt.ylabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.yticks(rotation=0)
plt.tight_layout()

# 💾 Save the plot with indexed filename
plot_filename = f"{PLOT_INDEX:02d}_cohort_retention_heatmap_filtered.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if 'OVERWRITE_PLOTS' not in globals():
    OVERWRITE_PLOTS = False

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Filtered retention heatmap saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()

# 🔁 Increment plot index
PLOT_INDEX += 1


# In[16]:


# 📈 Plot retention curves for selected strong cohorts only
import matplotlib.pyplot as plt

safe_print("📈 Plotting retention curves for selected cohorts: 2020-02 to 2020-05...\n")

# 🔄 Load the filtered retention matrix
filtered_retention_path = os.path.join(
    project_base_path,
    'cohort_outputs', 'data', 'cohort_retention_matrix_filtered.csv'
)
filtered_retention_matrix = pd.read_csv(filtered_retention_path, index_col=0)

# ✅ Define selected cohorts to plot
selected_cohorts = ['2020-02', '2020-03', '2020-04', '2020-05']

# 🎨 Plot the curves
plt.figure(figsize=(12, 7))

for cohort_label in selected_cohorts:
    if cohort_label in filtered_retention_matrix.index:
        cohort_values = filtered_retention_matrix.loc[cohort_label]
        plt.plot(cohort_values.index, cohort_values.values, marker='o', label=cohort_label)

plt.title("Retention Curves – Selected Cohorts (Filtered)", fontsize=16, pad=20)
plt.xlabel("Activity Month (year_month)")
plt.ylabel("Retention Rate")
plt.xticks(rotation=45)
plt.ylim(0, 1.05)
plt.grid(True)
plt.legend(title="Cohort", loc='upper right')
plt.tight_layout()

# 💾 Save with next plot index
plot_filename = f"{PLOT_INDEX:02d}_cohort_retention_curves_selected.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Selected cohort retention curves saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()

# 🔁 Increment plot index
PLOT_INDEX += 1


# In[17]:


# ⚠️ Step 14: Incident Rate per Cohort
safe_print("\n⚠️ Calculating incident rate per cohort...\n")

try:
    # 🔢 Count total and incident requests per cohort
    total_counts = (
        merged_cash_fee_cohort
        .groupby('cohort_year_month')
        .size()
        .rename('total_requests')
    )

    incident_counts = (
        merged_cash_fee_cohort[merged_cash_fee_cohort['incident_flag'] == 'incident']
        .groupby('cohort_year_month')
        .size()
        .rename('incident_requests')
    )

    # 🧮 Combine and calculate rate
    incident_df = pd.concat([total_counts, incident_counts], axis=1).fillna(0)
    incident_df['incident_rate'] = (incident_df['incident_requests'] / incident_df['total_requests']).round(4)

    # ✅ Display
    safe_print("📋 Incident Rate per Cohort:")
    display(incident_df)

    # 💾 Save to CSV
    output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_incident_rate.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    incident_df.to_csv(output_path)
    safe_print(f"\n💾 Incident rate data saved to: {output_path}")

except Exception as e:
    safe_print("❌ Failed to calculate incident rate.")
    raise e


# In[18]:


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import os
import pandas as pd

safe_print("📈 Plotting annotated incident rate bar chart per cohort...")

# 🔄 Load incident rate data
incident_rate_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_incident_rate.csv')
incident_df = pd.read_csv(incident_rate_path, index_col=0)
incident_df.index = incident_df.index.astype(str)

# 📊 Plot config
plt.figure(figsize=(12, 6))
barplot = sns.barplot(
    x=incident_df.index,
    y=incident_df['incident_rate'],
    hue=incident_df.index,
    palette="OrRd",
    legend=False
)

# 🧾 Annotate each bar with its incident rate
for index, bar in enumerate(barplot.patches):
    height = bar.get_height()
    label = f"{height:.1%}"  # e.g., 25.2%
    barplot.annotate(
        label,
        (bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom',
        fontsize=9,
        color='black',
        xytext=(0, 3),
        textcoords='offset points'
    )

plt.title("Incident Rate per User Cohort", fontsize=16, pad=15)
plt.ylabel("Incident Rate")
plt.xlabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.ylim(0, incident_df['incident_rate'].max() + 0.05)
plt.grid(axis='y')

# 🔻 Mark partial months
partial_months = ['2019-11', '2020-11']
for partial_month in partial_months:
    if partial_month in incident_df.index:
        idx = list(incident_df.index).index(partial_month)
        plt.axvline(x=idx, color='red', linestyle='--', linewidth=1.5)

# 🔻 Mark start of 2020
start_2020 = '2020-01'
if start_2020 in incident_df.index:
    idx = list(incident_df.index).index(start_2020)
    plt.axvline(x=idx, color='black', linestyle='--', linewidth=1.5)

# 🧾 Custom legend
custom_lines = [
    Line2D([0], [0], color='red', linestyle='--', lw=2),
    Line2D([0], [0], color='black', linestyle='--', lw=2)
]
plt.legend(
    custom_lines,
    ['⚠️ Partial Month', '2020 Begins'],
    loc='upper right'
)

plt.tight_layout()

# 💾 Save plot
plot_filename = f"{PLOT_INDEX:02d}_cohort_incident_rate.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Incident rate chart saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()

# 🔁 Increment plot index
PLOT_INDEX += 1


# In[19]:


import pandas as pd
import os

safe_print("💰 Calculating revenue per cohort...")

# 🔄 Load merged dataset
merged_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'merged_cash_fee_cohort.csv')
merged_df = pd.read_csv(merged_path)

# 💰 Filter for accepted fees only
accepted_fees = merged_df[merged_df['fee_status'] == 'accepted']

# 🧮 Group by cohort and sum total_amount
cohort_revenue = (
    accepted_fees.groupby('cohort_year_month')['total_amount']
    .sum()
    .reset_index(name='cohort_revenue')
    .sort_values(by='cohort_year_month')
)

# ✅ Display table
safe_print("📋 Cohort Revenue:")
display(cohort_revenue)

# 💾 Save to file
revenue_output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_revenue.csv')
os.makedirs(os.path.dirname(revenue_output_path), exist_ok=True)
cohort_revenue.to_csv(revenue_output_path, index=False)
safe_print(f"💾 Revenue data saved to: {revenue_output_path}")

# 📝 Partial month note
safe_print("\n*️⃣ Note: '2019-11' and '2020-11' are partial months.\n- Nov 2019: Data starts on the 19th.\n- Nov 2020: Data ends on the 1st.\nRevenue from these cohorts is expected to be lower and should not be compared directly.")


# In[20]:


import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
from matplotlib.lines import Line2D

safe_print("📈 Plotting revenue per cohort...")

# 🔄 Load revenue data
revenue_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_revenue.csv')
revenue_df = pd.read_csv(revenue_path)

# 📊 Plot setup
plt.figure(figsize=(12, 6))
barplot = sns.barplot(
    data=revenue_df,
    x='cohort_year_month',
    y='cohort_revenue',
    color='#4c72b0'
)

# 💬 Annotate each bar with its value
for bar in barplot.patches:
    height = bar.get_height()
    label = f"€{int(height):,}"  # e.g., €11,135
    barplot.annotate(
        label,
        (bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom',
        fontsize=9,
        color='black',
        xytext=(0, 3),
        textcoords='offset points'
    )

# ⚠️ Mark partial months
partial_months = ['2019-11', '2020-11']
for partial in partial_months:
    if partial in revenue_df['cohort_year_month'].values:
        idx = revenue_df[revenue_df['cohort_year_month'] == partial].index[0]
        plt.axvline(x=idx, color='red', linestyle='--', linewidth=1.5)

# 📌 Mark beginning of 2020
if '2020-01' in revenue_df['cohort_year_month'].values:
    jan_idx = revenue_df[revenue_df['cohort_year_month'] == '2020-01'].index[0]
    plt.axvline(x=jan_idx, color='black', linestyle='--', linewidth=1.5)

# 🖼️ Titles and labels
plt.title("Total Revenue per User Cohort", fontsize=16, pad=15)
plt.ylabel("Total Revenue (€)")
plt.xlabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.grid(axis='y')

# 🧭 Custom legend
legend_lines = [
    Line2D([0], [0], color='#4c72b0', lw=4),
    Line2D([0], [0], color='red', linestyle='--', lw=2),
    Line2D([0], [0], color='black', linestyle='--', lw=2),
]
plt.legend(legend_lines, ['Revenue', '⚠️ Partial Month', '2020 Begins'], loc='upper left')

# 💾 Save plot
plot_filename = f"{PLOT_INDEX:02d}_cohort_revenue_bar.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Revenue chart saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()

# 🔁 Increment plot index
PLOT_INDEX += 1


# In[21]:


safe_print("📈 Calculating cumulative revenue over time...")

# 🔄 Load cohort revenue
revenue_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_revenue.csv')
revenue_df = pd.read_csv(revenue_path)

# 📊 Sort and compute cumulative sum
revenue_df = revenue_df.sort_values("cohort_year_month")
revenue_df["cumulative_revenue"] = revenue_df["cohort_revenue"].cumsum()

# 💾 Save the cumulative revenue table
cumulative_table_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_cumulative_revenue.csv')
os.makedirs(os.path.dirname(cumulative_table_path), exist_ok=True)
revenue_df.to_csv(cumulative_table_path, index=False)
safe_print(f"💾 Cumulative revenue table saved to: {cumulative_table_path}")

# 🖥️ Show table before plot
safe_print("📋 Cumulative Revenue by Month:")
display(revenue_df[["cohort_year_month", "cohort_revenue", "cumulative_revenue"]])

# ➕ Note about partial months
safe_print("\n*️⃣ Note: `2019-11` and `2020-11` are partial months and should be interpreted cautiously.\n")

# 📈 Plot cumulative revenue line chart
plt.figure(figsize=(12, 6))
plt.plot(revenue_df["cohort_year_month"], revenue_df["cumulative_revenue"], marker='o', linewidth=3)
plt.title("Cumulative Revenue Over Time", fontsize=16, pad=15)
plt.xlabel("Cohort (cohort_year_month)")
plt.ylabel("Cumulative Revenue (€)")
plt.xticks(rotation=45)
plt.grid(True)

# 🔻 Add vertical dashed lines for partial months and Jan 2020
partial_months = ['2019-11', '2020-11']
for month in partial_months:
    if month in revenue_df["cohort_year_month"].values:
        idx = revenue_df[revenue_df["cohort_year_month"] == month].index[0]
        plt.axvline(x=idx, color='red', linestyle='--', linewidth=1.5)

# 🎯 Mark where 2020 starts
if "2020-01" in revenue_df["cohort_year_month"].values:
    jan_idx = revenue_df[revenue_df["cohort_year_month"] == "2020-01"].index[0]
    plt.axvline(x=jan_idx, color='black', linestyle='--', linewidth=1.5)

# 📘 Legend
custom_lines = [
    plt.Line2D([0], [0], color='blue', lw=3),
    plt.Line2D([0], [0], color='red', linestyle='--', lw=2),
    plt.Line2D([0], [0], color='black', linestyle='--', lw=2)
]
plt.legend(custom_lines, ['Cumulative Revenue', '⚠️ Partial Month', '2020 Begins'])

# 💾 Save plot
plot_filename = f"{PLOT_INDEX:02d}_cohort_revenue_cumulative_line.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ Cumulative revenue chart saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()
PLOT_INDEX += 1


# In[22]:


import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd

# 💸 ARPU (Average Revenue Per User) per Cohort
safe_print("💸 Calculating ARPU (Average Revenue Per User) per cohort...")

# 📂 Define paths
revenue_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_revenue.csv')
user_map_path = os.path.join(project_base_path, 'eda_outputs', 'data', 'user_first_request.csv')

# 📥 Load revenue and user-cohort mapping
cohort_revenue = pd.read_csv(revenue_path)
user_first_request = pd.read_csv(user_map_path)

# 👥 Count users per cohort
cohort_user_counts = (
    user_first_request.groupby('cohort_year_month')
    .size()
    .reset_index(name='user_count')
)

# 🔗 Merge revenue and user counts
arpu_df = pd.merge(cohort_revenue, cohort_user_counts, on='cohort_year_month', how='left')

# 🧮 Calculate ARPU
arpu_df['arpu'] = (arpu_df['cohort_revenue'] / arpu_df['user_count']).round(2)

# 📋 Preview table
safe_print("📋 ARPU per Cohort:")
display(arpu_df)

# ➕ Note about partial months
safe_print("\n*️⃣ Note: `2019-11` and `2020-11` are partial months and should be interpreted cautiously.\n")

# 💾 Save to CSV
arpu_output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_arpu.csv')
os.makedirs(os.path.dirname(arpu_output_path), exist_ok=True)
arpu_df.to_csv(arpu_output_path, index=False)
safe_print(f"💾 ARPU data saved to: {arpu_output_path}")

# 📊 Bar plot of ARPU
plt.figure(figsize=(12, 6))
barplot = sns.barplot(data=arpu_df, x='cohort_year_month', y='arpu', color='#55a868')

# 💬 Add ARPU value labels above bars
for bar in barplot.patches:
    height = bar.get_height()
    label = f"€{height:.2f}"
    barplot.annotate(
        label,
        (bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom',
        fontsize=9,
        color='black',
        xytext=(0, 3),
        textcoords='offset points'
    )

# 📌 Titles and axes
plt.title("ARPU per User Cohort", fontsize=16, pad=15)
plt.ylabel("ARPU (€)")
plt.xlabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.grid(axis='y')

# 🔻 Mark partial months
partial_months = ['2019-11', '2020-11']
for partial in partial_months:
    if partial in arpu_df['cohort_year_month'].values:
        idx = arpu_df[arpu_df['cohort_year_month'] == partial].index[0]
        plt.axvline(x=idx, color='red', linestyle='--', linewidth=1.5)

# ⚫ Add 2020 start line
if '2020-01' in arpu_df['cohort_year_month'].values:
    idx = arpu_df[arpu_df['cohort_year_month'] == '2020-01'].index[0]
    plt.axvline(x=idx, color='black', linestyle='--', linewidth=1.5)

# 🧾 Custom legend
custom_lines = [
    plt.Line2D([0], [0], color='#55a868', lw=4),
    plt.Line2D([0], [0], color='red', linestyle='--', lw=2),
    plt.Line2D([0], [0], color='black', linestyle='--', lw=2)
]
plt.legend(custom_lines, ['ARPU', '⚠️ Partial Month', '2020 Begins'], loc='upper right')

# 💾 Save plot
plot_filename = f"{PLOT_INDEX:02d}_cohort_arpu_bar.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ ARPU chart saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()
PLOT_INDEX += 1


# In[23]:


import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
import os
import pandas as pd

# 📌 Calculate Customer Lifetime Value (CLV)
safe_print("💡 Calculating CLV (Customer Lifetime Value)...")

# 📥 Load ARPU and filtered retention matrix
arpu_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_arpu.csv')
retention_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_retention_matrix_filtered.csv')

arpu_df = pd.read_csv(arpu_path)
retention_df = pd.read_csv(retention_path, index_col=0)

# 🔢 Calculate average retention duration: count non-zero months per cohort
retention_binary = retention_df.gt(0).astype(int)
avg_retention_months = retention_binary.sum(axis=1).rename("avg_retention_months").reset_index()

# 🔗 Merge with ARPU
clv_df = arpu_df.merge(avg_retention_months, on='cohort_year_month', how='left')
clv_df['clv'] = (clv_df['arpu'] * clv_df['avg_retention_months']).round(2)

# 🧹 Exclude partial cohorts from both table and plot
partial_months = ['2019-11', '2020-11']
clv_df = clv_df[~clv_df['cohort_year_month'].isin(partial_months)]

# 💾 Save CLV table
clv_output_path = os.path.join(project_base_path, 'cohort_outputs', 'data', 'cohort_clv.csv')
clv_df.to_csv(clv_output_path, index=False)
safe_print(f"💾 CLV data saved to: {clv_output_path}")

# 📋 Preview table before plotting
safe_print("📋 CLV per Cohort:")
display(clv_df)

# 📊 Plot CLV per cohort
plt.figure(figsize=(12, 6))
barplot = sns.barplot(data=clv_df, x='cohort_year_month', y='clv', color='#4c72b0')

# 💬 Add CLV labels above bars
for bar in barplot.patches:
    height = bar.get_height()
    label = f"€{height:.2f}"
    barplot.annotate(
        label,
        (bar.get_x() + bar.get_width() / 2, height),
        ha='center',
        va='bottom',
        fontsize=9,
        color='black',
        xytext=(0, 3),
        textcoords='offset points'
    )

# 📌 Titles and axes
plt.title("Customer Lifetime Value per User Cohort", fontsize=16, pad=15)
plt.ylabel("CLV (€)")
plt.xlabel("Cohort (cohort_year_month)")
plt.xticks(rotation=45)
plt.grid(axis='y')

# 🔻 Mark start of 2020 (centered on '2020-01')
if '2020-01' in clv_df['cohort_year_month'].values:
    x_labels = list(clv_df['cohort_year_month'])
    x_pos = x_labels.index('2020-01')
    plt.axvline(x=x_pos, color='black', linestyle='--', linewidth=1.5)

# 🧾 Custom legend
custom_lines = [
    Line2D([0], [0], color='#4c72b0', lw=4),
    Line2D([0], [0], color='black', linestyle='--', lw=2),
]
plt.legend(custom_lines, ['CLV', '2020 Begins'], loc='upper right')

# 💾 Save plot
plot_filename = f"{PLOT_INDEX:02d}_cohort_clv_bar.png"
plot_path = os.path.join(project_base_path, 'cohort_outputs', 'plots', plot_filename)
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

if OVERWRITE_PLOTS or not os.path.exists(plot_path):
    plt.savefig(plot_path)
    safe_print(f"✅ CLV chart saved to: {plot_path}")
else:
    safe_print(f"⚠️ Skipped saving – file already exists: {plot_path}")

plt.show()
PLOT_INDEX += 1


# In[24]:


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
