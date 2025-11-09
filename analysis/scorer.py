from .ml_predict import predict_price_ml
FUT_TAX_RATE = 0.05

def compute_score(prices, fut_tax=FUT_TAX_RATE, popularity=1.0, future_upgrade=False):
    if len(prices) < 7: return None
    current_price = prices[-1]
    avg_7 = sum(prices[-7:])/7
    avg_14 = sum(prices[-14:])/14 if len(prices)>=14 else avg_7
    avg_30 = sum(prices[-30:])/30 if len(prices)>=30 else avg_14
    net_price = current_price * (1 - fut_tax)
    score = (avg_7*0.4 + avg_14*0.3 + avg_30*0.2) - net_price
    score *= popularity
    if future_upgrade: score *= 1.25
    volatility = (max(prices)-min(prices))/avg_30*100
    if volatility < 5: risk="Faible ✅"
    elif volatility < 10: risk="Moyen ⚠️"
    else: risk="Élevé 🔴"
    return {
        "score": score,
        "risk": risk,
        "net_price": net_price,
        "current_price": current_price,
        "volatility": volatility,
        "future_upgrade": future_upgrade
    }

def predict_price_multi_model(prices):
    if len(prices) < 3: return prices[-1] if prices else 0
    return max(int(predict_price_ml(prices)), 0)