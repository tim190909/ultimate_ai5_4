import matplotlib.pyplot as plt
import io
import discord

async def create_price_graph(prices):
    plt.plot(prices)
    plt.title("Évolution du prix")
    plt.xlabel("Temps")
    plt.ylabel("Prix")
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return discord.File(buf, filename="graph.png")
