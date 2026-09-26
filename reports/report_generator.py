import os
import pandas as pd
import matplotlib.pyplot as plt


def create_output_folder():

    folder = "Portfolio_Analysis_Output"

    if not os.path.exists(folder):
        os.makedirs(folder)

    return folder


def create_pie_chart(df, output_folder):

    plt.figure(figsize=(9, 7))

    plt.pie(
        df["Current_Value"],
        labels=df["Ticker"],
        autopct="%1.1f%%",
        startangle=90
    )

    plt.title("Portfolio Allocation")

    chart_path = os.path.join(
        output_folder,
        "portfolio_allocation.png"
    )

    plt.savefig(
        chart_path,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


def save_csv_report(df, output_folder):

    report_path = os.path.join(
        output_folder,
        "portfolio_analysis.csv"
    )

    df.to_csv(
        report_path,
        index=False
    )

    return report_path


def save_text_report(
    df,
    diversification,
    best,
    worst,
    total_investment,
    total_current_value,
    total_profit_loss,
    portfolio_return,
    output_folder
):

    report_path = os.path.join(
        output_folder,
        "portfolio_summary.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "PORTFOLIO RISK & REBALANCING ANALYZER\n"
        )

        file.write("=" * 50 + "\n\n")

        file.write(
            f"Total Investment: "
            f"₹{total_investment:,.2f}\n"
        )

        file.write(
            f"Current Portfolio Value: "
            f"₹{total_current_value:,.2f}\n"
        )

        file.write(
            f"Total Profit/Loss: "
            f"₹{total_profit_loss:,.2f}\n"
        )

        file.write(
            f"Portfolio Return: "
            f"{portfolio_return:.2f}%\n"
        )

        file.write(
            f"Diversification Score: "
            f"{diversification:.2f}/100\n\n"
        )

        file.write("=" * 50 + "\n")

        file.write(
            f"Best Performer: "
            f"{best['Ticker']} "
            f"({best['Return_%']:.2f}%)\n"
        )

        file.write(
            f"Worst Performer: "
            f"{worst['Ticker']} "
            f"({worst['Return_%']:.2f}%)\n\n"
        )

        file.write("=" * 50 + "\n")

        file.write(
            "REBALANCING RECOMMENDATIONS\n"
        )

        file.write("=" * 50 + "\n\n")

        for _, row in df.iterrows():

            amount = row["Rebalance_Amount"]

            shares = row["Rebalance_Shares"]

            if amount > 0:

                file.write(
                    f"{row['Ticker']}: "
                    f"BUY approximately "
                    f"₹{amount:,.2f} "
                    f"({shares:.2f} shares)\n"
                )

            elif amount < 0:

                file.write(
                    f"{row['Ticker']}: "
                    f"SELL approximately "
                    f"₹{abs(amount):,.2f} "
                    f"({abs(shares):.2f} shares)\n"
                )

            else:

                file.write(
                    f"{row['Ticker']}: "
                    f"No rebalancing required\n"
                )

    return report_path