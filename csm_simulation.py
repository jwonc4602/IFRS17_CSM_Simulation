import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------
# 1. Generate synthetic insurance data
# --------------------------------------
n_contracts = 1000
np.random.seed(42)

annual_premium = np.random.normal(1200, 100, n_contracts)
annual_claim = np.random.normal(900, 120, n_contracts)

data = pd.DataFrame({
    'contract_id': np.arange(n_contracts),
    'premium': annual_premium,
    'claims': annual_claim,
    'expected_service_cost': annual_claim * 0.2  # assumption
})
# 2. Save synthetic data to CSV
data.to_csv('data/synthetic_insurance_data.csv', index=False)


# --------------------------------------
# 2. Function to calculate CSM
# --------------------------------------
def calculate_csm(df, n_years=10, discount_rate=0.03, margin_ratio=0.1):
    csm_results = []

    for _, row in df.iterrows():
        premium = row['premium']
        claim = row['claims']
        expense = row['expected_service_cost']
        service_margin = (premium - claim - expense) * margin_ratio

        # Discounted service margin per year
        csm = [service_margin / ((1 + discount_rate) ** year) for year in range(n_years)]
        csm_results.append(csm)

    return np.array(csm_results).mean(axis=0)


# --------------------------------------
# 3. Scenario comparison: financial sensitivity
# --------------------------------------
scenarios = {
    'Base': (0.03, 0.1),
    'Zero Discount Rate': (0.00, 0.1),
    'Very High Margin': (0.03, 0.2),
    'Negative Discount Rate': (-0.01, 0.1),
    'High Discount Rate': (0.05, 0.1)
}

n_years = 10
plt.figure(figsize=(10, 6))

for label, (rate, margin) in scenarios.items():
    csm = calculate_csm(data, n_years=n_years, discount_rate=rate, margin_ratio=margin)
    plt.plot(range(1, n_years + 1), csm, label=f'{label}', linewidth=2)

plt.title('CSM Sensitivity Analysis under IFRS 17')
plt.xlabel('Year')
plt.ylabel('Average CSM')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('plots/csm_sensitivity_analysis.png')
plt.show()
