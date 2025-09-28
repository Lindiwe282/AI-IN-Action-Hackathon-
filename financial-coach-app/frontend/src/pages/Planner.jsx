import React, { useState } from 'react';
import { apiEndpoints } from '../services/api';

const Planner = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    monthly_income: '',
    monthly_expenses: '',
    current_savings: '',
    total_debt: '',
    age: '',
    dependents: '',
    risk_tolerance: 'medium',
    financial_goals: [],
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = {
        ...formData,
        monthly_income: parseFloat(formData.monthly_income) || 0,
        monthly_expenses: parseFloat(formData.monthly_expenses) || 0,
        current_savings: parseFloat(formData.current_savings) || 0,
        total_debt: parseFloat(formData.total_debt) || 0,
        age: parseInt(formData.age) || 30,
        dependents: parseInt(formData.dependents) || 0,
        user_id: 1,
      };
      const response = await apiEndpoints.createPlan(data);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create financial plan');
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setFormData({
      monthly_income: '',
      monthly_expenses: '',
      current_savings: '',
      total_debt: '',
      age: '',
      dependents: '',
      risk_tolerance: 'medium',
      financial_goals: [],
    });
    setResult(null);
    setError(null);
  };

  return (
    <div className="planner-container">
      <style>{`
        .planner-container {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem;
          font-family: 'Segoe UI', Arial, sans-serif;
          background: #f5f7fa;
        }
        .section-title {
          font-size: 2rem;
          font-weight: 900;
          margin-bottom: 0.5rem;
          text-align: center;
        }
        .section-desc {
          font-size: 1rem;
          margin-bottom: 2rem;
          text-align: center;
          color: #555;
        }
        .card {
          padding: 1.5rem;
          border-radius: 16px;
          box-shadow: 0 10px 20px rgba(0,0,0,0.08);
          transition: transform 0.3s, box-shadow 0.3s;
          margin-bottom: 1.5rem;
          background: white;
          color: black;
        }
        .card:hover {
          transform: translateY(-5px);
          box-shadow: 0 15px 25px rgba(0,0,0,0.12);
        }
        .card-title {
          font-size: 1.25rem;
          font-weight: 700;
          margin-bottom: 1rem;
        }
        .input-field {
          width: 100%;
          padding: 0.75rem 1rem;
          margin-bottom: 1rem;
          border-radius: 12px;
          border: 1px solid #ccc;
          font-size: 1rem;
        }
        .btn {
          padding: 0.75rem 1.5rem;
          border-radius: 12px;
          border: none;
          font-weight: bold;
          cursor: pointer;
          transition: background 0.3s, transform 0.2s;
          margin-top: 1rem;
        }
        .btn-primary {
          background: #1976d2;
          color: white;
          width: 100%;
        }
        .btn-primary:hover {
          background: #115293;
        }
        .btn-secondary {
          background: white;
          color: #1976d2;
          border: 2px solid #1976d2;
        }
        .btn-secondary:hover {
          background: #f0f4fa;
        }
        .alert {
          padding: 1rem;
          border-radius: 12px;
          margin-bottom: 1rem;
          font-weight: bold;
        }
        .alert-error {
          background: #f8d7da;
          color: #721c24;
        }
        .alert-success {
          background: #d4edda;
          color: #155724;
        }
        .result-section { margin-top: 1rem; }
        .result-card { margin-bottom: 1rem; border-radius: 12px; padding: 1rem; background: #f0f4fa; }
        .result-title { font-weight: bold; margin-bottom: 0.5rem; }
      `}</style>

      <header>
        <h1 className="section-title">AI Financial Planner</h1>
        <p className="section-desc">
          Get personalized financial recommendations based on your current situation and goals.
        </p>
      </header>

      {/* Input Form */}
      <div className="card">
        <h2 className="card-title">Your Financial Information</h2>
        <form onSubmit={handleSubmit}>
          <input className="input-field" type="number" name="monthly_income" placeholder="Monthly Income" value={formData.monthly_income} onChange={handleInputChange} required />
          <input className="input-field" type="number" name="monthly_expenses" placeholder="Monthly Expenses" value={formData.monthly_expenses} onChange={handleInputChange} required />
          <input className="input-field" type="number" name="current_savings" placeholder="Current Savings" value={formData.current_savings} onChange={handleInputChange} />
          <input className="input-field" type="number" name="total_debt" placeholder="Total Debt" value={formData.total_debt} onChange={handleInputChange} />
          <input className="input-field" type="number" name="age" placeholder="Age" value={formData.age} onChange={handleInputChange} />
          <input className="input-field" type="number" name="dependents" placeholder="Number of Dependents" value={formData.dependents} onChange={handleInputChange} />
          <select className="input-field" name="risk_tolerance" value={formData.risk_tolerance} onChange={handleInputChange}>
            <option value="low">Conservative (Low Risk)</option>
            <option value="medium">Moderate (Medium Risk)</option>
            <option value="high">Aggressive (High Risk)</option>
          </select>
          <button type="submit" className="btn btn-primary">
            {loading ? 'Creating...' : 'Create Financial Plan'}
          </button>
        </form>
        <button className="btn btn-secondary" onClick={resetForm}>Reset</button>
      </div>

      {/* Results Section */}
      <div className="result-section">
        {error && <div className="alert alert-error">{error}</div>}

        {result && (
          <div className="card">
            <h2 className="card-title">Your Personalized Financial Plan</h2>

            {/* Budget Allocation */}
            {result.plan?.budget_allocation && (
              <div className="result-card">
                <div className="result-title">Recommended Budget Allocation</div>
                <div>Needs: ${result.plan.budget_allocation.needs?.toFixed(0)} ({result.plan.budget_allocation.percentages?.needs?.toFixed(1)}%)</div>
                <div>Wants: ${result.plan.budget_allocation.wants?.toFixed(0)} ({result.plan.budget_allocation.percentages?.wants?.toFixed(1)}%)</div>
                <div>Savings: ${result.plan.budget_allocation.savings?.toFixed(0)} ({result.plan.budget_allocation.percentages?.savings?.toFixed(1)}%)</div>
              </div>
            )}

            {/* Risk Assessment */}
            {result.plan?.risk_assessment && (
              <div className="result-card">
                <div className="result-title">Risk Assessment</div>
                <div>Level: {result.plan.risk_assessment.level} Risk</div>
                <div>Score: {result.plan.risk_assessment.score}/10</div>
                {result.plan.risk_assessment.factors?.length > 0 && (
                  <div>
                    <div>Factors:</div>
                    {result.plan.risk_assessment.factors.map((f, i) => <div key={i}>• {f}</div>)}
                  </div>
                )}
              </div>
            )}

            {/* Recommendations */}
            {result.plan?.recommendations?.length > 0 && (
              <div className="result-card">
                <div className="result-title">AI Recommendations</div>
                {result.plan.recommendations.map((rec, i) => (
                  <div key={i} style={{ marginBottom: '0.5rem' }}>
                    <div style={{ fontWeight: 'bold' }}>{rec.priority?.toUpperCase()} PRIORITY</div>
                    <div>{rec.message}</div>
                    {rec.suggested_action && <div style={{ color: '#555' }}>Action: {rec.suggested_action}</div>}
                  </div>
                ))}
              </div>
            )}

            {/* Emergency Fund */}
            {result.plan?.emergency_fund && (
              <div className="result-card">
                <div className="result-title">Emergency Fund Goal</div>
                <div>Target: ${result.plan.emergency_fund.target_amount?.toFixed(0)}</div>
                <div>Current: ${result.plan.emergency_fund.current_amount?.toFixed(0)}</div>
                <div>
                  {result.plan.emergency_fund.shortfall > 0 
                    ? `Shortfall: $${result.plan.emergency_fund.shortfall.toFixed(0)}`
                    : 'Goal Achieved!'}
                </div>
              </div>
            )}
          </div>
        )}

        {!result && !error && !loading && (
          <div className="card" style={{ textAlign: 'center', color: '#555' }}>
            Fill out the form to get your personalized financial plan
          </div>
        )}
      </div>
    </div>
  );
};

export default Planner;
