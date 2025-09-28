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
      gradient: "sage-light",
    },
    {
      title: "Government Bonds (RSA Retail Bonds)",
      level: "Very Safe",
      return: "R100 - R300 per R5,000 yearly",
      desc: "Government bonds are loans you give to the South African government. They are very secure and pay periodic interest, but inflation can slightly reduce real returns. Suitable for conservative investors.",
      example: "R5,000 government bond at 6% = R300 yearly",
      gradient: "sage-medium",
    },
    {
      title: "Corporate Bonds & Unit Trusts",
      level: "Moderately Safe",
      return: "R150 - R400 per R5,000 yearly",
      desc: "Corporate bonds and unit trusts invest in companies. Returns are higher than government bonds but carry some company risk. They are generally stable, with moderate growth potential.",
      example: "Allan Gray unit trust: R5,000 could grow by R350+ annually",
      gradient: "sage-dark",
    },
    {
      title: "JSE Index Funds (Top 40)",
      level: "Moderate Risk",
      return: "R300 - R500 per R5,000 yearly",
      desc: "Index funds let you own pieces of South Africa's top 40 companies. They are diversified and reduce single-stock risk, providing solid historical growth over time.",
      example: "Satrix Top 40 ETF: R10,000 historically grows R800-1,200 per year",
      gradient: "sage-forest",
    },
    {
      title: "Individual JSE Stocks",
      level: "High Risk",
      return: "R0 - R2,500+ per R5,000 yearly",
      desc: "Buying individual stocks is high-risk, high-reward. Prices fluctuate based on market trends and company performance. Can lead to large gains or losses.",
      example: "Naspers stock: R5,000 could become R0 or R15,000+ in a year",
      gradient: "sage-warning",
    },
    {
      title: "Crypto (Bitcoin, Ethereum)",
      level: "Extreme Risk",
      return: "R0 - R25,000+ per R5,000 yearly",
      desc: "Cryptocurrencies are highly volatile digital assets. Prices can soar or crash quickly. Only invest money you can afford to lose, as potential gains and losses are extreme.",
      example: "R1,000 in Bitcoin could become R100 or R10,000 within months",
      gradient: "sage-alert",
    },
  ];

  const investmentMetrics = [
    {
      title: "Sharpe Ratio - Your 'Bang for Your Buck' Score",
      level: "Investment Efficiency",
      desc: "Think of the Sharpe ratio like an efficiency rating for your investments. It's like comparing cars by their miles per gallon - it tells you how much return you're getting for the risk you're taking.",
      examples: [
        "Simple Analogy: Imagine you're choosing between two roller coasters:",
        "• Roller Coaster A: Gives you 10 units of thrill but is very scary (high risk)",
        "• Roller Coaster B: Gives you 8 units of thrill but is only moderately scary (lower risk)",
        "Roller Coaster B has a better 'thrill-to-fear' ratio - that's essentially what Sharpe ratio measures for investments!"
      ],
      gradient: "sage-medium",
      scores: [
        { range: "🟢 Excellent Score (Above 1.0)", meaning: "You're getting great returns for the risk you're taking", example: "Like finding a high-paying job that's also low-stress", action: "Your portfolio is performing very well" },
        { range: "🟡 Okay Score (0.5 - 1.0)", meaning: "Decent returns, but you might be taking too much risk", example: "Like a job that pays well but is very stressful", action: "Consider adjusting your strategy" },
        { range: "🔴 Poor Score (Below 0.5)", meaning: "You're taking a lot of risk but not getting enough reward", example: "Like a stressful job that doesn't pay well", action: "Your strategy needs improvement" }
      ]
    },
    {
      title: "Sentiment Score - The 'Market Mood' Meter",
      level: "Market Psychology",
      desc: "Sentiment analysis is like taking the emotional temperature of the financial news. It reads thousands of news articles and social media posts to figure out whether people are feeling optimistic or pessimistic about a stock.",
      examples: [
        "Simple Analogy: Imagine you're trying to decide whether to go to a new restaurant. You read online reviews:",
        "• Lots of 5-star reviews saying 'Amazing food!' = Positive sentiment",
        "• Lots of 1-star reviews saying 'Terrible service!' = Negative sentiment",
        "• Mixed reviews = Neutral sentiment"
      ],
      gradient: "sage-forest",
      scores: [
        { range: "Super Positive (0.35 and above)", meaning: "Almost everyone is saying great things about this stock", example: "A restaurant with 95% five-star reviews", action: "STRONG BUY - People are very optimistic", color: "Bright Green" },
        { range: "Pretty Positive (0.15 to 0.34)", meaning: "Most people are saying good things", example: "A restaurant with mostly 4-star reviews", action: "BUY - Generally positive vibes", color: "Light Blue" },
        { range: "Neutral (-0.14 to 0.14)", meaning: "People are unsure or opinions are mixed", example: "A restaurant with mixed 3-star reviews", action: "HOLD - Wait and see what happens", color: "Yellow" },
        { range: "Pretty Negative (-0.15 to -0.34)", meaning: "Most people are concerned or pessimistic", example: "A restaurant with mostly 2-star reviews", action: "SELL - People are worried", color: "Orange" },
        { range: "Very Negative (-0.35 and below)", meaning: "Almost everyone is saying bad things", example: "A restaurant with mostly 1-star reviews", action: "STRONG SELL - People are very pessimistic", color: "Red" }
      ]
    },
    {
      title: "Why These Scores Matter",
      level: "Smart Investing",
      desc: "Using Sharpe Ratio and Sentiment Score together helps you make better investment decisions by combining performance data with market psychology.",
      examples: [
        "Sharpe Ratio: Helps you understand if you're being smart with your money. A higher score means you're getting good returns without taking unnecessary risks.",
        "Sentiment Score: Helps you understand what other people think. If everyone is excited about a stock (high positive sentiment), the price might go up. If everyone is worried (negative sentiment), the price might go down."
      ],
      gradient: "sage-dark",
      scenarios: [
        { situation: "Best scenario", description: "High Sharpe ratio (good performance) + Positive sentiment (people are optimistic) = Strong investment opportunity" },
        { situation: "Worst scenario", description: "Low Sharpe ratio (poor performance) + Negative sentiment (people are pessimistic) = Avoid this investment" },
        { situation: "Mixed signals", description: "Use caution and do more research" }
      ],
      summary: "Think of it like this: Sharpe ratio tells you how well the investment has been performing, while sentiment tells you how people currently feel about its future. Both pieces of information help you make better decisions!"
    }
  ];

  const interestConcepts = [
    {
      title: "What is Interest?",
      desc: "Interest is the cost of borrowing money or the reward for saving it. It is expressed as a percentage rate.",
      examples: [],
      gradient: "sage-light",
    },
    {
      title: "Simple Interest",
      desc: "Calculated only on the original principal amount. Formula: Simple Interest = Principal × Rate × Time.",
      examples: [
        "Loan Example: Borrow R10,000 at 10% per year for 3 years → Interest = R3,000",
        "Investment Example: Deposit R5,000 at 6% for 2 years → Interest = R600"
      ],
      gradient: "sage-medium"
    },
    {
      title: "Compound Interest",
      desc: "Calculated on the principal amount plus any accumulated interest. Formula: Compound Interest = Principal × (1 + Rate / Number of times interest applied per year)^(Number of times interest applied × Years) - Principal.",
      examples: [
        "Investment: R5,000 at 6% annually, compounded quarterly for 2 years → ≈ R636 interest",
        "Loan: R10,000 at 10% annually, compounded monthly for 3 years → ≈ R3,347 interest"
      ],
      gradient: "sage-dark"
    },
    {
      title: "Compounding Periods",
      desc: "How often interest is applied: annually, semi-annually, quarterly, monthly, daily. More frequent compounding increases total interest.",
      examples: [
        "Monthly vs annually: R5,000 at 6% compounded monthly earns more than annually",
        "Short-term loan compounded daily accumulates more interest than monthly"
      ],
      gradient: "sage-forest"
    }
  ];

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
    <div className="menu-section">
      <div className="menu-content">
        <h2 className="menu-title">Select a Financial Knowledge Section</h2>
        <div className="menu-buttons">
          <button className="menu-btn" onClick={() => setSection("investments")}>
            <div className="menu-btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"></polyline>
              </svg>
            </div>
            <div className="menu-btn-content">
              <div className="menu-btn-title">Investments</div>
              <div className="menu-btn-desc">Learn about different investment options</div>
            </div>
          </button>
          <button className="menu-btn" onClick={() => setSection("interest")}>
            <div className="menu-btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
                <line x1="1" y1="10" x2="23" y2="10"></line>
              </svg>
            </div>
            <div className="menu-btn-content">
              <div className="menu-btn-title">Interest</div>
              <div className="menu-btn-desc">Understand simple & compound interest</div>
            </div>
          </button>
          <button className="menu-btn" onClick={() => setSection("quiz")}>
            <div className="menu-btn-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="9,9h6v6h-6z"></path>
                <path d="M16.24 7.76l-2.12 2.12"></path>
              </svg>
            </div>
            <div className="menu-btn-content">
              <div className="menu-btn-title">Test Your Knowledge</div>
              <div className="menu-btn-desc">Quiz yourself on financial concepts</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  );

  const renderCards = (items, showReturn = false) => (
    <div className="cards-grid">
      {items.map((item, idx) => (
        <div key={idx} className={`concept-card gradient-${item.gradient}`}>
          {item.level && <div className="card-level">{item.level}</div>}
          <h4 className="card-title">{item.title}</h4>
          <p className="card-desc">{item.desc}</p>
          {showReturn && <div className="card-return">Typical return: {item.return}</div>}
          {item.example && <div className="card-example">{item.example}</div>}
          {item.examples && item.examples.map((ex, i) => (
            <div key={i} className="card-example">{ex}</div>
          ))}
          {item.scores && (
            <div className="score-section">
              <h5 className="score-title">How to Read the Scores:</h5>
              {item.scores.map((score, scoreIdx) => (
                <div key={scoreIdx} className="score-item">
                  <div className="score-range">{score.range}</div>
                  <div className="score-details">
                    <strong>What it means:</strong> {score.meaning}<br/>
                    <strong>Real-world example:</strong> {score.example}<br/>
                    <strong>Investment meaning:</strong> {score.action}
                    {score.color && <><br/><strong>Color:</strong> {score.color}</>}
                  </div>
                </div>
              ))}
            </div>
          )}
          {item.scenarios && (
            <div className="scenario-section">
              <h5 className="scenario-title">Using Them Together:</h5>
              {item.scenarios.map((scenario, scenarioIdx) => (
                <div key={scenarioIdx} className="scenario-item">
                  <strong>{scenario.situation}:</strong> {scenario.description}
                </div>
              ))}
            </div>
          )}
          {item.summary && (
            <div className="summary-section">
              <div className="card-example">{item.summary}</div>
            </div>
          )}
        </div>
      ))}
    </div>
  );

  const renderQuiz = () => {
    const q = quizQuestions[currentQuestion];

    return (
      <div>
        {renderBackButton()}
        <div className="quiz-section">
          <h2 className="section-title">Financial Literacy Quiz</h2>
          <p className="section-desc">Test your understanding of financial concepts</p>

          {quizSubmitted ? (
            <div className="quiz-results">
              <div className="results-summary">
                <div className="score-display">
                  <div className="score-number">{quizScore}%</div>
                  <div className="score-label">Your Score</div>
                </div>
                <div className="xp-display">
                  <div className="xp-number">{xpEarned} XP</div>
                  <div className="xp-label">Experience Points</div>
                </div>
              </div>

              <div className="questions-review">
                {quizQuestions.map((question, idx) => (
                  <div key={idx} className="review-card">
                    <p className="review-question">{idx + 1}. {question.question}</p>
                    <div className="review-options">
                      {question.options.map((opt, i) => {
                        const isUserAnswer = quizAnswers[idx] === opt;
                        const isCorrect = question.answer === opt;
                        return (
                          <div
                            key={i}
                            className={`review-option ${
                              isCorrect ? "correct" : ""
                            } ${isUserAnswer && !isCorrect ? "wrong" : ""}`}
                          >
                            <span>{opt}</span>
                            {isCorrect && <span className="check-mark">✓</span>}
                            {isUserAnswer && !isCorrect && <span className="x-mark">✗</span>}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="quiz-card">
              <div className="quiz-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill" 
                    style={{ width: `${((currentQuestion + 1) / quizQuestions.length) * 100}%` }}
                  ></div>
                </div>
                <span className="progress-text">
                  Question {currentQuestion + 1} of {quizQuestions.length}
                </span>
              </div>

              <div className="question-content">
                <h3 className="quiz-question">{q.question}</h3>
                <div className="quiz-options">
                  {q.options.map((opt, i) => (
                    <label key={i} className={`quiz-option ${quizAnswers[currentQuestion] === opt ? "selected" : ""}`}>
                      <input
                        type="radio"
                        name={`q${currentQuestion}`}
                        value={opt}
                        checked={quizAnswers[currentQuestion] === opt}
                        onChange={() => handleAnswerChange(opt)}
                      />
                      <span className="option-text">{opt}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div className="quiz-navigation">
                <button
                  type="button"
                  disabled={currentQuestion === 0}
                  onClick={() => setCurrentQuestion(prev => prev - 1)}
                  className="nav-btn nav-btn-secondary"
                >
                  Previous
                </button>
                {currentQuestion < quizQuestions.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => setCurrentQuestion(prev => prev + 1)}
                    className="nav-btn nav-btn-primary"
                  >
                    Next
                  </button>
                ) : (
                  <button
                    type="button"
                    onClick={handleSubmitQuiz}
                    className="nav-btn nav-btn-submit"
                  >
                    Submit Quiz
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderBackButton = () => (
    <button 
      onClick={() => setSection("menu")} 
      className="back-button"
    >
      ← Back to Menu
    </button>
  );

  const renderSection = () => {
    switch(section) {
      case "investments":
        return (
          <section>
            {renderBackButton()}
            <div className="content-section">
              <h2 className="section-title">Investment Types</h2>
              <p className="section-desc">Learn about different types of investments from safe to risky, with South African examples.</p>
              {renderCards(investments, true)}
              
              <div className="metrics-section">
                <h2 className="section-title">Investment Metrics</h2>
                <p className="section-desc">Understand key metrics that help you evaluate investment performance and market sentiment.</p>
                {renderCards(investmentMetrics)}
              </div>
            </div>
          </section>
        );
      case "interest":
        return (
          <section>
            {renderBackButton()}
            <div className="content-section">
              <h2 className="section-title">Interest Concepts</h2>
              <p className="section-desc">Understand interest, simple interest, compound interest, and compounding periods.</p>
              {renderCards(interestConcepts)}
            </div>
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
        .literacy-container {
          min-height: 100vh;
          background: linear-gradient(135deg, 
            rgba(248, 250, 248, 1) 0%, 
            rgba(242, 247, 242, 1) 25%,
            rgba(235, 243, 235, 1) 50%,
            rgba(242, 247, 242, 1) 75%,
            rgba(248, 250, 248, 1) 100%
          );
          padding: 6rem 2rem 2rem;
          font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
          color: #1e293b;
        }
        
        .content-wrapper {
          max-width: 1000px;
          margin: 0 auto;
        }
        
        .header-section {
          text-align: center;
          margin-bottom: 4rem;
          position: relative;
        }
        
        .header-decoration {
          position: absolute;
          top: -20px;
          left: 50%;
          transform: translateX(-50%);
          width: 120px;
          height: 4px;
          background: linear-gradient(90deg, #8fae6d, #7a9b5b);
          border-radius: 2px;
        }
        
        .main-logo {
          display: inline-block;
          width: 80px;
          height: 80px;
          background: linear-gradient(135deg, #8fae6d, #7a9b5b);
          border-radius: 20px;
          color: white;
          font-weight: 800;
          font-size: 2.5rem;
          line-height: 80px;
          margin-bottom: 1.5rem;
          box-shadow: 0 8px 24px rgba(143, 174, 109, 0.3);
        }
        
        .main-title {
          font-size: 3.5rem;
          font-weight: 800;
          margin-bottom: 1rem;
          background: linear-gradient(135deg, #1e293b 0%, #475569 50%, #7a9b5b 100%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          line-height: 1.1;
        }
        
        .main-subtitle {
          font-size: 1.25rem;
          color: #64748b;
          font-weight: 400;
          max-width: 700px;
          margin: 0 auto;
          line-height: 1.6;
        }
        
        .menu-section {
          display: flex;
          justify-content: center;
          padding: 2rem 0;
        }
        
        .menu-content {
          width: 100%;
          max-width: 800px;
        }
        
        .menu-title {
          text-align: center;
          font-size: 2rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 3rem;
        }
        
        .menu-buttons {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        .menu-btn {
          display: flex;
          align-items: center;
          gap: 1.5rem;
          padding: 2rem;
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 250, 248, 0.9) 100%
          );
          border: 2px solid rgba(143, 174, 109, 0.2);
          border-radius: 20px;
          cursor: pointer;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          backdrop-filter: blur(20px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        }
        
        .menu-btn:hover {
          transform: translateY(-4px);
          border-color: #8fae6d;
          box-shadow: 0 16px 32px rgba(143, 174, 109, 0.15);
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 1) 0%, 
            rgba(248, 250, 248, 1) 100%
          );
        }
        
        .menu-btn-icon {
          width: 80px;
          height: 80px;
          background: linear-gradient(135deg, #8fae6d, #7a9b5b);
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          color: white;
        }
        
        .menu-btn-icon svg {
          width: 40px;
          height: 40px;
          stroke-width: 2.5;
        }
        
        .menu-btn-content {
          flex: 1;
          text-align: left;
        }
        
        .menu-btn-title {
          font-size: 1.5rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 0.5rem;
        }
        
        .menu-btn-desc {
          color: #64748b;
          font-size: 1rem;
          line-height: 1.4;
        }
        
        .back-button {
          padding: 0.75rem 1.5rem;
          border-radius: 12px;
          border: 2px solid rgba(143, 174, 109, 0.3);
          background: rgba(248, 250, 248, 0.9);
          color: #7a9b5b;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          margin-bottom: 2rem;
          backdrop-filter: blur(10px);
        }
        
        .back-button:hover {
          background: rgba(143, 174, 109, 0.1);
          border-color: #8fae6d;
          transform: translateY(-2px);
        }
        
        .content-section {
          margin-top: 2rem;
        }
        
        .metrics-section {
          margin-top: 4rem;
          padding-top: 3rem;
          border-top: 2px solid rgba(143, 174, 109, 0.2);
        }
        
        .section-title {
          font-size: 2.5rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1rem;
          text-align: center;
        }
        
        .section-desc {
          font-size: 1.1rem;
          color: #64748b;
          text-align: center;
          max-width: 600px;
          margin: 0 auto 3rem;
          line-height: 1.6;
        }
        
        .cards-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
          gap: 2rem;
          margin-top: 2rem;
        }
        
        .concept-card {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 250, 248, 0.9) 100%
          );
          border: 2px solid rgba(143, 174, 109, 0.15);
          border-radius: 20px;
          padding: 2rem;
          backdrop-filter: blur(15px);
          box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          position: relative;
          overflow: hidden;
        }
        
        .concept-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 4px;
          background: var(--card-gradient);
          border-radius: 20px 20px 0 0;
        }
        
        .concept-card:hover {
          transform: translateY(-6px);
          box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
          border-color: rgba(143, 174, 109, 0.3);
        }
        
        .gradient-sage-light {
          --card-gradient: linear-gradient(135deg, #a7c085, #8fae6d);
        }
        
        .gradient-sage-medium {
          --card-gradient: linear-gradient(135deg, #8fae6d, #7a9b5b);
        }
        
        .gradient-sage-dark {
          --card-gradient: linear-gradient(135deg, #7a9b5b, #658749);
        }
        
        .gradient-sage-forest {
          --card-gradient: linear-gradient(135deg, #658749, #507338);
        }
        
        .gradient-sage-warning {
          --card-gradient: linear-gradient(135deg, #d97706, #b45309);
        }
        
        .gradient-sage-alert {
          --card-gradient: linear-gradient(135deg, #dc2626, #b91c1c);
        }
        
        .card-level {
          display: inline-block;
          background: rgba(143, 174, 109, 0.15);
          color: #7a9b5b;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-weight: 600;
          font-size: 0.85rem;
          margin-bottom: 1rem;
          border: 1px solid rgba(143, 174, 109, 0.3);
        }
        
        .card-title {
          font-size: 1.4rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1rem;
          line-height: 1.3;
        }
        
        .card-desc {
          color: #475569;
          line-height: 1.6;
          margin-bottom: 1rem;
          font-size: 1rem;
        }
        
        .card-return {
          background: rgba(143, 174, 109, 0.1);
          color: #7a9b5b;
          padding: 0.75rem 1rem;
          border-radius: 12px;
          font-weight: 600;
          margin-bottom: 1rem;
          border: 1px solid rgba(143, 174, 109, 0.2);
        }
        
        .card-example {
          background: rgba(248, 250, 248, 0.8);
          border: 1px solid rgba(143, 174, 109, 0.2);
          padding: 1rem;
          border-radius: 12px;
          color: #475569;
          font-size: 0.95rem;
          line-height: 1.5;
          margin-bottom: 0.75rem;
        }
        
        .card-example:last-child {
          margin-bottom: 0;
        }
        
        .score-section {
          margin-top: 1.5rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(143, 174, 109, 0.2);
        }
        
        .score-title {
          font-size: 1.1rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1rem;
        }
        
        .score-item {
          background: rgba(248, 250, 248, 0.8);
          border: 1px solid rgba(143, 174, 109, 0.2);
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 1rem;
        }
        
        .score-range {
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 0.5rem;
          font-size: 1rem;
        }
        
        .score-details {
          color: #475569;
          font-size: 0.9rem;
          line-height: 1.5;
        }
        
        .scenario-section {
          margin-top: 1.5rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(143, 174, 109, 0.2);
        }
        
        .scenario-title {
          font-size: 1.1rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 1rem;
        }
        
        .scenario-item {
          background: rgba(248, 250, 248, 0.8);
          border: 1px solid rgba(143, 174, 109, 0.2);
          padding: 1rem;
          border-radius: 8px;
          margin-bottom: 0.75rem;
          color: #475569;
          line-height: 1.5;
        }
        
        .summary-section {
          margin-top: 1.5rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(143, 174, 109, 0.2);
        }
        
        .quiz-section {
          max-width: 800px;
          margin: 0 auto;
        }
        
        .quiz-card {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 250, 248, 0.9) 100%
          );
          border: 2px solid rgba(143, 174, 109, 0.2);
          border-radius: 20px;
          padding: 2.5rem;
          backdrop-filter: blur(20px);
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
          margin-bottom: 2rem;
        }
        
        .quiz-progress {
          margin-bottom: 2rem;
        }
        
        .progress-bar {
          width: 100%;
          height: 8px;
          background: rgba(143, 174, 109, 0.2);
          border-radius: 4px;
          overflow: hidden;
          margin-bottom: 0.5rem;
        }
        
        .progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #8fae6d, #7a9b5b);
          border-radius: 4px;
          transition: width 0.3s ease;
        }
        
        .progress-text {
          color: #64748b;
          font-size: 0.9rem;
          font-weight: 500;
        }
        
        .quiz-question {
          font-size: 1.3rem;
          font-weight: 700;
          color: #1e293b;
          margin-bottom: 2rem;
          line-height: 1.4;
        }
        
        .quiz-options {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        
        .quiz-option {
          display: flex;
          align-items: center;
          padding: 1rem 1.25rem;
          border: 2px solid rgba(143, 174, 109, 0.2);
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.3s ease;
          background: rgba(248, 250, 248, 0.5);
        }
        
        .quiz-option:hover {
          border-color: #8fae6d;
          background: rgba(143, 174, 109, 0.05);
          transform: translateY(-1px);
        }
        
        .quiz-option.selected {
          border-color: #7a9b5b;
          background: rgba(143, 174, 109, 0.15);
        }
        
        .quiz-option input {
          margin-right: 1rem;
          width: 18px;
          height: 18px;
          accent-color: #7a9b5b;
        }
        
        .option-text {
          flex: 1;
          font-weight: 500;
          color: #1e293b;
        }
        
        .quiz-navigation {
          display: flex;
          gap: 1rem;
          justify-content: space-between;
        }
        
        .nav-btn {
          padding: 0.75rem 2rem;
          border-radius: 12px;
          border: none;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          font-size: 1rem;
        }
        
        .nav-btn-primary {
          background: linear-gradient(135deg, #8fae6d, #7a9b5b);
          color: white;
          box-shadow: 0 4px 12px rgba(143, 174, 109, 0.3);
        }
        
        .nav-btn-primary:hover {
          background: linear-gradient(135deg, #7a9b5b, #658749);
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(143, 174, 109, 0.4);
        }
        
        .nav-btn-secondary {
          background: rgba(248, 250, 248, 0.8);
          color: #7a9b5b;
          border: 2px solid rgba(143, 174, 109, 0.3);
        }
        
        .nav-btn-secondary:hover {
          background: rgba(143, 174, 109, 0.1);
          border-color: #8fae6d;
        }
        
        .nav-btn-submit {
          background: linear-gradient(135deg, #7a9b5b, #658749);
          color: white;
          box-shadow: 0 4px 12px rgba(122, 155, 91, 0.4);
        }
        
        .nav-btn-submit:hover {
          background: linear-gradient(135deg, #658749, #507338);
          transform: translateY(-2px);
        }
        
        .nav-btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
          transform: none;
        }
        
        .quiz-results {
          margin-top: 2rem;
        }
        
        .results-summary {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 2rem;
          margin-bottom: 3rem;
        }
        
        .score-display, .xp-display {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.9) 0%, 
            rgba(248, 250, 248, 0.8) 100%
          );
          border: 2px solid rgba(143, 174, 109, 0.2);
          border-radius: 16px;
          padding: 2rem;
          text-align: center;
          backdrop-filter: blur(10px);
          box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05);
        }
        
        .score-number, .xp-number {
          font-size: 3rem;
          font-weight: 800;
          background: linear-gradient(135deg, #7a9b5b, #658749);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          margin-bottom: 0.5rem;
        }
        
        .score-label, .xp-label {
          color: #64748b;
          font-weight: 600;
          font-size: 1.1rem;
        }
        
        .questions-review {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        
        .review-card {
          background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.95) 0%, 
            rgba(248, 250, 248, 0.9) 100%
          );
          border: 2px solid rgba(143, 174, 109, 0.15);
          border-radius: 16px;
          padding: 2rem;
          backdrop-filter: blur(10px);
          box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
        }
        
        .review-question {
          font-size: 1.1rem;
          font-weight: 600;
          color: #1e293b;
          margin-bottom: 1rem;
          line-height: 1.4;
        }
        
        .review-options {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        
        .review-option {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          border-radius: 8px;
          font-weight: 500;
          transition: all 0.3s ease;
        }
        
        .review-option.correct {
          background: rgba(34, 197, 94, 0.15);
          color: #15803d;
          border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        .review-option.wrong {
          background: rgba(239, 68, 68, 0.15);
          color: #dc2626;
          border: 1px solid rgba(239, 68, 68, 0.3);
        }
        
        .check-mark {
          color: #15803d;
          font-weight: 700;
          font-size: 1.2rem;
        }
        
        .x-mark {
          color: #dc2626;
          font-weight: 700;
          font-size: 1.2rem;
        }
        
        @media (max-width: 768px) {
          .literacy-container {
            padding: 4rem 1rem 1rem;
          }
          
          .main-title {
            font-size: 2.5rem;
          }
          
          .main-subtitle {
            font-size: 1.1rem;
          }
          
          .menu-btn {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
            padding: 1.5rem;
          }
          
          .menu-btn-content {
            text-align: center;
          }
          
          .cards-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
          }
          
          .concept-card {
            padding: 1.5rem;
          }
          
          .quiz-card {
            padding: 1.5rem;
          }
          
          .quiz-navigation {
            flex-direction: column;
            gap: 1rem;
          }
          
          .nav-btn {
            width: 100%;
          }
          
          .results-summary {
            grid-template-columns: 1fr;
            gap: 1rem;
          }
        }
      `}</style>

      <div className="content-wrapper">
        <header className="header-section">
          <div className="header-decoration"></div>
          {/*<div className="main-logo">R</div>*/}
          <h1 className="main-title">Financial Education Center</h1>
          <p className="main-subtitle">
            Master your finances with practical South African examples, from safe savings to bold investments. 
            Build your financial knowledge with interactive lessons and quizzes.
          </p>
        </header>

        {renderSection()}
      </div>
    </div>
  );
};

export default Literacy;