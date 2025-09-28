import React, { useState } from "react";

const Literacy = () => {
  const [section, setSection] = useState("menu");
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizScore, setQuizScore] = useState(0);
  const [xpEarned, setXpEarned] = useState(0);
  const [currentQuestion, setCurrentQuestion] = useState(0);

  const investments = [
    {
      title: "Savings Accounts & Fixed Deposits",
      level: "Ultra Safe",
      return: "R50 - R250 per R5,000 yearly",
      desc: "Your money is 100% safe with banks. These are low-risk options, ideal for short-term goals or emergency funds. They earn interest steadily, but returns are usually lower than other investments.",
      example: "Put R10,000 in a savings account at 5% = R500 interest per year",
      gradient: "green",
    },
    {
      title: "Government Bonds (RSA Retail Bonds)",
      level: "Very Safe",
      return: "R100 - R300 per R5,000 yearly",
      desc: "Government bonds are loans you give to the South African government. They are very secure and pay periodic interest, but inflation can slightly reduce real returns. Suitable for conservative investors.",
      example: "R5,000 government bond at 6% = R300 yearly",
      gradient: "blue",
    },
    {
      title: "Corporate Bonds & Unit Trusts",
      level: "Moderately Safe",
      return: "R150 - R400 per R5,000 yearly",
      desc: "Corporate bonds and unit trusts invest in companies. Returns are higher than government bonds but carry some company risk. They are generally stable, with moderate growth potential.",
      example: "Allan Gray unit trust: R5,000 could grow by R350+ annually",
      gradient: "amber",
    },
    {
      title: "JSE Index Funds (Top 40)",
      level: "Moderate Risk",
      return: "R300 - R500 per R5,000 yearly",
      desc: "Index funds let you own pieces of South Africa's top 40 companies. They are diversified and reduce single-stock risk, providing solid historical growth over time.",
      example: "Satrix Top 40 ETF: R10,000 historically grows R800-1,200 per year",
      gradient: "purple",
    },
    {
      title: "Individual JSE Stocks",
      level: "High Risk",
      return: "R0 - R2,500+ per R5,000 yearly",
      desc: "Buying individual stocks is high-risk, high-reward. Prices fluctuate based on market trends and company performance. Can lead to large gains or losses.",
      example: "Naspers stock: R5,000 could become R0 or R15,000+ in a year",
      gradient: "orange",
    },
    {
      title: "Crypto (Bitcoin, Ethereum)",
      level: "Extreme Risk",
      return: "R0 - R25,000+ per R5,000 yearly",
      desc: "Cryptocurrencies are highly volatile digital assets. Prices can soar or crash quickly. Only invest money you can afford to lose, as potential gains and losses are extreme.",
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
      desc: "Calculated only on the original principal amount. Formula: Simple Interest = Principal × Rate × Time.",
      examples: [
        "Loan Example: Borrow R10,000 at 10% per year for 3 years → Interest = R3,000",
        "Investment Example: Deposit R5,000 at 6% for 2 years → Interest = R600"
      ],
      gradient: "green"
    },
    {
      title: "Compound Interest",
      desc: "Calculated on the principal amount plus any accumulated interest. Formula: Compound Interest = Principal × (1 + Rate / Number of times interest applied per year)^(Number of times interest applied × Years) - Principal.",
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

  //quiz questions covering Investments and Interest
  const quizQuestions = [
    {
      question: "Which investment is considered ultra-safe?",
      options: ["Individual Stocks", "Savings Accounts & Fixed Deposits", "Crypto", "Corporate Bonds"],
      answer: "Savings Accounts & Fixed Deposits",
    },
    {
      question: "Government bonds are best described as:",
      options: ["High-risk investments", "Loans to banks", "Loans to the government", "Speculative assets"],
      answer: "Loans to the government",
    },
    {
      question: "Compound interest is calculated on:",
      options: ["Only the principal", "Principal plus accumulated interest", "Only interest", "Inflation-adjusted principal"],
      answer: "Principal plus accumulated interest",
    },
    {
      question: "Which investment type has the potential for the highest returns?",
      options: ["Crypto", "Savings Accounts", "Government Bonds", "Unit Trusts"],
      answer: "Crypto",
    },
    {
      question: "Simple interest formula is:",
      options: ["Principal × Rate × Time", "Principal × (1 + Rate)^Time", "Rate × Time", "Principal ÷ Time"],
      answer: "Principal × Rate × Time",
    },
    {
      question: "JSE Index Funds provide:",
      options: ["High single-stock risk", "Diversification across top companies", "Guaranteed returns", "Fixed deposits"],
      answer: "Diversification across top companies",
    },
    {
      question: "Which investment is considered high-risk?",
      options: ["Corporate Bonds", "Government Bonds", "Individual Stocks", "Savings Accounts"],
      answer: "Individual Stocks",
    },
    {
      question: "More frequent compounding results in:",
      options: ["Lower total interest", "Higher total interest", "No change in interest", "Negative interest"],
      answer: "Higher total interest",
    },
    {
      question: "If you deposit R5,000 at 6% simple interest for 2 years, how much interest will you earn?",
      options: ["R300", "R600", "R500", "R550"],
      answer: "R600",
    },
    {
      question: "Crypto investment can lead to:",
      options: ["Stable returns", "Guaranteed profits", "Large gains or losses", "No risk at all"],
      answer: "Large gains or losses",
    },
  ];

  const handleAnswerChange = (option) => {
    setQuizAnswers(prev => ({ ...prev, [currentQuestion]: option }));
  };

  const handleSubmitQuiz = () => {
    let correctCount = 0;
    quizQuestions.forEach((q, idx) => {
      if (quizAnswers[idx] === q.answer) correctCount++;
    });
    const percent = (correctCount / quizQuestions.length) * 100;
    setQuizScore(percent);

    let xp = 0;
    if (percent === 100) xp = 50;
    else if (percent >= 80) xp = 40;
    else if (percent >= 50) xp = 30;
    setXpEarned(xp);
    setQuizSubmitted(true);
  };

  const renderMenu = () => (
    <div className="menu-buttons" style={{ display: "flex", flexDirection: "column", gap: "2rem", alignItems: "center", marginTop: "4rem" }}>
      <h2 style={{ textAlign: "center" }}>Select a Financial Knowledge Section</h2>
      <button className="menu-btn" onClick={() => setSection("investments")}>Investments</button>
      <button className="menu-btn" onClick={() => setSection("interest")}>Interest</button>
      <button className="menu-btn" onClick={() => setSection("quiz")}>Test Your Knowledge</button>
    </div>
  );

  const renderCards = (items, showReturn = false) => (
    <div className="grid-container">
      {items.map((item, idx) => (
        <div key={idx} className={`card gradient-${item.gradient}`}>
          {item.level && <div className="card-level">{item.level}</div>}
          <h4 className="card-title">{item.title}</h4>
          <p className="card-desc">{item.desc}</p>
          {showReturn && <p className="card-return"> Typical return: {item.return}</p>}
          {item.examples && item.examples.map((ex, i) => (
            <div key={i} className="card-example">{ex}</div>
          ))}
        </div>
      ))}
    </div>
  );

  const renderQuiz = () => {
  const q = quizQuestions[currentQuestion];

  return (
    <div>
      {renderBackButton()}
      <h2 className="section-title">Financial Literacy Quiz</h2>

      {quizSubmitted ? (
        <div>
          {quizQuestions.map((question, idx) => (
            <div key={idx} className="quiz-card">
              <p className="quiz-question">{idx + 1}. {question.question}</p>
              {question.options.map((opt, i) => {
                const isUserAnswer = quizAnswers[idx] === opt;
                const isCorrect = question.answer === opt;
                return (
                  <div
                    key={i}
                    className={`quiz-option-review ${isCorrect ? "correct" : ""} ${isUserAnswer && !isCorrect ? "wrong" : ""}`}
                  >
                    {opt} {isCorrect && "✔"} {isUserAnswer && !isCorrect && "✖"}
                  </div>
                );
              })}
            </div>
          ))}
          <p className="quiz-score">You scored: {quizScore}%</p>
          <p className="quiz-score">XP Earned: {xpEarned}</p>
        </div>
      ) : (
        <div className="quiz-card">
          <p className="quiz-question">{currentQuestion + 1}. {q.question}</p>
          {q.options.map((opt, i) => (
            <label key={i} className={`quiz-option ${quizAnswers[currentQuestion] === opt ? "selected" : ""}`}>
              <input
                type="radio"
                name={`q${currentQuestion}`}
                value={opt}
                checked={quizAnswers[currentQuestion] === opt}
                onChange={() => handleAnswerChange(opt)}
              />
              {opt}
            </label>
          ))}

          <div className="quiz-nav">
            <button
              type="button"
              disabled={currentQuestion === 0}
              onClick={() => setCurrentQuestion(prev => prev - 1)}
              className="nav-btn"
            >
              Previous
            </button>
            {currentQuestion < quizQuestions.length - 1 ? (
              <button
                type="button"
                onClick={() => setCurrentQuestion(prev => prev + 1)}
                className="nav-btn"
              >
                Next
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmitQuiz}
                className="nav-btn submit"
              >
                Submit Quiz
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};


  const renderBackButton = () => (
    <button 
      onClick={() => setSection("menu")} 
      style={{ 
        marginBottom: "1rem", 
        padding: "0.5rem 1rem", 
        borderRadius: "8px", 
        border: "none", 
        background: "#1976d2", 
        color: "white", 
        fontWeight: "bold",
        cursor: "pointer",
        transition: "background 0.3s, transform 0.2s"
      }}
      onMouseEnter={e => e.currentTarget.style.background = "#115293"}
      onMouseLeave={e => e.currentTarget.style.background = "#1976d2"}
    >
      ⬅ Back
    </button>
  );

  const renderSection = () => {
    switch(section) {
      case "investments":
        return (
          <section>
            {renderBackButton()}
            <h2 className="section-title">Investments</h2>
            <p className="section-desc">Learn about different types of investments from safe to risky.</p>
            {renderCards(investments, true)}
          </section>
        );
      case "interest":
        return (
          <section>
            {renderBackButton()}
            <h2 className="section-title">Interest Rates</h2>
            <p className="section-desc">Understand interest, simple interest, compound interest, and compounding periods.</p>
            {renderCards(interestConcepts)}
          </section>
        );
      case "quiz":
        return <section>{renderQuiz()}</section>;
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
        .card-level { background: rgba(255,255,255,0.2); padding: 0.25rem 0.5rem; border-radius: 12px; font-weight: bold; font-size: 0.8rem; display: inline-block; margin-bottom: 0.5rem; }
        .card-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 0.5rem; color: black; }
        .card-desc { font-size: 0.9rem; margin-bottom: 0.5rem; color: black; }
        .card-return { font-size: 0.9rem; margin-bottom: 0.5rem; color: black; }
        .card-example { background: rgba(255,255,255,0.15); padding: 0.5rem; border-radius: 12px; font-size: 0.8rem; color: black; margin-bottom: 0.25rem; }
        .gradient-green { background: linear-gradient(135deg, #4facfe, #00f2fe); }
        .gradient-blue { background: linear-gradient(135deg, #3a7bd5, #00d2ff); }
        .gradient-amber { background: linear-gradient(135deg, #f7971e, #ffd200); }
        .gradient-purple { background: linear-gradient(135deg, #7b2ff7, #f107a3); }
        .gradient-orange { background: linear-gradient(135deg, #f953c6, #b91d73); }
        .gradient-red { background: linear-gradient(135deg, #ff416c, #ff4b2b); }
        .quiz-card {background: linear-gradient(135deg, #4facfe, #00f2fe); padding: 1.5rem; border-radius: 16px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .quiz-card:hover {transform: translateY(-5px); }
        .quiz-question {font-weight: 700; font-size: 1.1rem; margin-bottom: 1rem; }
        .quiz-option {display: block; margin-bottom: 0.5rem; padding: 0.5rem 1rem; border-radius: 12px; background: rgba(255,255,255,0.15); cursor: pointer; transition: background 0.3s; }
        .quiz-option.selected {background: rgba(255,255,255,0.3); }
        .quiz-option input {margin-right: 0.5rem; }
        .quiz-nav {margin-top: 1rem; display: flex; gap: 1rem; }
        .nav-btn {padding: 0.5rem 1.5rem; border-radius: 8px; border: none; background: #1976d2; color: white; font-weight: bold; cursor: pointer; transition: background 0.3s; }
        .nav-btn:hover:not(:disabled) {background: #115293; }
        .nav-btn:disabled {opacity: 0.5; cursor: not-allowed; }
        .nav-btn.submit {background: #4caf50; }
        .nav-btn.submit:hover {background: #388e3c; }
        .quiz-option-review {padding: 0.5rem 1rem; border-radius: 12px; margin-bottom: 0.25rem; }
        .quiz-option-review.correct {background: #4caf50; color: white; }
        .quiz-option-review.wrong {background: #f44336; color: white; }
        .quiz-score {font-size: 1.2rem; font-weight: bold; margin-top: 1rem; }
      `}</style>

      <header className="header" style={{ textAlign: "center", marginBottom: "4rem" }}>
        <div className="logo" style={{ display: "inline-block", width: "60px", height: "60px", background: "linear-gradient(135deg, #4facfe, #00f2fe)", borderRadius: "16px", color: "white", fontWeight: "bold", fontSize: "2rem", lineHeight: "60px", marginBottom: "1rem" }}>R</div>
        <h1 className="title" style={{ fontSize: "3rem", fontWeight: 900 }}>Financial Literacy Hub</h1>
        <p className="subtitle" style={{ fontSize: "1.2rem", color: "#555", maxWidth: "800px", margin: "0 auto" }}>
          Master your finances with practical South African examples, from safe savings to bold investments, all explained in Rands you can relate to.
        </p>
      </header>

      {renderSection()}
    </div>
  );
};

export default Literacy;
