import React, { useState } from "react";
import axios from "axios";

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

    const formData = new FormData();
    formData.append("pdf", pdfFile);
    formData.append("amount", amount || 0);
    formData.append("interest_rate", interestRate || 0);
    formData.append("promised_return", promisedReturn || 0);

    setLoadingFraud(true);
    try {
      const res = await axios.post(
        "http://localhost:5000/api/fraud/detect",
        formData,
        { headers: { "Content-Type": "multipart/form-data" }, timeout: 30000 }
      );
      setFraudResult(res.data);
    } catch (error) {
      console.error(error);
      alert("Error analyzing the PDF. Make sure backend is running.");
    }
    setLoadingFraud(false);
  };

  const handleSubmitPhishing = async () => {
    if (!phishingInput) {
      alert("Please enter text or a link to check for phishing.");
      return;
    }

    setLoadingPhish(true);
    try {
      const res = await axios.post(
        "http://localhost:5000/api/phishing/check",
        { input: phishingInput },
        { timeout: 20000 }
      );
      setPhishingResult(res.data);
    } catch (error) {
      console.error(error);
      alert("Error checking phishing. Make sure backend is running.");
    }
    setLoadingPhish(false);
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
      <style>{`
        .fraud-container {
          max-width: 900px;
          margin: 0 auto;
          padding: 2rem;
          font-family: 'Segoe UI', Arial, sans-serif;
          background: #f5f7fa;
        }
        .section-title { font-size: 2rem; font-weight: 900; margin-bottom: 1rem; text-align: center; }
        .section-desc { font-size: 1rem; margin-bottom: 2rem; text-align: center; color: #555; }
        .card { padding: 1.5rem; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s; margin-bottom: 1.5rem; background: white; color: black; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(0,0,0,0.12); }
        .card-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; }
        .card-desc { font-size: 0.9rem; margin-bottom: 0.5rem; }
        .card-return { font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem; }
        .input-field { width: 100%; padding: 0.75rem 1rem; margin-bottom: 1rem; border-radius: 12px; border: 1px solid #ccc; font-size: 1rem; }
        .btn { padding: 0.75rem 1.5rem; border-radius: 12px; border: none; font-weight: bold; cursor: pointer; transition: background 0.3s, transform 0.2s; margin-right: 1rem; }
        .btn-primary { background: #1976d2; color: white; }
        .btn-primary:hover { background: #115293; }
        .btn-secondary { background: white; color: #1976d2; border: 2px solid #1976d2; }
        .btn-secondary:hover { background: #f0f4fa; }
        .alert { padding: 1rem; border-radius: 12px; margin-top: 1rem; font-weight: bold; }
        .alert-success { background: #d4edda; color: #155724; }
        .alert-error { background: #f8d7da; color: #721c24; }
        .red-flags { margin-top: 1rem; }
        .red-flags li { margin-bottom: 0.5rem; }
      `}</style>

      <header style={{ textAlign: "center", marginBottom: "3rem" }}>
        <div style={{ display: "inline-block", width: "60px", height: "60px", background: "linear-gradient(135deg, #4facfe, #00f2fe)", borderRadius: "16px", color: "white", fontWeight: "bold", fontSize: "2rem", lineHeight: "60px", marginBottom: "1rem" }}>F</div>
        <h1 className="section-title">Fraud & Phishing Detection</h1>
        <p className="section-desc">Analyze investment documents or check text/links for phishing risks.</p>
      </header>

      {/* PDF Fraud Detection */}
      <div className="card">
        <h2 className="card-title">Upload PDF for Fraud Check</h2>
        <input type="file" accept="application/pdf" onChange={handleFileChange} className="input-field" />
        {pdfFile && <div className="alert alert-success">Selected: {pdfFile.name} ({(pdfFile.size / 1024 / 1024).toFixed(2)} MB)</div>}
        <input type="number" placeholder="Investment Amount (ZAR)" value={amount} onChange={e => setAmount(e.target.value)} className="input-field" />
        <input type="number" placeholder="Interest Rate (%)" value={interestRate} onChange={e => setInterestRate(e.target.value)} className="input-field" />
        <input type="number" placeholder="Promised Return (%)" value={promisedReturn} onChange={e => setPromisedReturn(e.target.value)} className="input-field" />
        <div style={{ textAlign: "center", marginTop: "1rem" }}>
          <button className="btn btn-primary" onClick={handleSubmitFraud} disabled={loadingFraud || !pdfFile}>
            {loadingFraud ? "Analyzing..." : "Analyze for Fraud"}
          </button>
        </div>
        {fraudResult && (
          <div className={`alert ${fraudResult.is_fraud ? "alert-error" : "alert-success"}`}>
            Fraud Risk: {(fraudResult.fraud_probability * 100).toFixed(1)}%<br />
            Assessment: {fraudResult.is_fraud ? "High Risk - Potentially Fraudulent" : "Low Risk - Appears Legitimate"}
          </div>
        )}
        {fraudResult?.red_flags?.length > 0 && (
          <ul className="red-flags">
            {fraudResult.red_flags.map((flag, idx) => (
              <li key={idx}>{flag}</li>
            ))}
          </ul>
        )}
      </div>

      {/* Phishing Detection */}
      <div className="card">
        <h2 className="card-title">Check Text or Link for Phishing</h2>
        <textarea
          placeholder="Paste suspicious text or link here..."
          value={phishingInput}
          onChange={e => setPhishingInput(e.target.value)}
          className="input-field"
          rows={4}
        />
        <div style={{ textAlign: "center", marginTop: "1rem" }}>
          <button className="btn btn-primary" onClick={handleSubmitPhishing} disabled={loadingPhish || !phishingInput}>
            {loadingPhish ? "Checking..." : "Check for Phishing"}
          </button>
        </div>
        {phishingResult && (
          <div className={`alert ${phishingResult.is_phishing ? "alert-error" : "alert-success"}`}>
            Phishing Risk: {(phishingResult.risk_score * 100).toFixed(1)}%<br />
            Assessment: {phishingResult.is_phishing ? "High Risk - Potentially Phishing" : "Low Risk - Appears Legitimate"}
          </div>
        )}
      </div>

      <div style={{ textAlign: "center", marginTop: "2rem" }}>
        <button className="btn btn-secondary" onClick={resetForm}>Reset All</button>
      </div>
    </div>
  );
};

export default FraudCheck;
