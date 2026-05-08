"""
generate_sample_data.py
Generates a realistic 1000-row telecom churn CSV for testing.
Run: python generate_sample_data.py
"""
import numpy as np
import pandas as pd

np.random.seed(42)
N = 1000

tenure         = np.random.randint(1, 72, N)
senior         = np.random.choice([0, 1], N, p=[0.84, 0.16])
gender         = np.random.choice(["Male", "Female"], N)
partner        = np.random.choice(["Yes", "No"], N)
dependents     = np.random.choice(["Yes", "No"], N, p=[0.3, 0.7])
phone          = np.random.choice(["Yes", "No"], N, p=[0.9, 0.1])
internet       = np.random.choice(["DSL", "Fiber optic", "No"], N, p=[0.34, 0.44, 0.22])
security       = np.where(internet != "No", np.random.choice(["Yes", "No"], N, p=[0.29, 0.71]), "No internet service")
support        = np.where(internet != "No", np.random.choice(["Yes", "No"], N, p=[0.29, 0.71]), "No internet service")
contract       = np.random.choice(["Month-to-month", "One year", "Two year"], N, p=[0.55, 0.24, 0.21])
paperless      = np.random.choice(["Yes", "No"], N, p=[0.59, 0.41])
payment        = np.random.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"], N)
monthly        = np.round(20 + 60 * (internet == "Fiber optic").astype(float) + 20 * np.random.rand(N), 2)
total          = np.round(monthly * tenure * (0.9 + 0.2 * np.random.rand(N)), 2)

churn_prob = np.clip(
    0.05
    + 0.30 * (contract == "Month-to-month").astype(float)
    + 0.15 * (internet == "Fiber optic").astype(float)
    + 0.10 * (security == "No").astype(float)
    - 0.20 * (tenure > 36).astype(float)
    + 0.08 * (monthly > 70).astype(float)
    + 0.05 * np.random.rand(N),
    0, 1
)
churn = np.where(np.random.rand(N) < churn_prob, "Yes", "No")

df = pd.DataFrame({
    "CustomerID": [f"CUS-{i:04d}" for i in range(1, N+1)],
    "Gender": gender, "SeniorCitizen": senior, "Partner": partner,
    "Dependents": dependents, "Tenure": tenure, "PhoneService": phone,
    "InternetService": internet, "OnlineSecurity": security,
    "TechSupport": support, "Contract": contract,
    "PaperlessBilling": paperless, "PaymentMethod": payment,
    "MonthlyCharges": monthly, "TotalCharges": total, "Churn": churn,
})

# Inject ~3% missing values
for col in ["TotalCharges", "MonthlyCharges", "Tenure"]:
    df.loc[np.random.rand(N) < 0.03, col] = np.nan

df.to_csv("sample_telecom_data.csv", index=False)
print(f"✅ Saved sample_telecom_data.csv — {len(df)} rows, churn rate: {(df['Churn']=='Yes').mean():.1%}")
