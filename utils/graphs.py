import io
import matplotlib.pyplot as plt
from discord import File

def plot_prices_interactive(prices):
    plt.figure(figsize=(4,2))
    plt.plot(prices[-30:], label="30j", color="blue")
    if len(prices)>=14: plt.plot(prices[-14:], label="14j", color="orange")
    plt.plot(prices[-7:], label="7j", color="green")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

def export_portfolio_pdf(user_id, data):
    return f"PDF export for {user_id} with {len(data)} entries."

def export_portfolio_excel(user_id, data):
    return f"Excel export for {user_id} with {len(data)} entries."