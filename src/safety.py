class SafetyResult:
    def __init__(self, blocked: bool, message: str):
        self.blocked = blocked
        self.message = message


def check(query: str):
    """Check if query violates financial regulations"""
    if not query or not query.strip():
        return SafetyResult(False, "Safe")
    
    q = query.lower().strip()
    
    # Request patterns that indicate intent to commit fraud
    is_request = any(w in q for w in [
        "help me", "show me", "can i", "should i", "how to", "how do i", 
        "ways to", "tips for", "tell me", "let me", "want to", "i need", 
        "design", "draft", "trade on", "get me", "find me", "give me",
        "what's the best", "best way", "without", "without reporting",
        "i work at", "my friend", "i know about", "gave me", "know the"
    ])
    
    # INSIDER TRADING - block requests for insider info/tips
    insider_patterns = [
        "insider tip", "give me a tip", "tip about earnings", "tip about acquisition",
        "load up before", "before earnings", "before announcement", "non-public info",
        "confidential info", "unannounced", "know the earnings", "earnings before",
        "material non-public", "inside information", "know about an unannounced",
        "confidential merger", "merger news", "gave me a tip"
    ]
    if any(w in q for w in insider_patterns):
        if is_request or any(w in q for w in ["my friend", "told me", "someone told me", "gave me", "at microsoft", "at apple"]):
            return SafetyResult(True, "Blocked: Insider trading")
    
    # MARKET MANIPULATION - block requests to manipulate markets
    manip_patterns = [
        "pump and dump", "pump up", "pump the price", "coordinated buying",
        "move the price", "drive up price", "wash trade", "spoofing", "layering",
        "coordinate with", "signal to buy", "fake volume", "buying scheme"
    ]
    if any(w in q for w in manip_patterns):
        if is_request:
            return SafetyResult(True, "Blocked: Market manipulation")
    
    # MONEY LAUNDERING - block requests to hide money/profits
    launder_patterns = [
        "hide money", "hide profits", "hide trading", "hide from tax",
        "without reporting", "structure deposits", "avoid reporting",
        "avoid the 10k", "move cash", "move 500k", "move money",
        "layer trades", "layer deposits", "obscure the source", "offshore",
        "clean the money", "launder", "shell account", "through stock trading"
    ]
    if any(w in q for w in launder_patterns):
        if is_request or "how" in q:
            return SafetyResult(True, "Blocked: Money laundering")
    
    # GUARANTEED RETURNS - block claims/requests for guaranteed returns
    # (but allow educational questions like "why are guaranteed returns bad")
    return_patterns = [
        "guaranteed returns", "guaranteed profit", "100% certain", "double your money",
        "double in a year", "foolproof", "risk-free", "promise", "50% return",
        "30% return", "guaranteed to go up", "guaranteed profit", "promise you'll make",
        "guarantee me"
    ]
    is_educational = any(w in q for w in [
        "why", "explain", "legitimate", "what is", "what are", "difference",
        "penalties", "investigate", "rules", "disclosure", "illegal", "crime"
    ])
    if any(w in q for w in return_patterns):
        if not is_educational:
            return SafetyResult(True, "Blocked: Guaranteed returns")
    
    # RECKLESS ADVICE - block requests to use critical funds
    reckless_patterns = [
        "all my savings", "my savings", "mortgage my house", "emergency fund",
        "margin loan", "margin trading", "entire retirement", "retirement savings",
        "put everything", "bet everything", "sell everything"
    ]
    if any(w in q for w in reckless_patterns):
        if is_request or any(w in q for w in ["should i", "tell me to", "which stock"]):
            return SafetyResult(True, "Blocked: Reckless advice")
    
    # SANCTIONS/COMPLIANCE - block attempts to evade sanctions
    sanction_patterns = [
        "sanctions", "ofac", "russian company", "sanctioned entity",
        "sanctioned country", "without traced", "without being traced",
        "secret account", "bypass sanctions", "evade sanctions"
    ]
    if any(w in q for w in sanction_patterns):
        # Educational questions (what are sanctions) vs malicious (how to bypass)
        if is_request or "how to" in q or "can i" in q:
            # BUT: allow educational questions about compliance
            if any(e in q for e in ["what are", "what is", "rules", "brokerages", "screen", "compliance"]):
                pass  # Educational - allow
            else:
                return SafetyResult(True, "Blocked: Sanctions evasion")
    
    # FRAUD - block requests to create fraudulent documents
    fraud_patterns = [
        "fake contract", "draft a fake", "fraudulent", "fake note",
        "false statement", "forged", "fake proof", "fabricate"
    ]
    if any(w in q for w in fraud_patterns):
        if is_request:
            return SafetyResult(True, "Blocked: Fraud")
    
    # All other queries are safe
    return SafetyResult(False, "Safe")