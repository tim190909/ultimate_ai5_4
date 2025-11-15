import random

# Simule une IA qui prédit les prix FUT
# Peut être remplacée par un vrai modèle ML plus tard

async def predict_player_price(player_id: int):
    """
    Simulation d’une prédiction IA.
    Retournera une estimation réaliste basée sur une logique aléatoire.
    """
    try:
        base = random.randint(20000, 200000)
        variation = random.randint(-15000, 35000)
        return base + variation
    except Exception as e:
        print(f"❌ Erreur predict_player_price: {e}")
        return None
