"""
SAP R2R (Record-to-Report) Financial Data Analysis
===================================================
Capstone Project - SAP Functional Module
Scenario: Month-End Financial Close Process Simulation

This script demonstrates:
1. Loading SAP-style financial data (GL entries)
2. Running trial balance, P&L and expense analysis
3. Generating dashboard charts for project documentation
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ─── Configuration ─────────────────────────────────────────────────────────────
DATA_PATH = "../dataset/financial_data.csv"
OUTPUT_CHARTS = "../dashboard_images/"
SCREENSHOTS  = "../screenshots/"

os.makedirs(OUTPUT_CHARTS, exist_ok=True)
os.makedirs(SCREENSHOTS, exist_ok=True)

# ─── 1. Load Data ──────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print("=" * 55)
print("  SAP R2R FINANCIAL DATA — LOADED SUCCESSFULLY")
print("=" * 55)
print(df.head(10).to_string(index=False))
print(f"\nTotal Records : {len(df)}")
print(f"Months Covered: {df['Month'].nunique()}")
print(f"GL Accounts   : {df['GL_Account'].nunique()}")

# ─── 2. Monthly Revenue vs Expense Summary ─────────────────────────────────────
monthly = df.groupby("Month").agg(
    Total_Revenue=("Credit", "sum"),
    Total_Expense=("Debit", "sum")
).reset_index()
monthly["Net_Profit"] = monthly["Total_Revenue"] - monthly["Total_Expense"]

print("\n" + "=" * 55)
print("  MONTHLY PROFIT & LOSS SUMMARY (INR)")
print("=" * 55)
print(monthly.to_string(index=False))

# ─── 3. Cost Center Expense Breakdown ──────────────────────────────────────────
cc_expense = df[df["Debit"] > 0].groupby("Cost_Center")["Debit"].sum().reset_index()
cc_expense.columns = ["Cost_Center", "Total_Expense"]

print("\n" + "=" * 55)
print("  COST CENTER EXPENSE BREAKDOWN (INR)")
print("=" * 55)
print(cc_expense.to_string(index=False))

# ─── 4. GL Account Category Analysis ──────────────────────────────────────────
gl_summary = df.groupby(["GL_Account", "GL_Description"]).agg(
    Total_Debit=("Debit", "sum"),
    Total_Credit=("Credit", "sum")
).reset_index()
gl_summary["Net_Balance"] = gl_summary["Total_Credit"] - gl_summary["Total_Debit"]

print("\n" + "=" * 55)
print("  TRIAL BALANCE — GL ACCOUNT SUMMARY (INR)")
print("=" * 55)
print(gl_summary.to_string(index=False))

# ─── 5. CHART 1: Monthly Profit Chart ─────────────────────────────────────────
months_order = ["Jan-2025","Feb-2025","Mar-2025","Apr-2025","May-2025","Jun-2025"]
monthly["Month"] = pd.Categorical(monthly["Month"], categories=months_order, ordered=True)
monthly = monthly.sort_values("Month")

fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(monthly))
bars_rev = ax.bar([i - 0.25 for i in x], monthly["Total_Revenue"] / 1e5,
                  width=0.25, label="Revenue (₹ Lakh)", color="#2E75B6")
bars_exp = ax.bar([i for i in x], monthly["Total_Expense"] / 1e5,
                  width=0.25, label="Expense (₹ Lakh)", color="#ED7D31")
ax.plot([i + 0.25 for i in x], monthly["Net_Profit"] / 1e5,
        marker="o", color="#70AD47", linewidth=2.5, label="Net Profit (₹ Lakh)")
ax.set_xticks(list(x))
ax.set_xticklabels(monthly["Month"], rotation=15, fontsize=9)
ax.set_ylabel("Amount (₹ Lakhs)", fontsize=10)
ax.set_title("SAP R2R — Monthly Revenue vs Expense vs Profit\n(Jan–Jun 2025)", fontsize=12, fontweight="bold")
ax.legend(fontsize=9)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.savefig(OUTPUT_CHARTS + "profit_chart.png", dpi=150)
plt.savefig(SCREENSHOTS + "analysis_output.png", dpi=150)
print("\n[Chart Saved] profit_chart.png")
plt.close()

# ─── 6. CHART 2: Expense Breakdown Pie Chart ──────────────────────────────────
expense_by_desc = df[df["Debit"] > 0].groupby("GL_Description")["Debit"].sum()

fig, ax = plt.subplots(figsize=(8, 6))
colors = ["#2E75B6", "#ED7D31", "#A9D18E", "#FFC000"]
wedges, texts, autotexts = ax.pie(
    expense_by_desc.values,
    labels=expense_by_desc.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=colors,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="white", linewidth=1.5)
)
for t in autotexts:
    t.set_fontsize(9)
ax.set_title("SAP R2R — Expense Category Distribution\n(Jan–Jun 2025)", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_CHARTS + "expense_chart.png", dpi=150)
print("[Chart Saved] expense_chart.png")
plt.close()

# ─── 7. SCREENSHOT: Data Table View ───────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis("off")
sample = df[["Month","GL_Account","GL_Description","Debit","Credit","Cost_Center"]].head(8)
table = ax.table(
    cellText=sample.values,
    colLabels=sample.columns,
    cellLoc="center",
    loc="center"
)
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1.2, 1.6)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor("#2E75B6")
        cell.set_text_props(color="white", fontweight="bold")
    elif row % 2 == 0:
        cell.set_facecolor("#EBF3FB")
ax.set_title("SAP GL Journal Entry Data — Preview", fontsize=11, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig(SCREENSHOTS + "data_view.png", dpi=150)
print("[Screenshot Saved] data_view.png")
plt.close()

# ─── 8. SAP Architecture Diagram ──────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")
ax.set_facecolor("#F8F9FA")
fig.patch.set_facecolor("#F8F9FA")

boxes = [
    (1, 5.2, 2, 0.9, "#2E75B6", "white", "SAP ECC / S/4HANA\nFI Module (GL)"),
    (4, 5.2, 2, 0.9, "#ED7D31", "white", "FI-CO Integration\n(Cost Centers)"),
    (7, 5.2, 2, 0.9, "#70AD47", "white", "Controlling Module\n(Profit Centers)"),
    (1, 3.2, 2, 0.9, "#4472C4", "white", "Journal Entry\n(FB50 / F-02)"),
    (4, 3.2, 2, 0.9, "#C55A11", "white", "Period End Close\n(F.16 / FAGLGVTR)"),
    (7, 3.2, 2, 0.9, "#375623", "white", "Financial Reports\n(F.01 / S_ALR_*)"),
    (3.5, 1.2, 3, 0.9, "#7030A0", "white", "Project Output:\nP&L | Trial Balance | Dashboard"),
]
for (x, y, w, h, col, tc, lbl) in boxes:
    rect = mpatches.FancyBboxPatch((x, y), w, h,
                                    boxstyle="round,pad=0.08",
                                    facecolor=col, edgecolor="white", linewidth=1.5)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, lbl, ha="center", va="center",
            fontsize=8.5, color=tc, fontweight="bold")

# Arrows
arrow_props = dict(arrowstyle="->", color="#555555", lw=1.5)
for (x1, y1, x2, y2) in [(3, 5.65, 4, 5.65), (6, 5.65, 7, 5.65),
                           (2, 5.2, 2, 4.1), (5, 5.2, 5, 4.1), (8, 5.2, 8, 4.1),
                           (3, 3.65, 4, 3.65), (6, 3.65, 7, 3.65),
                           (5, 3.2, 5, 2.1)]:
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props)

ax.set_title("SAP R2R Process Architecture — End-to-End Flow", fontsize=12, fontweight="bold", pad=10)
plt.tight_layout()
plt.savefig(SCREENSHOTS + "sap_architecture.png", dpi=150)
print("[Screenshot Saved] sap_architecture.png")
plt.close()

print("\n" + "=" * 55)
print("  ALL ANALYSIS COMPLETE — Charts & Screenshots Saved")
print("=" * 55)
