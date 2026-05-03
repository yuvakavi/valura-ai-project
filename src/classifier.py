import re

class Result:
    def __init__(self, agent, entities):
        self.agent = agent
        self.entities = entities


def extract_tickers(query: str):
    """Extract uppercase stock tickers (AAPL, TSLA, etc)"""
    return re.findall(r'\b[A-Z]{1,5}\b', query)


def classify(query: str, llm=None):
    """Classify user query to appropriate financial agent"""
    q = query.lower().strip()
    
    # ===== EDUCATIONAL QUERIES (general knowledge) =====
    # Pattern: starts with "what", "explain", "why", "define" about generic topics
    educational_markers = ["what is", "what's the", "what are", "explain", "why", "how do", "define", "describe"]
    generic_topics = ["mutual fund", "etf", "index fund", "compound interest", "p/e", "ratio"]
    
    is_educational_question = (
        any(marker in q for marker in educational_markers) and 
        any(topic in q for topic in generic_topics)
    )
    
    if is_educational_question:
        return Result("general_query", {})
    
    # ===== CUSTOMER SUPPORT =====
    if any(w in q for w in ["password", "log in", "reset", "account", "can't access"]):
        return Result("customer_support", {})
    
    # ===== FINANCIAL PLANNING =====
    if any(w in q for w in ["retire", "retirement", "college", "education", "long term", "future goal"]):
        return Result("financial_planning", {})
    
    # ===== INVESTMENT STRATEGY - Actions on portfolio (buy/sell/rebalance) =====
    if any(w in q for w in [
        "should i buy", "should i sell", "should i invest",
        "buy more", "sell my", "rebalance", "when to buy", "when to sell",
        "diversify", "allocation", "invest in"
    ]):
        return Result("investment_strategy", {})
    
    # ===== PORTFOLIO HEALTH - Structured portfolio analysis =====
    if any(w in q for w in [
        "portfolio", "health check", "review my", "am i beating", "concentration",
        "my holdings", "portfolio summary"
    ]):
        return Result("portfolio_health", {})
    
    # ===== RISK ASSESSMENT - Risk metrics and analysis =====
    if any(w in q for w in ["var", "risk", "exposure", "downside", "volatility", "correlation"]):
        return Result("risk_assessment", {})
    
    # ===== PREDICTIVE ANALYSIS =====
    if any(w in q for w in ["crash", "recession", "forecast", "predict", "trend", "bull", "bear"]):
        return Result("predictive_analysis", {})
    
    # ===== PRODUCT RECOMMENDATION =====
    if any(w in q for w in [
        "recommend", "suggest", "good fund", "best fund", "best etf",
        "which etf", "which fund", "index fund", "bond fund", "fund option"
    ]):
        return Result("product_recommendation", {})
    
    # ===== FINANCIAL CALCULATOR - Deterministic calculations =====
    if any(w in q for w in [
        "calculate", "mortgage", "dca", "dollar-cost", "tax", "interest",
        "compound", "how much", "payment", "future value", "roi", "return"
    ]):
        return Result("financial_calculator", {})
    
    # ===== MARKET RESEARCH - Factual info about instruments/sectors/news =====
    if any(w in q for w in [
        "price", "news", "stock", "performance", "tell me about",
        "microsoft", "apple", "nvidia", "tesla", "asml", "amazon",
        "company", "sector", "happening"
    ]):
        tickers = extract_tickers(query)
        return Result("market_research", {"tickers": tickers})
    
    # ===== DEFAULT: GENERAL QUERY (educational, conversational) =====
    return Result("general_query", {})
