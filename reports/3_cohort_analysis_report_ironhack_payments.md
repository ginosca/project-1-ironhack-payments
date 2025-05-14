# 📊 Cohort Analysis Report  

### 📁 **Project:** Cohort Analysis of Ironhack Payments

### 📓 Notebook: 3_cohort_analysis_metrics.ipynb  

📅 **Date:** December 13, 2024

👩‍💻 **Author:** Ginosca Alejandro Dávila 

🏫 **School:** Ironhack Puerto Rico

🛠️ **Bootcamp:** Data Science & Machine Learning

---

## 🧾 Overview

This notebook performs **cohort-based behavioral analysis** of Ironhack Payments users, building on the outputs of prior notebooks. This analysis builds on cleaned data and EDA outputs prepared in prior notebooks (`1_data_cleaning_ironhack_payments.ipynb` and `2_eda_ironhack_payments.ipynb`). The goal is to assess how different user cohorts behave over time in terms of service usage, retention, incident rates, and monetization (revenue, ARPU, CLV). The analysis provides a foundation for understanding **customer lifetime value** and identifying **growth and retention strategies**.

---

## 📁 Input Data

Four key datasets were loaded from the EDA phase:

- `user_first_request.csv` – First request dates and cohort assignments per user  
- `monthly_active_users.csv` – Active user counts per month  
- `transfer_type_share.csv` – Share of transfer types (instant vs. regular)  
- `merged_cash_fee.csv` – Fully cleaned and merged dataset of cash requests and associated fees

Each file was inspected for structure, types, and missing values prior to merging.

---

## 🧪 Methodology

Steps included:

1. **Cohort Assignment:** Merged cohort dates from `user_first_request.csv` into the main transactional dataset.
2. **Usage Frequency:** Built a cohort matrix counting cash requests per cohort and month.
3. **Retention Analysis:** Calculated and visualized monthly user retention rates (full and filtered matrices).
4. **Incident Rates:** Quantified and plotted the incident rate per cohort.
5. **Revenue Analysis:** Summarized and visualized monthly revenue and cumulative revenue by cohort.
6. **ARPU Calculation:** Derived Average Revenue Per User per cohort.
7. **CLV Estimation:** Estimated Customer Lifetime Value as: `CLV = ARPU × Avg. Retention Months`

All datasets and visualizations were saved for use in dashboards or presentations.

---

## 📌 Key Findings
- **User Activity Spikes:** The number of monthly active users surged in **April 2020** and peaked in **October 2020 with 7,191 active users**, driving short-term gains in usage, revenue, and strain on system performance.
- **October 2020** generated the **highest cohort revenue** at **€23,530**, followed by **June 2020 (€14,365)** and **July 2020 (€11,135)**.
- Despite high revenue, **October 2020** had the **lowest CLV (€4.90)** due to short retention (1 month), indicating limited long-term value.
- The **highest CLV** was observed in the **February 2020 cohort (€63.54)**, driven by strong ARPU and 9-month average retention.
- **Retention trends** reveal that cohorts from early 2020 (e.g., Feb–Apr) had higher user stickiness over time, peaking at **~74%** by month 6 (Feb 2020 cohort).
- **Incident rates** rose consistently over time, with peaks around **25%** in cohorts from **April–July 2020**, suggesting system strain or user friction as growth scaled.
- **ARPU** peaked in **June 2020 (€9.33)**, **May 2020 (€9.10)**, and **February 2020 (€7.06)** — reflecting higher monetization effectiveness for those cohorts.
- The **first cohort (Nov 2019)** is too small (only one user) to derive meaningful trends. Likewise, **Nov 2020** had limited data (partial month).

---

## 💼 Business Recommendations

Based on the insights above, we suggest the following actions:

1. **Double Down on Onboarding (Feb–May 2020 Strategy)**  
   Revisit engagement or onboarding tactics used during these months to replicate their retention success in future cohorts.

2. **Balance Growth with Stability**  
   Large spikes in usage (e.g., Oct 2020) correlated with higher incident rates and lower retention. Consider pacing growth campaigns or improving infrastructure to better support surges.

3. **Optimize for Retention, Not Just Acquisition**  
   High revenue in later months was often offset by poor retention. Focus marketing and product features on long-term engagement rather than short-term volume.

4. **Target High-Value Cohorts with Tailored Offers**  
   Cohorts like **Feb–Mar 2020** had excellent CLV and ARPU. Identify similar profiles and design targeted loyalty programs or premium service tiers.

5. **Reduce Friction and Incidents During Peak Periods**  
   Strengthen support, UX clarity, or automated checks during high-volume periods (e.g., summer 2020) to lower incident rates and enhance trust.

---

## 💾 Outputs Generated

All outputs were saved under:

```plaintext
/project-1-ironhack-payments-2-en/cohort_outputs/
├── data/
│   ├── cohort_usage_matrix.csv
│   ├── cohort_retention_matrix.csv
│   ├── cohort_retention_matrix_filtered.csv
│   ├── cohort_incident_rate.csv
│   ├── cohort_revenue.csv
│   ├── cohort_arpu.csv
│   └── cohort_clv.csv
├── plots/
│   ├── 01_cohort_retention_heatmap.png
│   ├── 02_cohort_retention_heatmap_filtered.png
│   ├── 03_cohort_retention_curves_selected.png
│   ├── 04_cohort_incident_rate.png
│   ├── 05_cohort_revenue_bar.png
│   ├── 06_cohort_revenue_cumulative_line.png
│   ├── 07_cohort_arpu_bar.png
│   └── 08_cohort_clv_bar.png
```
