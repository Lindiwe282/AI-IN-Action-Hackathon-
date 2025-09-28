import React, { useState } from "react";
import { 
  Shield, 
  Upload, 
  FileText, 
  DollarSign, 
  TrendingUp, 
  Target, 
  Search, 
  AlertTriangle, 
  CheckCircle, 
  RefreshCw,
  Link,
  Mail,
  Eye,
  BarChart3
} from "lucide-react";

const FraudCheck = () => {
  const [pdfFile, setPdfFile] = useState(null);
  const [amount, setAmount] = useState("");
  const [interestRate, setInterestRate] = useState("");
  const [promisedReturn, setPromisedReturn] = useState("");
  const [fraudResult, setFraudResult] = useState(null);

  const [phishingInput, setPhishingInput] = useState("");
  const [phishingResult, setPhishingResult] = useState(null);

  const [loadingFraud, setLoadingFraud] = useState(false);
  const [loadingPhish, setLoadingPhish] = useState(false);

  // --- Handlers ---
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setPdfFile(file);
    setFraudResult(null);
  };

  const handleSubmitFraud = async () => {
    if (!pdfFile) {
      alert("Please upload a PDF file.");
      return;
    }

    setLoadingFraud(true);
    
    // Simulate API call with demo data
    setTimeout(() => {
      const mockResult = {
        fraud_probability: Math.random() > 0.7 ? 0.85 : 0.15,
        is_fraud: Math.random() > 0.7,
        red_flags: Math.random() > 0.5 ? [
          "Unusually high promised returns compared to market standards",
          "Lack of proper regulatory documentation",
          "Pressure tactics for immediate investment"
        ] : []
      };
      setFraudResult(mockResult);
      setLoadingFraud(false);
    }, 2000);
  };

  const handleSubmitPhishing = async () => {
    if (!phishingInput) {
      alert("Please enter text or a link to check for phishing.");
      return;
    }

    setLoadingPhish(true);
    
    // Simulate API call with demo data
    setTimeout(() => {
      const hasPhishingKeywords = phishingInput.toLowerCase().includes('urgent') || 
                                  phishingInput.toLowerCase().includes('click here') ||
                                  phishingInput.toLowerCase().includes('verify account') ||
                                  phishingInput.toLowerCase().includes('suspended');
      
      const mockResult = {
        risk_score: hasPhishingKeywords ? 0.9 : Math.random() * 0.3,
        is_phishing: hasPhishingKeywords || Math.random() > 0.8
      };
      setPhishingResult(mockResult);
      setLoadingPhish(false);
    }, 1500);
  };

  const resetForm = () => {
    setPdfFile(null);
    setAmount("");
    setInterestRate("");
    setPromisedReturn("");
    setFraudResult(null);
    setPhishingInput("");
    setPhishingResult(null);
  };

  return (
    <div className="fraud-container">
      <div className="content-wrapper">
        <style>{`
          .fraud-container {
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

          .card { 
            background: linear-gradient(135deg, 
              rgba(255, 255, 255, 0.95) 0%, 
              rgba(248, 250, 252, 0.9) 100%
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
            position: relative;
          }

          .card::before {
            content: '';
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: linear-gradient(90deg, #87a96b, #6b8e47);
            border-radius: 2px;
          }

          .card:hover { 
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
            content: '✦';
            color: #87a96b;
            font-size: 1rem;
          }

          .input-field { 
            width: 100%; 
            padding: 1rem 1.25rem; 
            margin-bottom: 1.25rem; 
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
            margin-right: 1rem;
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
          }

          .btn-primary:hover:not(:disabled) { 
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
            backdrop-filter: blur(10px);
          }

          .btn-secondary:hover { 
            background: rgba(135, 169, 107, 0.1);
            border-color: #87a96b;
            transform: translateY(-2px);
          }

          .alert { 
            padding: 1.25rem 1.5rem;
            border-radius: 16px;
            margin-top: 1.5rem;
            font-weight: 500;
            border: 1px solid;
            backdrop-filter: blur(10px);
          }

          .alert-success { 
            background: linear-gradient(135deg, rgba(135, 169, 107, 0.1), rgba(107, 142, 71, 0.05));
            color: #166534;
            border-color: rgba(135, 169, 107, 0.3);
          }

          .alert-error { 
            background: linear-gradient(135deg, rgba(248, 113, 113, 0.1), rgba(239, 68, 68, 0.05));
            color: #dc2626;
            border-color: rgba(248, 113, 113, 0.3);
          }

          .red-flags { 
            margin-top: 2rem;
            background: linear-gradient(135deg, rgba(248, 113, 113, 0.08) 0%, rgba(239, 68, 68, 0.05) 100%);
            border: 1px solid rgba(248, 113, 113, 0.3);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
          }

          .red-flags li { 
            margin-bottom: 0.75rem; 
            color: #dc2626;
            font-weight: 500;
            padding-left: 0.5rem;
          }

          .file-upload-area {
            border: 2px dashed rgba(135, 169, 107, 0.3);
            border-radius: 16px;
            padding: 2rem;
            text-align: center;
            background: linear-gradient(135deg, rgba(135, 169, 107, 0.05) 0%, rgba(248, 250, 252, 0.8) 100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1.5rem;
            backdrop-filter: blur(10px);
          }

          .file-upload-area:hover {
            border-color: #87a96b;
            background: linear-gradient(135deg, rgba(135, 169, 107, 0.08) 0%, rgba(248, 250, 252, 0.9) 100%);
            transform: translateY(-2px);
          }

          .file-upload-area input[type="file"] {
            display: none;
          }

          .file-upload-label {
            cursor: pointer;
            color: #6b8e47;
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
          }

          .progress-bar {
            width: 100%;
            height: 6px;
            background: rgba(135, 169, 107, 0.2);
            border-radius: 8px;
            overflow: hidden;
            margin-top: 1.5rem;
          }

          .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #87a96b 0%, #6b8e47 100%);
            border-radius: 8px;
            animation: progress 2s ease-in-out infinite;
          }

          @keyframes progress {
            0% { width: 0%; }
            50% { width: 70%; }
            100% { width: 100%; }
          }

          .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-top: 2rem;
          }

          .stat-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(248, 250, 252, 0.8) 100%);
            border: 1px solid rgba(135, 169, 107, 0.15);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          }

          .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(135, 169, 107, 0.15);
            border-color: rgba(135, 169, 107, 0.25);
          }

          .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
          }

          .stat-label {
            color: #64748b;
            font-weight: 500;
          }

          @media (max-width: 768px) {
            .fraud-container {
              padding: 5rem 1rem 1rem;
            }
            
            .main-title {
              font-size: 2.5rem;
            }
            
            .card {
              padding: 1.5rem;
            }
            
            .stats-grid {
              grid-template-columns: 1fr;
              gap: 1rem;
            }
          }
        `}</style>

        <header className="header-section">
          <div className="header-decoration"></div>
          <h1 className="main-title">AI Security Guardian</h1>
          <p className="main-subtitle">
            Advanced fraud detection and phishing protection powered by AI. 
            Safeguard your financial interests and personal data with intelligent analysis.
          </p>
        </header>

        {/* PDF Fraud Detection */}
        <div className="card">
          <h2 className="card-title">Investment Document Analysis</h2>
          
          <div className="file-upload-area">
            <label htmlFor="pdf-upload" className="file-upload-label">
              <Upload size={24} />
              Click to upload PDF document or drag and drop
              <input 
                id="pdf-upload"
                type="file" 
                accept="application/pdf" 
                onChange={handleFileChange}
              />
            </label>
          </div>
          
          {pdfFile && (
            <div className="alert alert-success">
              <CheckCircle size={20} style={{ marginRight: '0.5rem', verticalAlign: 'middle' }} />
              Selected: {pdfFile.name} ({(pdfFile.size / 1024 / 1024).toFixed(2)} MB)
            </div>
          )}
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1rem' }}>
            <div style={{ position: 'relative' }}>
              <DollarSign size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b8e47', zIndex: 1 }} />
              <input 
                type="number" 
                placeholder="Investment Amount (ZAR)" 
                value={amount} 
                onChange={e => setAmount(e.target.value)} 
                className="input-field"
                style={{ paddingLeft: '3rem' }}
              />
            </div>
            <div style={{ position: 'relative' }}>
              <TrendingUp size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b8e47', zIndex: 1 }} />
              <input 
                type="number" 
                placeholder="Interest Rate (%)" 
                value={interestRate} 
                onChange={e => setInterestRate(e.target.value)} 
                className="input-field"
                style={{ paddingLeft: '3rem' }}
              />
            </div>
            <div style={{ position: 'relative' }}>
              <Target size={20} style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)', color: '#6b8e47', zIndex: 1 }} />
              <input 
                type="number" 
                placeholder="Promised Return (%)" 
                value={promisedReturn} 
                onChange={e => setPromisedReturn(e.target.value)} 
                className="input-field"
                style={{ paddingLeft: '3rem' }}
              />
            </div>
          </div>
          
          <div style={{ textAlign: "center", marginTop: "2rem" }}>
            <button 
              className="btn btn-primary" 
              onClick={handleSubmitFraud} 
              disabled={loadingFraud || !pdfFile}
            >
              <Search size={20} />
              {loadingFraud ? "Analyzing..." : "Analyze for Fraud"}
            </button>
          </div>
          
          {loadingFraud && (
            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
          )}
          
          {fraudResult && (
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">
                  <BarChart3 size={24} />
                  {(fraudResult.fraud_probability * 100).toFixed(1)}%
                </div>
                <div className="stat-label">Fraud Risk Score</div>
              </div>
              <div className="stat-card">
                <div className="stat-value" style={{ color: fraudResult.is_fraud ? '#dc2626' : '#166534' }}>
                  {fraudResult.is_fraud ? (
                    <><AlertTriangle size={24} />HIGH RISK</>
                  ) : (
                    <><CheckCircle size={24} />LOW RISK</>
                  )}
                </div>
                <div className="stat-label">Assessment</div>
              </div>
            </div>
          )}
          
          {fraudResult?.red_flags?.length > 0 && (
            <div className="red-flags">
              <h4 style={{ margin: '0 0 1rem 0', color: '#dc2626', display: 'flex', alignItems: 'center' }}>
                <AlertTriangle size={20} style={{ marginRight: '0.5rem' }} />
                Warning Signs Detected:
              </h4>
              <ul style={{ margin: 0, paddingLeft: '1.5rem' }}>
                {fraudResult.red_flags.map((flag, idx) => (
                  <li key={idx}>{flag}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Phishing Detection */}
        <div className="card">
          <h2 className="card-title">Phishing & Scam Detection</h2>
          <div style={{ position: 'relative' }}>
            <Link size={20} style={{ position: 'absolute', left: '1rem', top: '1.5rem', color: '#6b8e47', zIndex: 1 }} />
            <textarea
              placeholder="Paste suspicious text, email content, or website link here for analysis..."
              value={phishingInput}
              onChange={e => setPhishingInput(e.target.value)}
              className="input-field"
              rows={5}
              style={{ resize: 'vertical', minHeight: '120px', paddingLeft: '3rem' }}
            />
          </div>
          
          <div style={{ textAlign: "center", marginTop: "1.5rem" }}>
            <button 
              className="btn btn-primary" 
              onClick={handleSubmitPhishing} 
              disabled={loadingPhish || !phishingInput}
            >
              <Eye size={20} />
              {loadingPhish ? "Checking..." : "Check for Phishing"}
            </button>
          </div>
          
          {loadingPhish && (
            <div className="progress-bar">
              <div className="progress-fill"></div>
            </div>
          )}
          
          {phishingResult && (
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-value">
                  <BarChart3 size={24} />
                  {(phishingResult.risk_score * 100).toFixed(1)}%
                </div>
                <div className="stat-label">Phishing Risk Score</div>
              </div>
              <div className="stat-card">
                <div className="stat-value" style={{ color: phishingResult.is_phishing ? '#dc2626' : '#166534' }}>
                  {phishingResult.is_phishing ? (
                    <><AlertTriangle size={24} />SUSPICIOUS</>
                  ) : (
                    <><CheckCircle size={24} />SAFE</>
                  )}
                </div>
                <div className="stat-label">Assessment</div>
              </div>
            </div>
          )}
        </div>

        <div style={{ textAlign: "center", marginTop: "3rem" }}>
          <button className="btn btn-secondary" onClick={resetForm}>
            <RefreshCw size={20} />
            Reset All Forms
          </button>
        </div>
      </div>
    </div>
  );
};

export default FraudCheck;