# SAP R2R Capstone Project — Record-to-Report Financial Close

## Overview
This project simulates the complete **Record-to-Report (R2R)** process in SAP FI/CO for a fictitious company **KIIT Industries Pvt. Ltd.** (Company Code: K100), covering month-end financial close activities for Jan–Jun 2025.

---

## Project Structure
```
SAP-Data-Analytics-Project/
├── README.md                        ← This file
├── Project_Report.pdf               ← 4-page capstone report (submit this)
├── dataset/
│   └── financial_data.csv           ← SAP-style GL journal entries (6 months)
├── notebooks/
│   └── analysis.py                  ← Python: P&L, Trial Balance, Charts
├── screenshots/
│   ├── data_view.png                ← GL data table preview
│   ├── analysis_output.png          ← Monthly P&L output chart
│   └── sap_architecture.png         ← R2R process architecture diagram
└── dashboard_images/
    ├── profit_chart.png             ← Revenue vs Expense vs Profit (bar+line)
    └── expense_chart.png            ← Expense category distribution (pie)
```

---

## R2R Process Covered

| Step | SAP Activity | T-Code |
|------|-------------|--------|
| 1 | GL Master Account creation | FS00 |
| 2 | Cost Center setup (CC1001, CC2001, CC3001) | KS01 |
| 3 | Profit Center setup | KE51 |
| 4 | Journal Entry posting (Jan–Jun 2025) | FB50 / F-02 |
| 5 | Cost Center Allocations | KSV5 |
| 6 | Month-End Closing | F.16 / OB52 |
| 7 | Balance Carryforward | FAGLGVTR |
| 8 | Trial Balance | F.01 |
| 9 | P&L Statement | S_ALR_87012277 |
| 10 | Python Analytics & Visualization | Pandas / Matplotlib |

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib

# Run analysis
cd notebooks
python analysis.py
```

Output charts are saved to `dashboard_images/` and `screenshots/` automatically.

---

## Tech Stack
- **SAP ECC / S/4HANA** — FI (Financial Accounting), CO (Controlling)
- **Python 3.11** — Pandas, Matplotlib
- **ReportLab** — PDF generation
- **GitHub** — Version control

---

## Key Results (6-Month Summary)

| Month | Revenue (INR) | Expenses (INR) | Net Profit (INR) |
|-------|-------------|--------------|----------------|
| Jan 2025 | 11,70,000 | 7,40,000 | 4,30,000 |
| Feb 2025 | 12,00,000 | 7,65,000 | 4,35,000 |
| Mar 2025 | 14,60,000 | 8,42,000 | 6,18,000 |
| Apr 2025 | 13,30,000 | 8,13,000 | 5,17,000 |
| May 2025 | 15,20,000 | 8,68,000 | 6,52,000 |
| Jun 2025 | 16,80,000 | 9,25,000 | 7,55,000 |
| **Total** | **83,60,000** | **49,53,000** | **34,07,000** |

---

## Submission Details
- **Module:** SAP Functional — R2R
- **Batch/Program:** B.Tech CSE
- **Student:** Ved Tamang | Roll No: 23051800

> Submit via Google Form: ZIP file + GitHub link + Project_Report.pdf
