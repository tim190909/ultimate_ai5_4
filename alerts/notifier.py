from futbin.scraper import fetch_popular_players, is_future_upgrade
from analysis.scorer import compute_score, predict_price_multi_model
from sbc.optimizer import optimize_sbc

async def check_sbc_alerts(channel):
    alerts = []
    players = await fetch_popular_players("ps")
    for p in players[:5]:
        future_upgrade = await is_future_upgrade(p["id"])
        prices = [10000, 10500, 10750] # Exemples, remplacer par DB
        score_data = compute_score(prices, future_upgrade=future_upgrade)
        predicted_price = predict_price_multi_model(prices)
        if predicted_price > 15000 and score_data["score"] > 0:
            sbc_opt = await optimize_sbc(p["name"])
            alerts.append(
                f"⚡ {p['name']} ({p['platform']}) - Score: {score_data['score']:.2f}\n"
                f"Prix prévisionnel: {int(predicted_price)}\n"
                f"Solution SBC optimale actuelle:\n{sbc_opt}"
            )
    return alerts