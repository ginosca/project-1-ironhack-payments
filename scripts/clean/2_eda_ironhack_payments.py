# 📊 Exploratory Data Analysis Script – Ironhack Payments
# 📓 Source Notebook: 2_eda_ironhack_payments.ipynb
# 🔍 Description: Analyzes cleaned data, visualizes user behavior, and prepares cohort aggregates.
# 📅 Date: December 13, 2024
# 👩‍💻 Author: Ginosca Alejandro Dávila
# 🛠️ Bootcamp: Ironhack Data Science and Machine Learning

#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

    # ✅ Try default path first
    default_path = 'MyDrive/Colab Notebooks/Ironhack/Week 2/Week 2 - Day 4/project-1-ironhack-payments-2-en'
    full_default_path = os.path.join('/content/drive', default_path)

    if os.path.exists(full_default_path):
        project_base_path = full_default_path
        safe_print(f"✅ Colab project path set to: {project_base_path}")
    else:
        # Ask for user input if default fails
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

    # ✅ Assume script is inside /scripts/ and go two levels up
    project_base_path = os.path.abspath(os.path.join(script_dir, '..', '..'))
    safe_print(f"✅ Local environment detected. Base path set to: {project_base_path}")


# In[3]:


# 📦 Import core libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# 🧼 Aesthetic setup for plots
plt.style.use("ggplot")
sns.set_palette("pastel")

# 📁 Define paths to the cleaned datasets using project_base_path
cash_path = os.path.join(project_base_path, 'cleaned_project_datasets', 'clean_cash_requests.csv')
fees_path = os.path.join(project_base_path, 'cleaned_project_datasets', 'clean_fees.csv')

# 📥 Load the data with error handling
try:
    cash_df = pd.read_csv(cash_path, parse_dates=True)
    fees_df = pd.read_csv(fees_path, parse_dates=True)
    safe_print("✅ Cleaned datasets loaded successfully.")
    safe_print(f"cash_df shape: {cash_df.shape}")
    safe_print(f"fees_df shape: {fees_df.shape}")
except FileNotFoundError as e:
    safe_print(f"❌ File not found: {e}")
    sys.exit(1)  # Exit the script gracefully if file is missing


# In[4]:


# ✅ Define display fallback for script environments
try:
    display
except NameError:
    def display(x):
        safe_print(x.to_string() if isinstance(x, pd.DataFrame) else x)

# 📏 Configure Pandas to show full width and content
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 100)

# 🧾 First and last 5 rows of cash_df
safe_print("🔍 First 5 rows of cash_df:")
display(cash_df.head())

safe_print("🔍 Last 5 rows of cash_df:")
display(cash_df.tail())

# 📊 Data types and nulls for cash_df
safe_print("\n📊 Structure of cash_df:")
cash_df.info()

# 🔍 Missing values in cash_df
safe_print("\n🧼 Missing values in cash_df:")
display(cash_df.isnull().sum())


# In[5]:


# 🧾 First and last 5 rows of fees_df
safe_print("🔍 First 5 rows of fees_df:")
display(fees_df.head())

safe_print("🔍 Last 5 rows of fees_df:")
display(fees_df.tail())

# 📊 Data types and nulls for fees_df
safe_print("\n📊 Structure of fees_df:")
fees_df.info()

# 🔍 Missing values in fees_df
safe_print("\n🧼 Missing values in fees_df:")
display(fees_df.isnull().sum())


# In[6]:


# Summary stats for numerical columns
safe_print("🔢 Summary statistics for `cash_df['amount']`")
display(cash_df['amount'].describe())

safe_print("\n🔢 Summary statistics for `fees_df['total_amount']`")
display(fees_df['total_amount'].describe())


# In[7]:


import seaborn as sns
import matplotlib.pyplot as plt
import os

# 📊 Set seaborn plot style
sns.set(style="whitegrid")

# ✅ Config toggles
SAVE_PLOTS = True
OVERWRITE_PLOTS = True
plot_index = 1

# 📁 Ensure plot directory exists
eda_plot_path = os.path.join(project_base_path, 'eda_outputs', 'plots')
os.makedirs(eda_plot_path, exist_ok=True)

# 🧭 Quick tip: confirm save location
safe_print(f"🧭 Plot outputs will be saved to: {eda_plot_path}")

# 🔠 Helper to annotate barplot counts
def annotate_counts(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9)

# 🗂️ Categorical variables to analyze
categorical_cash = ['status', 'transfer_type', 'recovery_status']
categorical_fees = ['type', 'status', 'category', 'charge_moment']

# 🧼 Columns to replace NaN with 'missing'
replace_nan_cash = ['recovery_status']
replace_nan_fees = ['category']

# 📊 Plot cash_df categorical variables
for col in categorical_cash:
    safe_print(f"📊 Value counts for cash_df['{col}']:\n")
    temp_col = cash_df[col].fillna("missing") if col in replace_nan_cash else cash_df[col]
    counts = temp_col.value_counts(dropna=False)
    display(counts)

    plt.figure(figsize=(10, 4))
    ax = sns.countplot(x=temp_col, order=counts.index)
    plt.title(f'Distribution of {col}')
    plt.xticks(rotation=45)
    plt.ylim(0, counts.max() * 1.1)
    annotate_counts(ax)
    plt.tight_layout()

    if SAVE_PLOTS:
        filename = f"{plot_index:02d}_distribution_cash_{col}.png"
        filepath = os.path.join(eda_plot_path, filename)
        if OVERWRITE_PLOTS or not os.path.exists(filepath):
            plt.savefig(filepath)
            safe_print(f"✅ Saved: {filename}")
        else:
            safe_print(f"⚠️ Skipped (already exists): {filename}")
    plot_index += 1
    plt.show()

# 📊 Plot fees_df categorical variables
for col in categorical_fees:
    safe_print(f"📊 Value counts for fees_df['{col}']:\n")
    temp_col = fees_df[col].fillna("missing") if col in replace_nan_fees else fees_df[col]
    counts = temp_col.value_counts(dropna=False)
    display(counts)

    plt.figure(figsize=(10, 4))
    ax = sns.countplot(x=temp_col, order=counts.index)
    plt.title(f'Distribution of {col}')
    plt.xticks(rotation=45)
    plt.ylim(0, counts.max() * 1.1)
    annotate_counts(ax)
    plt.tight_layout()

    if SAVE_PLOTS:
        filename = f"{plot_index:02d}_distribution_fees_{col}.png"
        filepath = os.path.join(eda_plot_path, filename)
        if OVERWRITE_PLOTS or not os.path.exists(filepath):
            plt.savefig(filepath)
            safe_print(f"✅ Saved: {filename}")
        else:
            safe_print(f"⚠️ Skipped (already exists): {filename}")
    plot_index += 1
    plt.show()


# In[8]:


# --- 📊 Merged Chart: Cash Requests Volume and Amount Over Time ---

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# 1. Ensure datetime is parsed
cash_df['created_at'] = pd.to_datetime(cash_df['created_at'], errors='coerce')
cash_df['year_month'] = cash_df['created_at'].dt.to_period('M')
cash_df['month_label'] = cash_df['created_at'].dt.strftime('%b %Y')

# 2. Group and merge volume + amount
monthly_requests = (
    cash_df.groupby(['year_month', 'month_label'])
    .size()
    .reset_index(name='cash_requests')
)

monthly_amount = (
    cash_df.groupby(['year_month', 'month_label'])['amount']
    .sum()
    .reset_index()
)

monthly_summary = pd.merge(monthly_requests, monthly_amount, on=['year_month', 'month_label'])
monthly_summary = monthly_summary.sort_values(by='year_month')

# 3. Mark partial months
monthly_summary['month_label'] = monthly_summary['month_label'].replace({
    'Nov 2019': 'Nov 2019*',
    'Nov 2020': 'Nov 2020*'
})

# 4. Format amount column with € symbol for table
formatted_table = monthly_summary.copy()
formatted_table['amount'] = formatted_table['amount'].apply(lambda x: f"€{x:,.0f}")
safe_print("📊 Monthly Cash Requests and Amount Requested:")
display(formatted_table[['year_month', 'month_label', 'cash_requests', 'amount']])
safe_print("\n(*) Partial months: Nov 2019 starts on 19th, Nov 2020 ends on 1st.")

# 5. Plot dual-axis chart
fig, ax1 = plt.subplots(figsize=(14, 6))

# Left Y-axis: Number of Requests
line1, = ax1.plot(
    monthly_summary['month_label'],
    monthly_summary['cash_requests'],
    marker='o',
    color='blue',
    label='Cash Requests'
)
ax1.set_ylabel('Number of Cash Requests', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xlabel('Month')
ax1.set_ylim(0, monthly_summary['cash_requests'].max() * 1.1)
ax1.yaxis.set_major_locator(plt.MaxNLocator(integer=True, nbins=6))

# Right Y-axis: Total Amount (€)
ax2 = ax1.twinx()
line2, = ax2.plot(
    monthly_summary['month_label'],
    monthly_summary['amount'],
    marker='o',
    color='green',
    label='Total Requested (€)'
)
ax2.set_ylabel('Total Amount Requested (€)', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Smooth right axis ticks
ax2.set_ylim(0, monthly_summary['amount'].max() * 1.1)
ax2.yaxis.set_major_formatter(mtick.StrMethodFormatter('€{x:,.0f}'))

# Red dashed lines for partial months
partial_months = ['Nov 2019*', 'Nov 2020*']
for i, pm in enumerate(partial_months):
    idx = monthly_summary[monthly_summary['month_label'] == pm].index
    if not idx.empty:
        ax1.axvline(
            x=idx[0],
            color='red',
            linestyle='--',
            linewidth=1.5,
            alpha=0.7,
            label='⚠️ Partial Month' if i == 0 else None
        )

# Dashed line for Jan 2020
jan_idx = monthly_summary[monthly_summary['month_label'] == 'Jan 2020'].index
if not jan_idx.empty:
    ax1.axvline(
        x=jan_idx[0],
        color='black',
        linestyle='--',
        linewidth=1,
        alpha=0.8
    )
    ax1.text(jan_idx[0]+0.3, ax1.get_ylim()[1]*0.9, '2020 begins', fontsize=9, color='gray')

# Title and layout
plt.title('Monthly Cash Request Volume and Total Requested Amount')
ax1.set_xticks(range(len(monthly_summary)))
ax1.set_xticklabels(monthly_summary['month_label'], rotation=45)
plt.grid(True, which='both', axis='y', linestyle='--', alpha=0.5)
fig.tight_layout()

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.show()

# 💾 Save the figure
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_monthly_cash_requests_dual_axis.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        fig.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1


# In[9]:


# --- 👤 User-Level Behavior – Cash Request Frequency ---

# 1. Count number of requests per user
user_request_counts = cash_df['final_user_id'].value_counts().reset_index()
user_request_counts.columns = ['final_user_id', 'request_count']

# 2. Show summary stats
safe_print("📊 Request count summary per user:")
display(user_request_counts['request_count'].describe())

# 3. Calculate single vs. multi-use users
single_use = (user_request_counts['request_count'] == 1).sum()
multi_use = (user_request_counts['request_count'] > 1).sum()
total_users = user_request_counts.shape[0]

safe_print(f"🧍‍♂️ Single-use users: {single_use:,} ({single_use / total_users:.2%})")
safe_print(f"🧍‍♀️ Multi-use users: {multi_use:,} ({multi_use / total_users:.2%})")
safe_print(f"📌 Total unique users: {total_users:,}")

# 4. Prepare frequency table for plotting
request_freq = user_request_counts['request_count'].value_counts().sort_index()
request_freq_df = request_freq.reset_index()
request_freq_df.columns = ['request_count', 'user_count']
request_freq_df['request_count_str'] = request_freq_df['request_count'].astype(str)  # Convert to string for categorical axis

# 5. Display table
safe_print("\n📋 Frequency Table: Number of Users per Request Count")
display(request_freq_df)

# 6. Plot with x-ticks as categories (strings) to ensure all are shown
plt.figure(figsize=(12, 5))
ax = sns.barplot(data=request_freq_df, x='request_count_str', y='user_count', color='skyblue')

plt.title("Distribution of Cash Requests per User")
plt.xlabel("Number of Requests")
plt.ylabel("Number of Users")
plt.grid(True, axis='y')

# 7. Annotate bar tops
for bar in ax.patches:
    height = bar.get_height()
    if height > 0:
        ax.annotate(f'{int(height)}',
                    (bar.get_x() + bar.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# 8. Save plot if enabled
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_user_request_frequency.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
        plot_index += 1
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
else:
    plot_index += 1

plt.show()


# In[10]:


# --- ⚠️ Distribution of recovery_status in cash_df ---

# 1. Replace NaN with "missing" for visualization
cash_df['recovery_status_clean'] = cash_df['recovery_status'].fillna("missing")

# 2. Calculate value counts and percentages
recovery_counts = cash_df['recovery_status_clean'].value_counts()
recovery_percent = recovery_counts / len(cash_df) * 100

# 3. Display tables
safe_print("📊 Recovery Status Counts:")
display(recovery_counts.to_frame(name='count'))

safe_print("\n📈 Recovery Status Percentage:")
display(recovery_percent.round(2).to_frame(name='proportion'))

# 4. Plot the distribution without triggering future warning
plt.figure(figsize=(10, 5))
ax = sns.countplot(
    data=cash_df,
    x='recovery_status_clean',
    hue='recovery_status_clean',
    order=recovery_counts.index,
    palette='muted',
    legend=False
)
plt.title("Recovery Status Distribution")
plt.xlabel("Recovery Status")
plt.ylabel("Number of Cash Requests")

# Annotate bar tops
for bar in ax.patches:
    height = bar.get_height()
    ax.annotate(f'{height:.1f}', (bar.get_x() + bar.get_width() / 2., height),
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()

# 5. Save plot if enabled
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_recovery_status_distribution.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
        plot_index += 1
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
else:
    plot_index += 1

plt.show()


# In[11]:


# --- ⚠️ Incident Trends Over Time ---

# 1. Prepare datetime field (already done earlier, safe to repeat)
cash_df['created_at'] = pd.to_datetime(cash_df['created_at'], errors='coerce')
cash_df['year_month'] = cash_df['created_at'].dt.to_period('M')

# 2. Classify incident status
cash_df['incident_flag'] = np.where(cash_df['recovery_status'].notna(), 'incident', 'no_incident')

# 3. Group by month and incident_flag
incident_trend = (
    cash_df
    .groupby(['year_month', 'incident_flag'])
    .size()
    .reset_index(name='count')
)

# 4. Pivot table for incident counts
incident_pivot = incident_trend.pivot(index='year_month', columns='incident_flag', values='count').fillna(0)

# 5. Prepare table for display
incident_table = incident_pivot.copy()
incident_table['Incident Ratio (%)'] = (
    incident_table['incident'] / (incident_table['incident'] + incident_table['no_incident'])
) * 100
incident_table = incident_table.reset_index()
incident_table['Month'] = incident_table['year_month'].dt.strftime('%b %Y')

# 6. Mark partial months
incident_table['Month'] = incident_table['Month'].replace({
    'Nov 2019': 'Nov 2019*',
    'Nov 2020': 'Nov 2020*'
})

# 7. Select and rename columns
incident_table = incident_table[['Month', 'incident', 'no_incident', 'Incident Ratio (%)']]
incident_table.columns = ['Month', 'Incident Requests', 'Non-Incident Requests', 'Incident Ratio (%)']

# 8. Display table
safe_print("📊 Monthly Incident Request Breakdown:")
display(incident_table)

# 9. Partial month note
safe_print("\n*️⃣ Note: Months marked with * are partial months.\n- Nov 2019: Data starts from November 19th.\n- Nov 2020: Data available only up to November 1st.")

# 10. Plot
fig, ax = plt.subplots(figsize=(14, 6))
incident_pivot.plot(kind='bar', stacked=True, color=['#4c72b0', '#dd8452'], ax=ax)

# Dashed lines for partial months
partial_months = {'2019-11': 'Nov 2019*', '2020-11': 'Nov 2020*'}
for month_period, label in partial_months.items():
    idx = incident_pivot.index.get_loc(pd.Period(month_period, freq='M'))
    ax.axvline(x=idx, color='red', linestyle='--', linewidth=1.5)

# Dashed line for Jan 2020
jan_2020_period = pd.Period('2020-01', freq='M')
if jan_2020_period in incident_pivot.index:
    jan_idx = incident_pivot.index.get_loc(jan_2020_period)
    ax.axvline(x=jan_idx, color='black', linestyle='--', linewidth=1.5)

# Titles and formatting
ax.set_title('Monthly Cash Requests: Incident vs. Non-Incident')
ax.set_ylabel('Number of Requests')
ax.set_xlabel('Month')
ax.set_xticklabels(incident_pivot.index.strftime('%b %Y'), rotation=45)
ax.grid(True, axis='y')

# Custom legend
custom_lines = [
    plt.Line2D([0], [0], color='#4c72b0', lw=4),
    plt.Line2D([0], [0], color='#dd8452', lw=4),
    plt.Line2D([0], [0], color='red', linestyle='--', lw=2),
    plt.Line2D([0], [0], color='black', linestyle='--', lw=2)
]
ax.legend(custom_lines, ['Non-Incident Requests', 'Incident Requests', '⚠️ Partial Month', '2020 Begins'], loc='upper left')

plt.tight_layout()

# 11. Save plot
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_monthly_incident_trends.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        fig.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
        plot_index += 1
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
else:
    plot_index += 1

plt.show()


# In[12]:


# --- 💸 Fees Overview ---

import seaborn as sns
import matplotlib.pyplot as plt

# 1. Columns to check
fee_cols = ['type', 'status', 'category', 'charge_moment']

# 2. Function to annotate counts
def annotate_counts(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=8)

# 3. Loop through each categorical column
for col in fee_cols:
    safe_print(f"\n📊 Value Counts for '{col}':")
    temp_col = fees_df[col].fillna('missing')
    display(temp_col.value_counts())

    # Plot
    plt.figure(figsize=(8, 4))
    ax = sns.countplot(
        x=temp_col,
        hue=temp_col,
        palette='pastel',
        legend=False,
        order=temp_col.value_counts().index
    )
    annotate_counts(ax)
    plt.title(f'Distribution of {col}')
    plt.xlabel(col.capitalize())
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    plt.tight_layout()

    # Save plot
    if SAVE_PLOTS:
        filename = f"{plot_index:02d}_fees_distribution_{col}.png"
        filepath = os.path.join(eda_plot_path, filename)
        if OVERWRITE_PLOTS or not os.path.exists(filepath):
            plt.savefig(filepath)
            safe_print(f"✅ Saved: {filename}")
        else:
            safe_print(f"⚠️ Skipped (already exists): {filename}")
    plot_index += 1

    plt.show()


# In[13]:


# --- 💸 Total Revenue by Fee Type ---

import matplotlib.pyplot as plt
import seaborn as sns

# 1. Group by type and sum total_amount
revenue_by_type = (
    fees_df
    .groupby('type')['total_amount']
    .sum()
    .reset_index()
    .sort_values(by='total_amount', ascending=False)
)

# 2. Display table
safe_print("📊 Total Revenue by Fee Type:")
display(revenue_by_type)

# 3. Plot grouped bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=revenue_by_type,
    x='type',
    y='total_amount',
    hue='type',  # ✅ Explicit hue to avoid future warnings
    legend=False,
    palette='pastel'
)

plt.title('Total Revenue by Fee Type')
plt.xlabel('Fee Type')
plt.ylabel('Total Revenue (Assumed €)')
plt.grid(axis='y')

# Annotate bar tops
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f'{height:,.0f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# 💾 Save plot
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_revenue_by_fee_type.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[14]:


# --- 💸 Total Revenue by Fee Type and Charge Moment ---

# 1. Group by type and charge_moment, summing total_amount
fee_revenue = (
    fees_df
    .groupby(['type', 'charge_moment'])['total_amount']
    .sum()
    .reset_index()
)

# 2. Display table
safe_print("📊 Total Revenue by Fee Type and Charge Moment:")
display(fee_revenue)

# 3. Plot grouped bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    data=fee_revenue,
    x='type',
    y='total_amount',
    hue='charge_moment',
    palette='pastel'
)

plt.title('Total Revenue by Fee Type and Charge Moment')
plt.xlabel('Fee Type')
plt.ylabel('Total Revenue (Assumed €)')
plt.grid(axis='y')

# Annotate bar tops
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(f'{height:,.0f}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# 💾 Save plot
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_revenue_by_type_and_charge_moment.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[15]:


# --- 📊 Frequency of Fee Amounts ---

# 1. Count frequencies of total_amount
amount_counts = fees_df['total_amount'].value_counts().sort_index()

# 2. Create a DataFrame for easy table display
amount_counts_df = amount_counts.reset_index()
amount_counts_df.columns = ['Total Amount (€)', 'Frequency']

# 3. Display table
safe_print("📋 Frequency of Fee Amounts:")
display(amount_counts_df)

# 4. Plot bar chart
plt.figure(figsize=(8, 5))
ax = sns.barplot(
    data=amount_counts_df,
    x='Total Amount (€)',
    y='Frequency',
    hue='Total Amount (€)',  # Avoids future warning
    palette='pastel',
    legend=False
)

# 5. Annotate bar tops
for i in range(amount_counts_df.shape[0]):
    plt.text(x=i,
             y=amount_counts_df.loc[i, 'Frequency'] + 50,
             s=f"{amount_counts_df.loc[i, 'Frequency']}",
             ha='center', va='bottom', fontsize=9)

# 6. Title and labels
plt.title('Frequency of Fee Amounts (€5 vs €10)')
plt.xlabel('Fee Amount (€)')
plt.ylabel('Number of Occurrences')
plt.xticks(rotation=0)
plt.grid(axis='y')

# 7. Save plot if needed
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_fee_amount_frequencies.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

# 8. Adjust layout and show
plt.tight_layout()
plt.show()


# In[16]:


# --- 🔗 Rename Overlapping Columns Before Merging ---

# 1. Rename columns in cash_df
cash_df = cash_df.rename(columns={
    'id': 'cash_request_id',
    'created_at': 'cash_created_at',
    'updated_at': 'cash_updated_at',
    'status': 'cash_status'
})

# 2. Rename columns in fees_df
fees_df = fees_df.rename(columns={
    'id': 'fee_id',
    'created_at': 'fee_created_at',
    'updated_at': 'fee_updated_at',
    'status': 'fee_status'
})

# ✅ Confirm renaming
safe_print("✅ Renaming complete. Updated columns:")

safe_print("\n📂 cash_df columns:")
safe_print(cash_df.columns.tolist())

safe_print("\n📂 fees_df columns:")
safe_print(fees_df.columns.tolist())


# In[17]:


# --- 🔗 Linking Fees to Cash Requests ---

# 1. Perform the merge
# I am doing a LEFT JOIN to keep all cash requests even if no fee is linked
merged_df = cash_df.merge(
    fees_df,
    how='left',
    left_on='cash_request_id',
    right_on='cash_request_id',
    suffixes=('_cash', '_fee')  # extra safety, although columns were renamed
)

# 2. Check merge results
safe_print("✅ Merge complete. New merged dataset structure:")
safe_print(f"📂 merged_df shape: {merged_df.shape}")

# 3. Quick verification after merge

# Total cash requests
total_cash_requests = merged_df['cash_request_id'].nunique()

# Cash requests with at least one fee (type is not null)
cash_requests_with_fees = merged_df[merged_df['type'].notna()]['cash_request_id'].nunique()

# Print summary
safe_print(f"\n📊 Quick Summary After Merge:")
safe_print(f"📌 Total Cash Requests: {total_cash_requests:,}")
safe_print(f"📌 Cash Requests with at least one fee: {cash_requests_with_fees:,}")
safe_print(f"📌 Percentage with at least one fee: {cash_requests_with_fees / total_cash_requests:.2%}")

# 4. Preview a few rows
display(merged_df.head())


# In[18]:


# --- 📊 Analyzing Relationships Between Cash Request Status and Fee Type ---

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Create a pivot table (cross-tab) between cash_status and fee type
status_fee_pivot = (
    merged_df
    .pivot_table(
        index='cash_status',  # cash request status (e.g., money_back, rejected)
        columns='type',       # fee type (e.g., instant_payment, postpone, incident)
        values='fee_id',      # count of fees (fee_id is not null if a fee exists)
        aggfunc='count',      # counting number of fees
        fill_value=0
    )
)

# 2. Display the table
safe_print("📋 Pivot Table: Cash Request Status vs Fee Type")
display(status_fee_pivot)

# 3. Plot heatmap
plt.figure(figsize=(10, 6))
ax = sns.heatmap(status_fee_pivot, annot=True, fmt='d', cmap='Blues', linewidths=0.5)
plt.title("Heatmap: Fee Types by Cash Request Status")
plt.xlabel("Fee Type")
plt.ylabel("Cash Request Status")
plt.tight_layout()

if SAVE_PLOTS:
    filename = f"{plot_index:02d}_heatmap_cash_status_vs_fee_type.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[19]:


# --- 💰 Total Revenue by Cash Request Status ---

# 1. Group by cash_status and sum total_amount
revenue_by_status = (
    merged_df
    .groupby('cash_status')['total_amount']
    .sum()
    .reset_index()
    .sort_values(by='total_amount', ascending=False)
)

# 2. Fill NaNs (no associated fees) with 0
revenue_by_status['total_amount'] = revenue_by_status['total_amount'].fillna(0)

# 3. Rename columns for clarity
revenue_by_status.columns = ['Cash Request Status', 'Total Revenue (€)']

# 4. Display table
safe_print("📋 Total Revenue by Cash Request Status:")
display(revenue_by_status)

# 5. Plot bar chart
plt.figure(figsize=(12, 6))
bars = plt.bar(revenue_by_status['Cash Request Status'], revenue_by_status['Total Revenue (€)'], color='lightblue')

# Annotate bar tops
for bar in bars:
    height = bar.get_height()
    plt.annotate(f'{height:,.0f}',
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 5),
                 textcoords="offset points",
                 ha='center', va='bottom', fontsize=9)

plt.title('Total Revenue by Cash Request Status')
plt.ylabel('Total Revenue (Assumed €)')
plt.xlabel('Cash Request Status')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()

# 💾 Save plot
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_revenue_by_cash_status.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[20]:


# --- 📆 First Cash Request Date per User ---

# 1. Ensure cash_created_at is datetime
cash_df['cash_created_at'] = pd.to_datetime(cash_df['cash_created_at'], errors='coerce')

# 2. Group by final_user_id and find the first request date
user_first_request = (
    cash_df
    .groupby('final_user_id')['cash_created_at']
    .min()
    .reset_index()
    .rename(columns={'cash_created_at': 'first_request_date'})
)

# 3. Create human-readable and sortable cohort columns
user_first_request['cohort_month'] = user_first_request['first_request_date'].dt.strftime('%b %Y')   # e.g., 'Jan 2020'
user_first_request['cohort_year_month'] = user_first_request['first_request_date'].dt.to_period('M').astype(str)  # e.g., '2020-01'

# 4. Display sample
safe_print("📋 First Cash Request Date and Cohort Month per User:")
display(user_first_request.head())

# 5. Basic Summary
safe_print(f"📊 Total unique users identified: {user_first_request.shape[0]:,}")


# In[21]:


# --- 📈 Monthly Active Users (MAU) ---

import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Ensure datetime
cash_df['cash_created_at'] = pd.to_datetime(cash_df['cash_created_at'], errors='coerce')

# 2. Extract month
cash_df['activity_month'] = cash_df['cash_created_at'].dt.to_period('M')

# 3. Group by activity month
monthly_active_users = (
    cash_df
    .groupby('activity_month')['final_user_id']
    .nunique()
    .reset_index()
    .rename(columns={'final_user_id': 'active_users'})
)

# 4. Format month
monthly_active_users['activity_month_str'] = monthly_active_users['activity_month'].dt.strftime('%b %Y')

# 5. Mark partial months in table
table_to_display = monthly_active_users[['activity_month_str', 'active_users']].copy()
table_to_display['activity_month_str'] = table_to_display['activity_month_str'].replace({
    'Nov 2019': 'Nov 2019*',
    'Nov 2020': 'Nov 2020*'
})

# 6. Display table
safe_print("📊 Monthly Active Users (MAU):")
display(table_to_display)

safe_print("\n*️⃣ Note: Months marked with * are partial months.")
safe_print("- Nov 2019: Data starts from November 19th.")
safe_print("- Nov 2020: Data available only up to November 1st.")

# 7. Plot
plt.figure(figsize=(12, 6))
ax = plt.gca()
plt.plot(table_to_display['activity_month_str'], monthly_active_users['active_users'], marker='o', color='orange', label='Active Users')
plt.title('Monthly Active Users (MAU)')
plt.xlabel('Month')
plt.ylabel('Active Users')
plt.xticks(rotation=45)

# Jan 2020 marker
if 'Jan 2020' in table_to_display['activity_month_str'].values:
    jan_2020_idx = table_to_display[table_to_display['activity_month_str'] == 'Jan 2020'].index[0]
    plt.axvline(x=jan_2020_idx, color='black', linestyle='--', linewidth=1)
    plt.text(jan_2020_idx + 0.2, plt.ylim()[1]*0.95, '2020 begins', fontsize=9, color='gray')

# Add only one red line to legend for partial month
partial_months = ['Nov 2019*', 'Nov 2020*']
for i, partial_month in enumerate(partial_months):
    if partial_month in table_to_display['activity_month_str'].values:
        idx = table_to_display[table_to_display['activity_month_str'] == partial_month].index[0]
        ax.axvline(
            x=idx, color='red', linestyle='--', linewidth=1.5,
            label='⚠️ Partial Month' if i == 0 else None
        )

# Show legend
handles, labels = ax.get_legend_handles_labels()
if handles:
    plt.legend()

plt.grid(True)
plt.tight_layout()

# 💾 Save plot
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_monthly_active_users.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        plt.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[22]:


# --- 🚀 Instant vs Regular Transfers and Instant Share (%) ---

import matplotlib.pyplot as plt

# 1. Ensure datetime
cash_df['cash_created_at'] = pd.to_datetime(cash_df['cash_created_at'], errors='coerce')

# 2. Create year_month and month_label
cash_df['year_month'] = cash_df['cash_created_at'].dt.to_period('M')
cash_df['month_label'] = cash_df['cash_created_at'].dt.strftime('%b %Y')

# 3. Group by year_month and transfer_type
transfer_counts = (
    cash_df
    .groupby(['year_month', 'month_label', 'transfer_type'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
    .sort_values('year_month')
)

# 4. Calculate instant share (%)
transfer_counts['instant_share_percent'] = (
    transfer_counts['instant'] / (transfer_counts['instant'] + transfer_counts['regular'])
) * 100

# 5. Mark partial months with *
transfer_counts['month_label'] = transfer_counts['month_label'].replace({
    'Nov 2019': 'Nov 2019*',
    'Nov 2020': 'Nov 2020*'
})

# 6. Display final table
safe_print("📋 Monthly Instant vs Regular Transfer Counts and Instant Share (%):")
display(transfer_counts[['month_label', 'instant', 'regular', 'instant_share_percent']])
safe_print("\n*️⃣ Note: Months marked with * are partial months.\n- Nov 2019: Data starts from November 19th.\n- Nov 2020: Data available only up to November 1st.")

# 7. Plot
fig, ax1 = plt.subplots(figsize=(14, 6))

# Left Y-axis: Number of transfers
line1, = ax1.plot(transfer_counts['month_label'], transfer_counts['instant'], marker='o', label='Instant Transfers', color='blue')
line2, = ax1.plot(transfer_counts['month_label'], transfer_counts['regular'], marker='o', label='Regular Transfers', color='orange')
ax1.set_ylabel('Number of Transfers')
ax1.set_xlabel('Month')
ax1.set_title('Instant vs Regular Transfers and Instant Share (%)')
ax1.tick_params(axis='y')
ax1.grid(True)

# Right Y-axis: Instant share %
ax2 = ax1.twinx()
line3, = ax2.plot(transfer_counts['month_label'], transfer_counts['instant_share_percent'], marker='o', color='green', label='Instant Share (%)')
ax2.set_ylabel('Instant Share (%)', color='green')
ax2.set_ylim(0, 100)
ax2.tick_params(axis='y', labelcolor='green')

# Partial months (only one in legend)
partial_months = ['Nov 2019*', 'Nov 2020*']
for i, pm in enumerate(partial_months):
    idx = transfer_counts[transfer_counts['month_label'] == pm].index
    if not idx.empty:
        ax1.axvline(
            x=idx[0],
            color='red',
            linestyle='--',
            linewidth=1.5,
            alpha=0.7,
            label='⚠️ Partial Month' if i == 0 else None
        )

# Jan 2020 reference
if 'Jan 2020' in transfer_counts['month_label'].values:
    jan_idx = transfer_counts[transfer_counts['month_label'] == 'Jan 2020'].index[0]
    ax1.axvline(x=jan_idx, color='black', linestyle='--', linewidth=1)
    ax1.text(jan_idx + 0.2, ax1.get_ylim()[1]*0.95, '2020 begins', fontsize=9, color='gray')

# Rotate x-axis labels
plt.xticks(rotation=45)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()

# 💾 Save figure
if SAVE_PLOTS:
    filename = f"{plot_index:02d}_transfers_instant_vs_regular.png"
    filepath = os.path.join(eda_plot_path, filename)
    if OVERWRITE_PLOTS or not os.path.exists(filepath):
        fig.savefig(filepath)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")
plot_index += 1

plt.show()


# In[23]:


# --- 💾 Save Final EDA Aggregates ---

import os

# ✅ Config toggle: allow or prevent overwriting CSVs
OVERWRITE_CSV = True

# 📁 Define and ensure eda_outputs/data folder exists
eda_data_path = os.path.join(project_base_path, 'eda_outputs', 'data')
os.makedirs(eda_data_path, exist_ok=True)

# 🧭 Output directory note
safe_print(f"🧭 CSV outputs will be saved to: {eda_data_path}")

# 🔁 Helper function to save CSVs safely
def save_csv_if_allowed(df, filename):
    filepath = os.path.join(eda_data_path, filename)
    if OVERWRITE_CSV or not os.path.exists(filepath):
        df.to_csv(filepath, index=False)
        safe_print(f"✅ Saved: {filename}")
    else:
        safe_print(f"⚠️ Skipped (already exists): {filename}")

# 💾 Save User First Request Cohort Mapping
save_csv_if_allowed(user_first_request, 'user_first_request.csv')

# 💾 Save Monthly Active Users
save_csv_if_allowed(monthly_active_users, 'monthly_active_users.csv')

# 💾 Save Transfer Type Share per Month
save_csv_if_allowed(
    transfer_counts[['month_label', 'instant', 'regular', 'instant_share_percent']],
    'transfer_type_share.csv'
)

# 💾 Save Merged Dataset (Cash Requests + Fees linked)
save_csv_if_allowed(merged_df, 'merged_cash_fee.csv')


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
