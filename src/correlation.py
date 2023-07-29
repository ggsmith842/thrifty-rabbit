"""
Provides support for diversification 
calculations.
"""
#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def findcorr(price_data):
    """
    Finds the weighed correlation of assets
    in a portfolio.

    Args:
        price_data (DataFrame): A DataFrame of asset prices.

    Returns:
        None.

    """
    price_data.fillna(0, inplace=True)
    corr_df = price_data.corr(method="pearson", numeric_only=True)

    # grab bottom half
    mask = np.zeros_like(corr_df)
    mask[np.triu_indices_from(mask)] = True

    # plot correlations
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr_df,
        annot=True,
        cmap="RdYlGn",
        vmax=1.0,
        vmin=-1.0,
        mask=mask,
        linewidths=2.5,
    )
    plt.show()

    avg_corr = corr_df.mean()

    report = format_report(avg_corr)
    print(report)

def format_report(avg_corr):
    '''
    Formats a diversification report based on the correlation 
    of assets in a given portfolio.

    Args:
        avg_corr (Series): A series of asset correlations.

    Returns:
        report (String): Formatted text reporting correlation
    '''
    header = "Diversification Report for Portfolio\n"
    divider = "-"*len(header)
    asset_mean = f"\nMean Correlation of each asset:\n{avg_corr.to_string(index=False)}\n"
    avg_mean = f"\nAverage Correlation of Portfolio\n{avg_corr.mean():.3f}"

    report = header + divider + asset_mean + divider + avg_mean
    return report