import math

# Old exchange rates
old_rates = {
    'SEK': 0.090909, 'ILS': 0.285714, 'SAR': 0.266652, 'RSD': 0.009091,
    'UAH': 0.027027, 'RUB': 0.014286, 'ZAR': 0.058824, 'EUR': 1,
    'DKK': 0.142857, 'EGP': 0.033333, 'HUF': 0.002667, 'NOK': 0.1,
    'TRY': 0.053476, 'PKR': 0.004348, 'KZT': 0.002174, 'PLN': 0.227273,
    'LBP': 6.67E-05, 'CZK': 0.043478, 'RON': 0.215983, 'CHF': 1,
    'BGN': 0.540541, 'GBP': 1.200005
}

# New exchange rates
new_rates = {
    'SEK': 0.090909, 'ILS': 0.25974, 'SAR': 0.266667, 'RSD': 0.009091,
    'UAH': 0.027027, 'RUB': 0.011111, 'ZAR': 0.052632, 'EUR': 1.050001,
    'DKK': 0.147059, 'EGP': 0.032258, 'HUF': 0.002857, 'NOK': 0.1,
    'TRY': 0.033333, 'PKR': 0.003571, 'KZT': 0.002174, 'PLN': 0.25,
    'LBP': 6.67E-05, 'CZK': 0.043478, 'RON': 0.222222, 'CHF': 1.111111,
    'BGN': 0.555556, 'GBP': 1.270003
}

# Define weights for each currency
weights = {
    'SEK': 0.05, 'ILS': 0.02, 'SAR': 0.02, 'RSD': 0.005,
    'UAH': 0.01, 'RUB': 0.01, 'ZAR': 0.015, 'EUR': 0.3,
    'DKK': 0.05, 'EGP': 0.01, 'HUF': 0.005, 'NOK': 0.05,
    'TRY': 0.015, 'PKR': 0.005, 'KZT': 0.0025, 'PLN': 0.1,
    'LBP': 0.0025, 'CZK': 0.05, 'RON': 0.05, 'CHF': 0.1,
    'BGN': 0.05, 'GBP': 0.3
}

# Calculate the total weighted adjustment factor
total_weighted_factor = sum(weights[currency] * (new_rates[currency] / old_rates[currency]) for currency in old_rates)

# Calculate the overall adjustment factor using the weighted average
overall_factor_weighted = total_weighted_factor / sum(weights.values())

print("Overall adjustment factor (Weighted average method):", overall_factor_weighted)
