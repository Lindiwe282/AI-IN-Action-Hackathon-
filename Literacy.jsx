import React, { useState } from "react";

const Literacy = () => {
  const [section, setSection] = useState("menu");

  const investments = [
    {
      title: "Savings Accounts & Fixed Deposits",
      level: "Ultra Safe",
      return: "R50 - R250 per R5,000 yearly",
      desc: "Your money is 100% safe with banks like FNB or Standard Bank. Low-risk, ideal for short-term goals or emergency funds.",
      example: "Put R10,000 in a savings account at 5% = R500 interest per year",
      gradient: "green",
    },
    {
      title: "Government Bonds (RSA Retail Bonds)",
      level: "Very Safe",
      return: "R100 - R300 per R5,000 yearly",
      desc: "Government bonds are loans you give to the South African government. Very secure and pay periodic interest.",
      example: "R5,000 government bond at 6% = R300 yearly",
      gradient: "blue",
    },
    {
      title: "Corporate Bonds & Unit Trusts",
      level: "Moderately Safe",
      return: "R150 - R400 per R5,000 yearly",
      desc: "Invest in companies with moderate growth potential. Higher returns than government bonds but some risk.",
      example: "Allan Gray unit trust: R5,000 could grow by R350+ annually",
      gradient: "amber",
    },
    {
      title: "JSE Index Funds (Top 40)",
      level: "Moderate Risk",
      return: "R300 - R500 per R5,000 yearly",
      desc: "Own pieces of South Africa's top 40 companies. Diversified and historically solid growth.",
      example: "Satrix Top 40 ETF: R10,000 historically grows R800-1,200 per year",
      gradient: "purple",
    },
    {
      title: "Individual JSE Stocks",
      level: "High Risk",
      return: "R0 - R2,500+ per R5,000 yearly",
      desc: "High-risk, high-reward. Prices fluctuate based on market trends and company performance.",
      example: "Naspers stock: R5,000 could become R0 or R15,000+ in a year",
      gradient: "orange",
    },
    {
      title: "Crypto (Bitcoin, Ethereum)",
      level: "Extreme Risk",
      return: "R0 - R25,000+ per R5,000 yearly",
      desc: "Highly volatile digital assets. Only invest money you can afford to lose.",
      example: "R1,000 in Bitcoin could become R100 or R10,000 within months",
      gradient: "red",
    },
  ];

  const interestConcepts = [
    {
      title: "What is Interest?",
      desc: "Interest is the cost of borrowing money or the reward for saving it. It is expressed as a percentage rate.",
      examples: [],
      gradient: "blue",
    },
    {
      title: "Simple Interest",
      desc: "Calculated only on the original principal. Formula: SI = P × R × T.",
      examples: [
        "Loan Example: Borrow R10,000 at 10% per year for 3 years → Interest = R3,000",
        "Investment Example: Deposit R5,000 at 6% for 2 years → Interest = R600"
      ],
      gradient: "green"
    },
    {
      title: "Compound Interest",
      desc: "Calculated on principal + accumulated interest. Formula: CI = P × (1 + R/n)^(n×T) - P.",
      examples: [
        "Investment: R5,000 at 6% annually, compounded quarterly for 2 years → ≈ R636 interest",
        "Loan: R10,000 at 10% annually, compounded monthly for 3 years → ≈ R3,347 interest"
      ],
      gradient: "purple"
    },
    {
      title: "Compounding Periods",
      desc: "How often interest is applied: annually, semi-annually, quarterly, monthly, daily. More frequent compounding increases total interest.",
      examples: [
        "Monthly vs annually: R5,000 at 6% compounded monthly earns more than annually",
        "Short-term loan compounded daily accumulates more interest than monthly"
      ],
      gradient: "amber"
    }
  ];

  const renderMenu = () => (
    <div className="menu-buttons" style={{ display: "flex", flexDirection: "column", gap: "2rem", alignItems: "center", marginTop: "4rem" }}>
      <h2 style={{ textAlign: "center" }}>Select a Financial Knowledge Section</h2>
      <button className="menu-btn" onClick={() => setSection("investments")}>📈 Investments</button>
      <button className="menu-btn" onClick={() => setSection("interest")}>💰 Interest</button>
      <button className="menu-btn" onClick={() => setSection("quiz")}>📝 Test Your Knowledge</button>
    </div>
  );

  const renderCards = (items) => (
    <div className="grid-container">
      {items.map((item, idx) => (
        <div key={idx} className={`card gradient-${item.gradient}`}>
          <h4 className="card-title">{item.title}</h4>
          <p className="card-desc">{item.desc}</p>
          {item.examples && item.examples.map((ex, i) => <div key={i} className="card-example">{ex}</div>)}
        </div>
      ))}
    </div>
  );

  const renderSection = () => {
    switch(section) {
      case "investments":
        return (
          <section>
            <button onClick={() => setSection("menu")} style={{ marginBottom: "1rem" }}>⬅ Back</button>
            <h2 className="section-title">Investments</h2>
            <p className="section-desc">Learn about different types of investments from safe to risky.</p>
            {renderCards(investments)}
          </section>
        );
      case "interest":
        return (
          <section>
            <button onClick={() => setSection("menu")} style={{ marginBottom: "1rem" }}>⬅ Back</button>
            <h2 className="section-title">Interest Rates</h2>
            <p className="section-desc">Understand interest, simple interest, compound interest, and compounding periods.</p>
            {renderCards(interestConcepts)}
          </section>
        );
      case "quiz":
        return (
          <section>
            <button onClick={() => setSection("menu")} style={{ marginBottom: "1rem" }}>⬅ Back</button>
            <h2 className="section-title">Test Your Financial Knowledge</h2>
            <p className="section-desc">Coming soon: A fun quiz to test your understanding of financial concepts!</p>
          </section>
        );
      default:
        return renderMenu();
    }
  };

  return (
    <div className="literacy-container">
      <style>{`
        .literacy-container { max-width: 900px; margin: 0 auto; padding: 2rem; font-family: 'Segoe UI', Arial, sans-serif; background: #f5f7fa; }
        .menu-btn { font-size: 1.25rem; padding: 1rem 2rem; border-radius: 12px; border: none; cursor: pointer; background: #1976d2; color: white; transition: background 0.3s; }
        .menu-btn:hover { background: #115293; }
        .grid-container { display: flex; flex-direction: column; gap: 2rem; }
        .card { padding: 1.5rem; border-radius: 16px; color: white; box-shadow: 0 10px 20px rgba(0,0,0,0.08); transition: transform 0.3s, box-shadow 0.3s; width: 100%; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(0,0,0,0.12); }
        .card-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color: black; }
        .card-desc { font-size: 0.9rem; margin-bottom: 0.5rem; color: black; }
        .card-example { background: rgba(255,255,255,0.15); padding: 0.5rem; border-radius: 12px; font-size: 0.8rem; color: black; margin-bottom: 0.25rem; }
        .gradient-green { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .gradient-blue { background: linear-gradient(135deg, #3a7bd5, #00d2ff); }
        .gradient-amber { background: linear-gradient(135deg, #f7971e, #ffd200); }
        .gradient-purple { background: linear-gradient(135deg, #7b2ff7, #f107a3); }
        .gradient-orange { background: linear-gradient(135deg, #f953c6, #b91d73); }
        .gradient-red { background: linear-gradient(135deg, #ff416c, #ff4b2b); }
      `}</style>

      <header className="header" style={{ textAlign: "center", marginBottom: "4rem" }}>
        <div className="logo" style={{ display: "inline-block", width: "60px", height: "60px", background: "linear-gradient(135deg, #4facfe, #00f2fe)", borderRadius: "16px", color: "white", fontWeight: "bold", fontSize: "2rem", lineHeight: "60px", marginBottom: "1rem" }}>R</div>
        <h1 className="title" style={{ fontSize: "3rem", fontWeight: 900 }}>Financial Literacy Hub</h1>
        <p className="subtitle" style={{ fontSize: "1.2rem", color: "#555", maxWidth: "800px", margin: "0 auto" }}>
          Master your finances with practical South African examples — from safe savings to bold investments — all explained in Rands you can relate to.
        </p>
      </header>

      {renderSection()}
    </div>
  );
};

export default Literacy;
