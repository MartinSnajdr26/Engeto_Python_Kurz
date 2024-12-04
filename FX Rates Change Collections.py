import math

# Old exchange rates
old_rates = {
    'NOK': 0.1, 'GBP': 1.200005, 'CHF': 1, 'CZK': 0.043478,
    'PLN': 0.227273, 'SEK': 0.090909, 'DKK': 0.142857, 'EUR': 1,
    'ZAR': 0.058824
}

# New exchange rates
new_rates = {
    'NOK': 0.1, 'GBP': 1.270003, 'CHF': 1.111111, 'CZK': 0.043478,
    'PLN': 0.25, 'SEK': 0.090909, 'DKK': 0.147059, 'EUR': 1.050001,
    'ZAR': 0.052632
}

# Define weights for each currency (you can adjust these according to your requirements)
weights = {
    'NOK': 0.2, 'GBP': 0.3, 'CHF': 0.1, 'CZK': 0.05,
    'PLN': 0.1, 'SEK': 0.15, 'DKK': 0.1, 'EUR': 0.3,
    'ZAR': 0.2
}

# Calculate the total weighted adjustment factor
total_weighted_factor = sum(weights[currency] * (new_rates[currency] / old_rates[currency]) for currency in old_rates)

# Calculate the overall adjustment factor using the weighted average
overall_factor_weighted = total_weighted_factor / sum(weights.values())

print("Overall adjustment factor (Weighted average method):", overall_factor_weighted)
