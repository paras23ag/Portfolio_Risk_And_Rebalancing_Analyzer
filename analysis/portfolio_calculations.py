import pandas as pd
import numpy as np


def calculate_investment_value(df):
    """
    Calculate the original amount invested in each stock.
    """

    df["Investment_Value"] = (
        df["Shares"] * df["Purchase_Price"]
    )

    return df


def calculate_current_value(df):
    """
    Calculate the current market value of each position.
    """

    df["Current_Value"] = (
        df["Shares"] * df["Current_Price"]
    )

    return df


def calculate_profit_loss(df):
    """
    Calculate profit/loss for each stock.
    """

    df["Profit_Loss"] = (
        df["Current_Value"]
        - df["Investment_Value"]
    )

    return df


def calculate_return(df):
    """
    Calculate percentage return for each stock.
    """

    df["Return_%"] = (
        df["Profit_Loss"]
        / df["Investment_Value"]
    ) * 100

    return df


def calculate_portfolio_weights(df):
    """
    Calculate each stock's percentage weight
    in the portfolio.
    """

    total_current_value = df["Current_Value"].sum()

    df["Portfolio_Weight_%"] = (
        df["Current_Value"]
        / total_current_value
    ) * 100

    return df


def calculate_rebalancing(df):
    """
    Calculate the amount required to move the
    portfolio toward equal allocation.
    """

    number_of_stocks = len(df)

    total_current_value = df["Current_Value"].sum()

    target_value = (
        total_current_value
        / number_of_stocks
    )

    df["Target_Value"] = target_value

    df["Rebalance_Amount"] = (
        df["Target_Value"]
        - df["Current_Value"]
    )

    df["Rebalance_Shares"] = (
        df["Rebalance_Amount"]
        / df["Current_Price"]
    )

    return df