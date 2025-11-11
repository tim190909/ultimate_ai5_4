def predict_investment_risk(price, trend):
    if trend > 0.1:
        return "Achat recommandé 📈"
    elif trend < -0.1:
        return "Vente conseillée 📉"
    return "Stable ⚖️
