import numpy as np
from sklearn.ensemble import RandomForestRegressor

def predict_price_ml(prices):
    x = np.arange(len(prices)).reshape(-1,1)
    y = np.array(prices)
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(x, y)
    pred = model.predict(np.array([[len(prices)]]))[0]
    return pred