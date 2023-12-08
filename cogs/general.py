import discord
import datetime
import time
import asyncio


from discord import app_commands
from discord.ext import commands
import datetime

from discord.app_commands import AppCommandError, Choice


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    #PING COMMAND
    @app_commands.command(name="ping", description="Shows the latency of the bot!")
    @app_commands.checks.cooldown(1, 10)
    async def ping(self, interaction: discord.Interaction):
        start = time.perf_counter()
        embed = discord.Embed(title="Ping/Latency", description='', color=0x38B6FF)
        response = 'Response: {0}ms'.format(round(self.bot.latency, 3))

        #INITIAL EMBED
        embed.add_field(name='', value=response, inline=False)
        embed.add_field(name='', value='Round Trip: Calculating...', inline=False)
        await interaction.response.send_message(embed=embed)
        end = time.perf_counter()
        duration = (end - start) * 1000

        #FINAL EMBED
        embed = discord.Embed(title="Ping/Latency", description='', color=0x38B6FF)
        embed.add_field(name='', value=response, inline=False)
        embed.add_field(name='', value='Round Trip: {0}ms'.format(round(duration, 0)), inline=False)
        await asyncio.sleep(0.5)
        await interaction.edit_original_response(embed=embed)


    @ping.error
    async def ping_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(General(bot))