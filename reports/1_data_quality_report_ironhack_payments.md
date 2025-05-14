
# 🧼 Data Quality Analysis Report  
### 📊 Project: Cohort Analysis for Ironhack Payments  
📅 Date: December 12, 2024  
👩‍💻 Author: Ginosca Alejandro Dávila  

---

## 📌 Overview

This report documents the **data quality review and cleaning process** applied to the datasets provided by Ironhack Payments, as part of a larger cohort analysis project. The data cleaning phase was implemented in the notebook `1_data_cleaning_ironhack_payments.ipynb`.

---

## 📂 Datasets Reviewed

| Dataset Name | Description |
|--------------|-------------|
| `cash_df`    | Cash request records including user identifiers, statuses, timestamps, and reimbursement lifecycle details |
| `fees_df`    | Fee records linked to cash requests, including fee types, statuses, amounts, charge timing, and timestamps |

---

## 🔍 Key Quality Dimensions Reviewed

### 1. ✅ **Duplicate Records**
- **`cash_df`**: No fully duplicated rows or duplicate `id` values found.
- **`fees_df`**: No fully duplicated rows or duplicate `id` values found.

➡️ **Conclusion**: ✅ No action required.

---

### 2. 📉 **Missing Values**

#### `cash_df`:

| Column                    | % Missing | Notes |
|---------------------------|-----------|-------|
| `deleted_account_id`      | 91.2%     | Expected – only used when a user deletes their account |
| `reimbursement_date`      | 87.3%     | Acceptable – mostly missing for requests that were reimbursed, rejected, or canceled |
| `reco_last_update`        | 86.1%     | Expected – only used in incident recovery flow |
| `money_back_date`         | 49.7%     | Acceptable – missing when funds haven't been confirmed as reimbursed |
| `moderated_at`            | 33.6%     | Acceptable – only filled for manually reviewed requests |
| `cash_request_received_date`, `send_at` | ~32% | Acceptable – depends on request lifecycle |
| `user_id`                 | 8.8%      | Acceptable – corresponds to deleted users and handled using `deleted_account_id` |

#### `fees_df`:

| Column         | % Missing | Notes |
|----------------|-----------|-------|
| `category`     | 89.6%     | Expected – only applies to `incident` fees |
| `from_date`, `to_date` | ~68% | Expected – only apply to `postpone` fees |
| `paid_at`      | 26.7%     | Acceptable – fee may not yet be charged |
| `cash_request_id` | 0.02% | Investigated and removed: 4 unlinked, canceled fee records |

➡️ **Conclusion**: ✅ Most missing values are expected and handled appropriately.  
🛠️ One record with both `user_id` and `deleted_account_id` was corrected.  
🧹 4 unlinked rows were removed from `fees_df`.

---

### 3. 🕒 **Invalid or Future Dates**

- ✅ All datetime fields were converted to `datetime64[ns]` format
- ✅ Timezone inconsistencies resolved — all values made timezone-naive
- ✅ No future-dated timestamps found beyond project cutoff (Dec 12, 2024)

➡️ **Conclusion**: ✅ Datetime fields are clean and consistent

---

### 4. 🧮 **Monetary Columns Check**

- `cash_df['amount']`: All values are numeric (`float64`), and none are negative or zero
- `fees_df['total_amount']`: All values are valid, mostly 5.0 or 10.0

➡️ **Conclusion**: ✅ Monetary columns are valid and trustworthy

---

### 5. 🔤 **Categorical Consistency**

All key categorical columns were cleaned and standardized:
- Lowercased and stripped of whitespace
- `"nan"` string values converted to true `NaN`

#### `cash_df`:
- `status`, `transfer_type`, `recovery_status`

#### `fees_df`:
- `type`, `status`, `category`, `charge_moment`

➡️ **Conclusion**: ✅ Consistent and safe for grouping and filtering

---

### 6. 🆔 **User Identity Normalization**

- Created a unified `final_user_id` column combining `user_id` and `deleted_account_id`
- Ensures each row is associated with a valid user (active or deleted)

➡️ **Conclusion**: ✅ Dataset supports reliable user-level analysis

---

### 7. 🗂️ **Column Reordering & Data Types**

- Reordered columns for better readability and analysis
- Confirmed expected data types:
  - Dates → `datetime64[ns]`
  - Amounts → `float64`
  - Identifiers → `int64` / `float64`
  - Categories → `object`

➡️ **Conclusion**: ✅ DataFrames are structured and correctly typed

---

## ✅ Final Assessment

Both datasets are now:
- Cleaned and standardized  
- Free from structural issues  
- Fully ready for exploratory analysis and cohort segmentation

Cleaned files saved to:  
📁 `cleaned_project_datasets/clean_cash_requests.csv`  
📁 `cleaned_project_datasets/clean_fees.csv`

---

### 📌 Next Step:
Proceed to **Exploratory Data Analysis** in  
📓 `2_eda_ironhack_payments.ipynb`
