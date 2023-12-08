import discord
import random
import aiohttp
import platform
import time
import json

from discord import app_commands
from discord.ext import commands
from discord.app_commands import AppCommandError
from re import search
from datetime import timedelta
from aiohttp_client_cache import CacheBackend
from aiohttp_client_cache.session import CachedSession
from components import db

cache = CacheBackend(expire_after=timedelta(seconds=120))
exclamain = db.client.exclamain

#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.discord_version = discord.__version__
        self.platform = platform.python_version()
        self.user_agent = f"HoHoBot/1.0 (discord.py {self.discord_version}, Python {self.platform})"

    #COZY COMMAND
    @app_commands.command(name="cozy", description="The coziest of subreddits!")
    @app_commands.checks.cooldown(1, 5.0)
    async def cozy(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        subreddit = [
            "https://www.reddit.com/r/cozy/new.json?limit=100",
            "https://www.reddit.com/r/cozyplaces/new.json?limit=100",
        ]
        async with CachedSession(cache=cache) as session:
            async with session.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()
                while True:
                    counter = 0
                    random_post = res["data"]["children"][random.randint(0, 99)]
                    image_url = str(random_post["data"]["url"])
                    if search(".jpg|.jpeg|.png|.gif$", image_url):
                        break
                    else:
                        counter += 1
                        if counter == 100:
                            image_url = None
                            break

                permalink = random_post["data"]["permalink"]
                title = random_post["data"]["title"]
                subreddit_title = random_post["data"]["subreddit"]
                embed = discord.Embed(
                    title=f"{title}",
                    description="",
                    url=f"https://reddit.com{permalink}",
                    color=0x38B6FF,
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"By r/{subreddit_title}")
                await interaction.followup.send(embed=embed)

    @cozy.error
    async def cozy_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    

    #CHRISTMAS COMMAND
    @app_commands.command(name="christmas", description="Christmas reddit posts just for you!")
    @app_commands.checks.cooldown(1, 5.0)
    async def christmas(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        subreddit = [
            'https://www.reddit.com/r/christmas/new.json?limit=100',
            'https://www.reddit.com/r/Winter/new.json?limit=100'
        ]
        async with CachedSession(cache=cache) as session:
            async with session.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()
                while True:
                    counter = 0
                    random_post = res["data"]["children"][random.randint(0, 99)]
                    image_url = str(random_post["data"]["url"])
                    if search(".jpg|.jpeg|.png|.gif$", image_url):
                        break
                    else:
                        counter += 1
                        if counter == 100:
                            image_url = None
                            break

                permalink = random_post["data"]["permalink"]
                title = random_post["data"]["title"]
                subreddit_title = random_post["data"]["subreddit"]
                embed = discord.Embed(
                    title=f"{title}",
                    description="",
                    url=f"https://reddit.com{permalink}",
                    color=0x38B6FF,
                )
                embed.set_image(url=image_url)
                embed.set_footer(text=f"By r/{subreddit_title}")
                await interaction.followup.send(embed=embed)

    @christmas.error
    async def christmas_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    

    #ISITCHRISTMAS COMMAND
    @app_commands.command(name="isitchristmas", description="Is it christmas yet??? By christmascountdown.live")
    @app_commands.checks.cooldown(1, 5.0)
    async def isitchristmas(self, interaction: discord.Interaction) -> None:
        apiIsToday = "https://christmascountdown.live/api/is-today"
        apiTimeleft = "https://christmascountdown.live/api/timeleft/days"
        async with aiohttp.ClientSession() as session:
            async with session.get(apiIsToday) as response:
                resIsToday = await response.json()
        async with aiohttp.ClientSession() as session:
            async with session.get(apiTimeleft) as response:
                resTimeleft = await response.json()
                if resIsToday is True:
                    embed = discord.Embed(
                        title="Is it Christmas?",
                        description="Yes, it's Christmas! :D",
                        color=0x38B6FF
                        )
                    await interaction.response.send_message(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Is it Christmas?",
                        description="No, it's not Christmas. ;(",
                        color=0x38B6FF
                        )
                    embed.add_field(
                        name="When is it tho?",
                        value=f"It's in {int(resTimeleft)} days!"
                    )
                    await interaction.response.send_message(embed=embed)

    @isitchristmas.error
    async def isitchristmas_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    #JOKE COMMAND
    @app_commands.command(name="joke", description="Christmas jokes! By christmascountdown.live")
    @app_commands.checks.cooldown(1, 5.0)
    async def joke(self, interaction: discord.Interaction) -> None:
        api = "https://christmascountdown.live/api/joke"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as response:
                simpl = await response.json()
                embed = discord.Embed(
                    title=simpl['question'],
                    description=simpl['answer'],
                    color=0x38B6FF
                    )
                await interaction.response.send_message(embed=embed)

    @joke.error
    async def joke_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
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
    await bot.add_cog(Fun(bot))