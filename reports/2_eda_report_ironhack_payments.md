# 📊 Exploratory Data Analysis (EDA) Report

### 📁 **Project:** Cohort Analysis of Ironhack Payments

📅 **Date:** December 13, 2024  
👩‍💻 **Author:** Ginosca Alejandro Dávila

🏫 **School:** Ironhack Puerto Rico

🚀**Bootcamp:** Data Science and Machine Learning

**📓 Notebook:** 2_eda_ironhack_payments.ipynb  

---

## 📌 Overview

This report summarizes the exploratory data analysis conducted on cleaned datasets produced in notebook 1_data_cleaning_ironhack_payments.ipynb for Ironhack Payments, forming the foundation for the upcoming cohort analysis.  
The full analysis with visualizations is available in the notebook: 2_eda_ironhack_payments.ipynb.

---

## 📂 Datasets Used

- **clean_cash_requests.csv**: 23,970 rows × 17 columns
- **clean_fees.csv**: 21,057 rows × 13 columns

Both datasets are cleaned, standardized, and include:

- Normalized datetime and categorical fields
- Removed duplicates and unlinked records
- Handled nulls
- Validated monetary values
- Ready for visualization and aggregation

---

## 🔢 Key Descriptive Insights

### 💰 Cash Request Amounts

- Most values cluster around €100.
- Minimum is €1, maximum is €200.
- Low standard deviation (~26.5), showing narrow range.

### 💸 Fee Amounts

- 99.99% of fees are €5, with a single €10 outlier.
- Indicates a flat fee model.

---

## 🔤 Categorical Variable Distributions

### In cash_df

- **Status**: Mostly money_back and rejected.
- **Transfer Type**: 58% instant, 42% regular.
- **Recovery Status**: 86% missing (no incidents), remainder are mostly completed.

### In fees_df

- **Type**: Mostly instant_payment, followed by postpone.
- **Status**: Dominantly accepted.
- **Category**: Mostly missing (only relevant for incident fees).
- **Charge Moment**: Primarily after the request.

---

## 📅 Time-Based Trends

### Monthly Cash Requests

- Sharp growth begins May 2020, peaking in October 2020.
- Partial months: Nov 2019 (data starts on 19th), Nov 2020 (only up to 1st).

### Monthly Cash Amounts

- Closely aligned with volume trends.
- Peaks in October 2020 at over €550,000.

---

## 👤 User Behavior

- 11,793 unique users.
- **60.5%** of users made only **1** request.
- Remaining 39.5% made multiple requests (most common: 2–5).

---

## ⚠️ Incident Analysis

- 86% of requests had no incidents.
- 10% were completed incidents, 3.5% were pending.
- Incident ratios are mostly stable between 10–16% monthly.
- Peak incident counts also in October 2020.
- Incident requests increased as user activity grew

---

## 💰 Revenue Analysis

### By Fee Type

- **Instant Payment**: ~€55,480
- **Postpone**: ~€38,830
- **Incident**: ~€10,980

### By Charge Timing

- Postpone fees split between before and after.
- Instant and Incident fees always charged after.

### By Request Status

- **Money Back** generated most revenue (~€94,000).
- **Direct Debit Rejected** second highest (~€9,290).
- Rejected/canceled requests yielded no revenue.

---

## 🔗 Dataset Merging

- cash_df and fees_df merged on cash_request_id.
- Final merged dataset: 32,094 rows × 33 columns.
- 23,970 unique cash requests, with 12,933 (53.95%) linked to at least one fee
- Merged dataset enables joint analysis of request behavior and financial outcomes

---

## 📊 Status and Revenue Relationships

- **Money Back** status accounts for most revenue: over €94,000.
- **Direct Debit Rejected** follows with €9,290, mostly via incident fees.
- Statuses like cancelled and rejected contribute little or no revenue.

---

## 📆 Cohort Preparation

### First Request Date

- Extracted per user
- Cohort month assigned (e.g., "Nov 2019")

### Monthly Active Users (MAU)

- Growth from Dec 2019 → Oct 2020 peak: 7,191 users
- Strong upward trend confirms user adoption and engagement.
- November 2020 shows a drop due to partial data.

---

## **✨** Transfer Preferences

- **Instant transfers** became available around July 2020.
- Rapid adoption: 0% in June → 93% by October 2020.
- Corresponding drop in regular transfers.

---

## 💾 Data Saved for Cohort Analysis

| **File** | **Description** |
| --- | --- |
| user_first_request.csv | First request date and cohort for each user |
| --- | --- |
| monthly_active_users.csv | Monthly count of active users |
| --- | --- |
| transfer_type_share.csv | Instant vs regular usage and share over time |
| --- | --- |
| merged_cash_fee.csv | Full joined dataset for cohort metrics |
| --- | --- |

---

## 📄 EDA Completion Checklist

| **Task** | **Status** |
| --- | --- |
| Data loaded and inspected | ✅   |
| --- | --- |
| Data quality issues identified and handled | ✅   |
| --- | --- |
| Cash request trends analyzed | ✅   |
| --- | --- |
| Incident rates and fee types explored | ✅   |
| --- | --- |
| Transfer type evolution (instant vs regular) studied | ✅   |
| --- | --- |
| Users assigned to cohorts based on first cash request | ✅   |
| --- | --- |
| Cash requests and fees successfully linked | ✅   |
| --- | --- |
| Key aggregates saved for cohort analysis | ✅   |
| --- | --- |

---

## **✅** EDA Final Summary and Next Steps

### **🔍 Accomplishments**

- Cleaned and analyzed core datasets.
- Explored user behavior, fees, and incidents.
- Investigated platform trends and revenue streams.
- Prepared the base for cohort segmentation.

### **✅ Final Thoughts**

The EDA revealed:

- Strong user and revenue growth across 2020.
- Platform reliability with minimal unresolved incidents.
- Cohort-ready structure, with clear behavioral patterns.

### **📦 Exports Ready**

- All needed .csv outputs are saved to the project directory.

### **🚀 Next Notebook**

Proceed to: 3_cohort_analysis_metrics.ipynb to:

- Define cohorts
- Calculate retention, frequency, incident rates and revenue KPIs
- Propose new metrics
- Generate business insights
