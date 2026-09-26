import numpy as np


def diversification_score(df):
    """
    Calculate a diversification score from 0 to 100.

    100 = perfectly equal allocation
    Lower score = more concentrated portfolio
    """

    weights = (
        df["Portfolio_Weight_%"] / 100
    )

    hhi = np.sum(weights ** 2)

    number_of_stocks = len(df)

    if number_of_stocks <= 1:
        return 0

    minimum_hhi = 1 / number_of_stocks

    score = (
        (1 - hhi)
        / (1 - minimum_hhi)
    ) * 100

    return score


def best_performer(df):
    """
    Find the stock with the highest return.
    """

    index = df["Return_%"].idxmax()

    return df.loc[index]


def worst_performer(df):
    """
    Find the stock with the lowest return.
    """

    index = df["Return_%"].idxmin()

    return df.loc[index]