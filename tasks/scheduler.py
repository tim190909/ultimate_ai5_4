import asyncio
from alerts.notifier import check_sbc_alerts

def start_tasks(bot):
    asyncio.create_task(check_sbc_alerts_task(bot))

async def check_sbc_alerts_task(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            channel = next((ch for ch in guild.text_channels if ch.name=="trading-alerts"), None)
            if channel:
                messages = await check_sbc_alerts(channel)
                for msg in messages:
                    await channel.send(msg)
        await asyncio.sleep(900) # toutes les 15 minutes
	
