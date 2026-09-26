import pandas as pd
import yfinance as yf
import tkinter as tk

from tkinter import filedialog

from analysis.portfolio_calculations import (
    calculate_investment_value,
    calculate_current_value,
    calculate_profit_loss,
    calculate_return,
    calculate_portfolio_weights,
    calculate_rebalancing
)

from analysis.risk_analysis import (
    diversification_score,
    best_performer,
    worst_performer
)

from reports.report_generator import (
    create_output_folder,
    create_pie_chart,
    save_csv_report,
    save_text_report
)


# =========================================================
# 1. SELECT CSV FILE
# =========================================================

root = tk.Tk()
root.withdraw()

print("Please select your portfolio CSV file...")

file_path = filedialog.askopenfilename(
    title="Select Portfolio CSV",
    filetypes=[
        ("CSV files", "*.csv"),
        ("All files", "*.*")
    ]
)

if not file_path:

    print("\nNo file selected.")
    print("Program stopped.")

    exit()


print("\nSelected file:")
print(file_path)


# =========================================================
# 2. READ CSV
# =========================================================

try:

    df = pd.read_csv(file_path)

except Exception as e:

    print(
        f"\nCould not read the CSV file: {e}"
    )

    exit()


# =========================================================
# 3. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "Ticker",
    "Shares",
    "Purchase_Price"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print(
        "\nERROR: Your CSV is missing:"
    )

    for column in missing_columns:

        print(f"- {column}")

    print(
        "\nYour CSV must contain:"
    )

    print(
        "Ticker, Shares, Purchase_Price"
    )

    exit()


# =========================================================
# 4. CLEAN DATA
# =========================================================

df = df[
    [
        "Ticker",
        "Shares",
        "Purchase_Price"
    ]
].copy()


df["Ticker"] = (
    df["Ticker"]
    .astype(str)
    .str.upper()
    .str.strip()
)


df["Shares"] = pd.to_numeric(
    df["Shares"],
    errors="coerce"
)


df["Purchase_Price"] = pd.to_numeric(
    df["Purchase_Price"],
    errors="coerce"
)


df = df.dropna()


if len(df) == 0:

    print(
        "\nERROR: No valid portfolio positions found."
    )

    exit()


# =========================================================
# 5. DOWNLOAD CURRENT PRICES
# =========================================================

ticker_list = df["Ticker"].tolist()

print("\nDownloading current prices...")

price_data = yf.download(
    ticker_list,
    period="5d",
    auto_adjust=False,
    group_by="ticker",
    threads=False
)

print("\nPrice download completed.")


# =========================================================
# 6. GET LATEST PRICE FOR EACH STOCK
# =========================================================

current_prices = []

print("\nGetting current prices:\n")


for ticker in ticker_list:

    try:

        ticker_data = price_data[ticker]

        latest_price = (
            ticker_data["Close"]
            .dropna()
            .iloc[-1]
        )

        current_prices.append(
            latest_price
        )

        print(
            f"{ticker}: ₹{latest_price:.2f}"
        )

    except Exception as e:

        print(
            f"{ticker}: Could not retrieve price"
        )

        print(e)

        current_prices.append(
            float("nan")
        )


# =========================================================
# 7. ADD CURRENT PRICE
# =========================================================

df["Current_Price"] = current_prices


# Remove stocks where price could not be obtained

df = df.dropna(
    subset=["Current_Price"]
).reset_index(drop=True)


if len(df) == 0:

    print(
        "\nERROR: No current prices could be retrieved."
    )

    exit()


# =========================================================
# 8. CALCULATE INVESTMENT VALUE
# =========================================================

df = calculate_investment_value(df)


# =========================================================
# 9. CALCULATE CURRENT VALUE
# =========================================================

df = calculate_current_value(df)


# =========================================================
# 10. CALCULATE PROFIT / LOSS
# =========================================================

df = calculate_profit_loss(df)


# =========================================================
# 11. CALCULATE RETURN
# =========================================================

df = calculate_return(df)


# =========================================================
# 12. CALCULATE PORTFOLIO WEIGHTS
# =========================================================

df = calculate_portfolio_weights(df)


# =========================================================
# 13. CALCULATE REBALANCING
# =========================================================

df = calculate_rebalancing(df)


# =========================================================
# 14. PORTFOLIO TOTALS
# =========================================================

total_investment = (
    df["Investment_Value"].sum()
)


total_current_value = (
    df["Current_Value"].sum()
)


total_profit_loss = (
    df["Profit_Loss"].sum()
)


portfolio_return = (
    total_profit_loss
    / total_investment
) * 100


# =========================================================
# 15. RISK ANALYSIS
# =========================================================

diversification = (
    diversification_score(df)
)


best = best_performer(df)

worst = worst_performer(df)


# =========================================================
# 16. DISPLAY RESULTS
# =========================================================

print("\n")
print("=" * 70)

print(
    "          PORTFOLIO RISK & REBALANCING ANALYZER"
)

print("=" * 70)


print(
    f"\nTotal Investment: "
    f"₹{total_investment:,.2f}"
)


print(
    f"Current Portfolio Value: "
    f"₹{total_current_value:,.2f}"
)


print(
    f"Total Profit/Loss: "
    f"₹{total_profit_loss:,.2f}"
)


print(
    f"Portfolio Return: "
    f"{portfolio_return:.2f}%"
)


print(
    f"Diversification Score: "
    f"{diversification:.2f}/100"
)


# =========================================================
# 17. BEST AND WORST PERFORMERS
# =========================================================

print("\n")
print("=" * 70)

print("PERFORMANCE")

print("=" * 70)


print(
    f"\nBest Performer: "
    f"{best['Ticker']} "
    f"({best['Return_%']:.2f}%)"
)


print(
    f"Worst Performer: "
    f"{worst['Ticker']} "
    f"({worst['Return_%']:.2f}%)"
)


# =========================================================
# 18. PORTFOLIO TABLE
# =========================================================

print("\n")
print("=" * 70)

print("PORTFOLIO ANALYSIS")

print("=" * 70)


display_columns = [
    "Ticker",
    "Shares",
    "Purchase_Price",
    "Current_Price",
    "Investment_Value",
    "Current_Value",
    "Profit_Loss",
    "Return_%",
    "Portfolio_Weight_%"
]


print(
    df[display_columns]
    .to_string(index=False)
)


# =========================================================
# 19. REBALANCING
# =========================================================

print("\n")
print("=" * 70)

print("EQUAL-WEIGHT REBALANCING")

print("=" * 70)


for _, row in df.iterrows():

    amount = row["Rebalance_Amount"]

    shares = row["Rebalance_Shares"]


    if amount > 0:

        print(
            f"{row['Ticker']}: "
            f"BUY ₹{amount:,.2f} "
            f"({shares:.2f} shares)"
        )


    elif amount < 0:

        print(
            f"{row['Ticker']}: "
            f"SELL ₹{abs(amount):,.2f} "
            f"({abs(shares):.2f} shares)"
        )


    else:

        print(
            f"{row['Ticker']}: "
            f"No change required"
        )


# =========================================================
# 20. CREATE OUTPUT FOLDER
# =========================================================

output_folder = (
    create_output_folder()
)


# =========================================================
# 21. CREATE PIE CHART
# =========================================================

chart_path = create_pie_chart(
    df,
    output_folder
)


# =========================================================
# 22. SAVE CSV REPORT
# =========================================================

csv_report_path = save_csv_report(
    df,
    output_folder
)


# =========================================================
# 23. SAVE TEXT REPORT
# =========================================================

text_report_path = save_text_report(
    df,
    diversification,
    best,
    worst,
    total_investment,
    total_current_value,
    total_profit_loss,
    portfolio_return,
    output_folder
)


# =========================================================
# 24. FINAL MESSAGE
# =========================================================

print("\n")
print("=" * 70)

print("ANALYSIS COMPLETE")

print("=" * 70)


print(
    f"\nOutput folder: "
    f"{output_folder}"
)

print(
    f"\nPie chart saved to:"
    f"\n{chart_path}"
)

print(
    f"\nCSV report saved to:"
    f"\n{csv_report_path}"
)

print(
    f"\nSummary report saved to:"
    f"\n{text_report_path}"
)

print("\n")
print("=" * 70)