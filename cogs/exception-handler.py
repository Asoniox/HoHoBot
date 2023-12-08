import discord
from discord.ext import commands

class ExceptionHandler(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error) -> None:
            if isinstance(error, commands.CommandNotFound):
                embed = discord.Embed(title="Error!", description=error, color=0xb40000)
                await ctx.channel.send(embed=embed, delete_after=10)

        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExceptionHandler(bot))