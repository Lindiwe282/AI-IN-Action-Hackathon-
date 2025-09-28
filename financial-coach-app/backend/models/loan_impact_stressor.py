# mrf_loan_risk.py
import numpy as np
import pandas as pd
from pgmpy.models import MarkovModel
from pgmpy.factors.discrete import DiscreteFactor
from pgmpy.inference import BeliefPropagation

# --------------------------
# Define nodes and possible states
# --------------------------
# 0=Low, 1=Medium, 2=High (risk/impact)
nodes = [
    'Loan_Amount', 'Interest_Rate', 'Monthly_Repayment',
    'Income', 'Essential_Expenses', 'Lifestyle_Spending',
    'Savings_Rate', 'DTI', 'Default_Risk',
    'Savings_Health', 'Lifestyle_Impact', 'Investment_Impact',
    'Financial_Stress'
]

# --------------------------
# Initialize the Markov Model
# --------------------------
model = MarkovModel()

# Add nodes
model.add_nodes_from(nodes)

# Add edges (dependencies)
edges = [
    ('Loan_Amount', 'Monthly_Repayment'),
    ('Interest_Rate', 'Monthly_Repayment'),
    ('Monthly_Repayment', 'Default_Risk'),
    ('Income', 'Default_Risk'),
    ('Income', 'Lifestyle_Impact'),
    ('Income', 'Savings_Health'),
    ('DTI', 'Default_Risk'),
    ('Savings_Rate', 'Savings_Health'),
    ('Essential_Expenses', 'Financial_Stress'),
    ('Monthly_Repayment', 'Financial_Stress'),
    ('Financial_Stress', 'Lifestyle_Impact'),
    ('Financial_Stress', 'Investment_Impact')
]
model.add_edges_from(edges)

# --------------------------
# Define factors
# --------------------------
# Example: Loan_Amount -> Monthly_Repayment
factor_loan_monthly = DiscreteFactor(
    variables=['Loan_Amount', 'Monthly_Repayment'],
    cardinality=[3, 3],
    values=[
        0.8, 0.15, 0.05,  # Loan Low -> Monthly Repayment Low/Med/High
        0.2, 0.6, 0.2,    # Loan Medium -> Monthly Repayment
        0.05, 0.25, 0.7   # Loan High -> Monthly Repayment
    ]
)

# Monthly_Repayment -> Default_Risk
factor_repay_default = DiscreteFactor(
    variables=['Monthly_Repayment', 'Default_Risk'],
    cardinality=[3, 3],
    values=[
        0.85, 0.1, 0.05,  # Low repayment -> Low/Med/High default
        0.2, 0.6, 0.2,
        0.05, 0.25, 0.7
    ]
)

# DTI -> Default_Risk
factor_dti_default = DiscreteFactor(
    variables=['DTI', 'Default_Risk'],
    cardinality=[3,3],
    values=[
        0.9, 0.08, 0.02,
        0.3, 0.5, 0.2,
        0.05, 0.25, 0.7
    ]
)

# Default_Risk -> Savings_Health
factor_default_savings = DiscreteFactor(
    variables=['Default_Risk', 'Savings_Health'],
    cardinality=[3,3],
    values=[
        0.9,0.08,0.02,
        0.3,0.5,0.2,
        0.05,0.25,0.7
    ]
)

# Financial_Stress -> Lifestyle_Impact
factor_stress_lifestyle = DiscreteFactor(
    variables=['Financial_Stress', 'Lifestyle_Impact'],
    cardinality=[3,3],
    values=[
        0.85,0.1,0.05,
        0.2,0.6,0.2,
        0.05,0.25,0.7
    ]
)

# Financial_Stress -> Investment_Impact
factor_stress_invest = DiscreteFactor(
    variables=['Financial_Stress', 'Investment_Impact'],
    cardinality=[3,3],
    values=[
        0.85,0.1,0.05,
        0.2,0.6,0.2,
        0.05,0.25,0.7
    ]
)

# Add factors to the model
model.add_factors(factor_loan_monthly, factor_repay_default,
                  factor_dti_default, factor_default_savings,
                  factor_stress_lifestyle, factor_stress_invest)

# --------------------------
# Inference
# --------------------------
bp = BeliefPropagation(model)

# Evidence example: user wants a medium loan, interest rate medium, monthly income medium, etc.
evidence = {
    'Loan_Amount': 1,       # 0=Low,1=Medium,2=High
    'Interest_Rate': 1,
    'Income': 1,
    'DTI': 1,
    'Savings_Rate': 1,
    'Essential_Expenses': 1,
    'Lifestyle_Spending': 1
}

result = bp.query(variables=['Default_Risk', 'Savings_Health', 'Lifestyle_Impact', 'Investment_Impact'],
                  evidence=evidence, show_progress=False)

print("Predicted probabilities:")
for var in result:
    print(f"{var}: {result[var].values}")
