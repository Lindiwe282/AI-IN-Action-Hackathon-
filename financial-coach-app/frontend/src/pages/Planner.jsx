import React, { useState } from 'react';

// Mock API endpoints for demo
const apiEndpoints = {
  createPlan: async (data) => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mock response with sample data
    return {
      data: {
        plan: {
          budget_allocation: {
            needs: data.monthly_income * 0.5,
            wants: data.monthly_income * 0.3,
            savings: data.monthly_income * 0.2,
            percentages: {
              needs: 50,
              wants: 30,
              savings: 20
            }
          },
          risk_assessment: {
            level: data.risk_tolerance === 'high' ? 'High' : data.risk_tolerance === 'low' ? 'Low' : 'Medium',
            score: data.risk_tolerance === 'high' ? 8 : data.risk_tolerance === 'low' ? 3 : 6,
            factors: ['Age-appropriate risk level', 'Income stability', 'Debt-to-income ratio']
          },
          recommendations: [
            {
              priority: 'high',
              message: 'Build an emergency fund covering 3-6 months of expenses',
              suggested_action: 'Set up automatic transfer of $200/month to savings'
            },
            {
              priority: 'medium',
              message: 'Consider increasing retirement contributions',
              suggested_action: 'Increase 401k contribution by 2%'
            }
          ],
          emergency_fund: {
            target_amount: data.monthly_expenses * 6,
            current_amount: data.current_savings,
            shortfall: Math.max(0, (data.monthly_expenses * 6) - data.current_savings)
          }
        }
      }
    };
  }
};

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

  const handleSubmit = async () => {
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
          min-height: 100vh;
          background: linear-gradient(135deg, 
            rgba(248, 250, 252, 1) 0%, 
            rgba(241, 245, 249, 1) 25%,
            rgba(226, 232, 240, 1) 50%,
            rgba(241, 245, 249, 1) 75%,
            rgba(248, 250, 252, 1) 100%
          );
          padding: 6rem 2rem 2rem;
          font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
        }
        
        .content-wrapper {
          max-width: 1000px;
          margin: 0 auto;
        }
        
        .header-section {
          text-align: center;
          margin-bottom: 3rem;
          position: relative;
        }
        
        .header-decoration {
          position: absolute;
          top: -20px;
          left: 50%;
          transform: translateX(-50%);
          width: 100px;
          height: 4px;
          background: linear-gradient(90deg, #87a96b, #6b8e47);
          border-radius: 2px;
        }
        
        .main-title {
          font-size: 3rem;
          font-weight: 800;
          margin-bottom: 0.75rem;
          background: linear-gradient(135deg, #1e293b 0%, #475569 50%, #6b8e47 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          line-height: 1.1;
        }
        
        .main-subtitle {
          font-size: 1.25rem;
          color: #64748b;
          font-weight: 400;
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.5;
        }
        
        .form-card {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.9) 0%, 
            rgba(248, 250, 252, 0.95) 100%
          );
          backdrop-filter: blur(20px);
          border: 1px solid rgba(135, 169, 107, 0.2);
          border-radius: 24px;
          padding: 2.5rem;
          margin-bottom: 2rem;
          box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.08),
            0 0 0 1px rgba(135, 169, 107, 0.1);
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .form-card:hover {
          transform: translateY(-4px);
          box-shadow: 
            0 32px 64px rgba(0, 0, 0, 0.12),
            0 0 0 1px rgba(135, 169, 107, 0.2);
        }
        
        .card-title {
          font-size: 1.5rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1.5rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        
        .card-title::before {
          content: '';
          width: 6px;
          height: 24px;
          background: linear-gradient(135deg, #87a96b, #6b8e47);
          border-radius: 3px;
        }
        
        .form-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }
        
        .input-group {
          position: relative;
        }
        
        .input-field {
          width: 100%;
          padding: 1rem 1.25rem;
          border: 2px solid rgba(135, 169, 107, 0.2);
          border-radius: 16px;
          font-size: 1rem;
          font-weight: 500;
          background: rgba(248, 250, 252, 0.8);
          color: #1e293b;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          box-sizing: border-box;
        }
        
        .input-field:focus {
          outline: none;
          border-color: #87a96b;
          background: rgba(255, 255, 255, 0.95);
          box-shadow: 
            0 0 0 4px rgba(135, 169, 107, 0.1),
            0 8px 16px rgba(135, 169, 107, 0.1);
          transform: translateY(-2px);
        }
        
        .input-field::placeholder {
          color: #94a3b8;
          font-weight: 400;
        }
        
        .select-field {
          appearance: none;
          background-image: linear-gradient(45deg, transparent 50%, #87a96b 50%),
                            linear-gradient(135deg, #87a96b 50%, transparent 50%);
          background-position: calc(100% - 20px) calc(1rem + 2px),
                               calc(100% - 15px) calc(1rem + 2px);
          background-size: 5px 5px, 5px 5px;
          background-repeat: no-repeat;
          cursor: pointer;
        }
        
        .btn {
          padding: 1rem 2rem;
          border-radius: 16px;
          border: none;
          font-weight: 600;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
          text-decoration: none;
          position: relative;
          overflow: hidden;
        }
        
        .btn::before {
          content: '';
          position: absolute;
          inset: 0;
          background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.3) 50%, transparent 70%);
          transform: translateX(-100%);
          transition: transform 0.6s;
        }
        
        .btn:hover::before {
          transform: translateX(100%);
        }
        
        .btn-primary {
          background: linear-gradient(135deg, #87a96b 0%, #6b8e47 100%);
          color: white;
          box-shadow: 0 8px 20px rgba(135, 169, 107, 0.3);
          width: 100%;
          margin-bottom: 1rem;
        }
        
        .btn-primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 12px 28px rgba(135, 169, 107, 0.4);
        }
        
        .btn-primary:disabled {
          opacity: 0.7;
          cursor: not-allowed;
          transform: none;
        }
        
        .btn-secondary {
          background: rgba(248, 250, 252, 0.9);
          color: #6b8e47;
          border: 2px solid rgba(135, 169, 107, 0.3);
          width: 100%;
        }
        
        .btn-secondary:hover {
          background: rgba(135, 169, 107, 0.1);
          border-color: #87a96b;
          transform: translateY(-2px);
        }
        
        .alert {
          padding: 1.25rem 1.5rem;
          border-radius: 16px;
          margin-bottom: 2rem;
          font-weight: 500;
          border: 1px solid;
          backdrop-filter: blur(10px);
        }
        
        .alert-error {
          background: linear-gradient(135deg, rgba(248, 113, 113, 0.1), rgba(239, 68, 68, 0.05));
          color: #dc2626;
          border-color: rgba(248, 113, 113, 0.3);
        }
        
        .alert-success {
          background: linear-gradient(135deg, rgba(135, 169, 107, 0.1), rgba(107, 142, 71, 0.05));
          color: #166534;
          border-color: rgba(135, 169, 107, 0.3);
        }
        
        .results-section {
          margin-top: 2rem;
        }
        
        .result-card {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 250, 252, 0.9) 100%
          );
          border: 1px solid rgba(135, 169, 107, 0.15);
          border-radius: 20px;
          padding: 2rem;
          margin-bottom: 1.5rem;
          backdrop-filter: blur(15px);
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.06);
          transition: all 0.3s ease;
        }
        
        .result-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
        }
        
        .result-title {
          font-size: 1.25rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        
        .result-title::before {
          content: '✦';
          color: #87a96b;
          font-size: 1rem;
        }
        
        .budget-item, .metric-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 0;
          border-bottom: 1px solid rgba(135, 169, 107, 0.1);
          color: #475569;
          font-weight: 500;
        }
        
        .budget-item:last-child, .metric-item:last-child {
          border-bottom: none;
        }
        
        .budget-amount {
          font-weight: 700;
          color: #1e293b;
        }
        
        .recommendation-item {
          background: rgba(135, 169, 107, 0.05);
          border: 1px solid rgba(135, 169, 107, 0.15);
          border-radius: 12px;
          padding: 1.25rem;
          margin-bottom: 1rem;
          transition: all 0.3s ease;
        }
        
        .recommendation-item:hover {
          background: rgba(135, 169, 107, 0.08);
          border-color: rgba(135, 169, 107, 0.25);
        }
        
        .priority-badge {
          display: inline-block;
          padding: 0.25rem 0.75rem;
          border-radius: 20px;
          font-size: 0.75rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.5px;
          margin-bottom: 0.5rem;
        }
        
        .priority-high {
          background: linear-gradient(135deg, #ef4444, #dc2626);
          color: white;
        }
        
        .priority-medium {
          background: linear-gradient(135deg, #f59e0b, #d97706);
          color: white;
        }
        
        .priority-low {
          background: linear-gradient(135deg, #87a96b, #6b8e47);
          color: white;
        }
        
        .recommendation-message {
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 0.5rem;
        }
        
        .recommendation-action {
          color: #64748b;
          font-style: italic;
        }
        
        .empty-state {
          text-align: center;
          padding: 3rem 2rem;
          color: #64748b;
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.6) 0%, 
            rgba(248, 250, 252, 0.8) 100%
          );
          border: 2px dashed rgba(135, 169, 107, 0.3);
          border-radius: 20px;
          backdrop-filter: blur(10px);
        }
        
        .loading-spinner {
          width: 20px;
          height: 20px;
          border: 2px solid transparent;
          border-top: 2px solid currentColor;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
        
        @media (max-width: 768px) {
          .planner-container {
            padding: 5rem 1rem 1rem;
          }
          
          .main-title {
            font-size: 2.5rem;
          }
          
          .form-card {
            padding: 1.5rem;
          }
          
          .form-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
          }
        }
      `}</style>

      <div className="content-wrapper">
        <header className="header-section">
          <div className="header-decoration"></div>
          <h1 className="main-title">AI Financial Planner</h1>
          <p className="main-subtitle">
            Get personalized financial recommendations based on your current situation and goals. 
            Let our AI help you build a secure financial future.
          </p>
        </header>

        {/* Input Form */}
        <div className="form-card">
          <h2 className="card-title">Your Financial Information</h2>
          <div>
            <div className="form-grid">
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="monthly_income" 
                  placeholder="Monthly Income ($)" 
                  value={formData.monthly_income} 
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="monthly_expenses" 
                  placeholder="Monthly Expenses ($)" 
                  value={formData.monthly_expenses} 
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="current_savings" 
                  placeholder="Current Savings ($)" 
                  value={formData.current_savings} 
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="total_debt" 
                  placeholder="Total Debt ($)" 
                  value={formData.total_debt} 
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="age" 
                  placeholder="Age" 
                  value={formData.age} 
                  onChange={handleInputChange}
                />
              </div>
              
              <div className="input-group">
                <input 
                  className="input-field" 
                  type="number" 
                  name="dependents" 
                  placeholder="Number of Dependents" 
                  value={formData.dependents} 
                  onChange={handleInputChange}
                />
              </div>
            </div>
            
            <div className="input-group" style={{ marginBottom: '2rem' }}>
              <select 
                className="input-field select-field" 
                name="risk_tolerance" 
                value={formData.risk_tolerance} 
                onChange={handleInputChange}
              >
                <option value="low">Conservative (Low Risk)</option>
                <option value="medium">Moderate (Medium Risk)</option>
                <option value="high">Aggressive (High Risk)</option>
              </select>
            </div>
            
            <button 
              type="button" 
              className="btn btn-primary" 
              disabled={loading || !formData.monthly_income || !formData.monthly_expenses}
              onClick={handleSubmit}
            >
              {loading && <div className="loading-spinner"></div>}
              {loading ? 'Creating Your Plan...' : 'Create Financial Plan'}
            </button>
          </div>
          <button className="btn btn-secondary" onClick={resetForm}>
            Reset Form
          </button>
        </div>

        {/* Results Section */}
        <div className="results-section">
          {error && <div className="alert alert-error">{error}</div>}

          {result && (
            <div className="form-card">
              <h2 className="card-title">Your Personalized Financial Plan</h2>

              {/* Budget Allocation */}
              {result.plan?.budget_allocation && (
                <div className="result-card">
                  <div className="result-title">Recommended Budget Allocation</div>
                  <div className="budget-item">
                    <span>Essential Needs</span>
                    <span className="budget-amount">
                      ${result.plan.budget_allocation.needs?.toFixed(0)} ({result.plan.budget_allocation.percentages?.needs?.toFixed(1)}%)
                    </span>
                  </div>
                  <div className="budget-item">
                    <span>Discretionary Wants</span>
                    <span className="budget-amount">
                      ${result.plan.budget_allocation.wants?.toFixed(0)} ({result.plan.budget_allocation.percentages?.wants?.toFixed(1)}%)
                    </span>
                  </div>
                  <div className="budget-item">
                    <span>Savings & Investment</span>
                    <span className="budget-amount">
                      ${result.plan.budget_allocation.savings?.toFixed(0)} ({result.plan.budget_allocation.percentages?.savings?.toFixed(1)}%)
                    </span>
                  </div>
                </div>
              )}

              {/* Risk Assessment */}
              {result.plan?.risk_assessment && (
                <div className="result-card">
                  <div className="result-title">Risk Assessment</div>
                  <div className="metric-item">
                    <span>Risk Level</span>
                    <span className="budget-amount">{result.plan.risk_assessment.level} Risk</span>
                  </div>
                  <div className="metric-item">
                    <span>Risk Score</span>
                    <span className="budget-amount">{result.plan.risk_assessment.score}/10</span>
                  </div>
                  {result.plan.risk_assessment.factors?.length > 0 && (
                    <div style={{ marginTop: '1rem' }}>
                      <div style={{ fontWeight: '600', marginBottom: '0.5rem', color: '#1e293b' }}>Assessment Factors:</div>
                      {result.plan.risk_assessment.factors.map((f, i) => (
                        <div key={i} style={{ padding: '0.25rem 0', color: '#64748b' }}>• {f}</div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Recommendations */}
              {result.plan?.recommendations?.length > 0 && (
                <div className="result-card">
                  <div className="result-title">AI Recommendations</div>
                  {result.plan.recommendations.map((rec, i) => (
                    <div key={i} className="recommendation-item">
                      <div className={`priority-badge priority-${rec.priority?.toLowerCase()}`}>
                        {rec.priority?.toUpperCase()} PRIORITY
                      </div>
                      <div className="recommendation-message">{rec.message}</div>
                      {rec.suggested_action && (
                        <div className="recommendation-action">Action: {rec.suggested_action}</div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* Emergency Fund */}
              {result.plan?.emergency_fund && (
                <div className="result-card">
                  <div className="result-title">Emergency Fund Goal</div>
                  <div className="metric-item">
                    <span>Target Amount</span>
                    <span className="budget-amount">${result.plan.emergency_fund.target_amount?.toFixed(0)}</span>
                  </div>
                  <div className="metric-item">
                    <span>Current Amount</span>
                    <span className="budget-amount">${result.plan.emergency_fund.current_amount?.toFixed(0)}</span>
                  </div>
                  <div className="metric-item">
                    <span>
                      {result.plan.emergency_fund.shortfall > 0 ? 'Shortfall' : 'Status'}
                    </span>
                    <span className="budget-amount" style={{ 
                      color: result.plan.emergency_fund.shortfall > 0 ? '#dc2626' : '#16a34a'
                    }}>
                      {result.plan.emergency_fund.shortfall > 0 
                        ? `$${result.plan.emergency_fund.shortfall.toFixed(0)}`
                        : 'Goal Achieved! ✓'}
                    </span>
                  </div>
                </div>
              )}
            </div>
          )}

         
        </div>
      </div>
    </div>
  );
};

export default Planner;