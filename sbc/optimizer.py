def optimize_sbc(players):
    best_team = sorted(players, key=lambda x: x["rating"], reverse=True)[:11]
    return best_team
