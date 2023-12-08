import random
import time
import discord

from discord import app_commands
from discord.app_commands import AppCommandError, Choice
from discord.ext import commands
from components import db, hohoitems

exclamain = db.client.exclamain


# COG CLASS
class Economy(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # FISH COMMAND
    @app_commands.command(name="fish", description="Fishes fish!")
    @app_commands.checks.cooldown(1, 5.0)
    async def fish(self, interaction: discord.Interaction):
        bitemj = "<:bit:1137510432354095104>"
        while True:
            item_caught = random.choice(fishitems.fishitemslist)
            item_name = list(item_caught)[0]
            item_chance = item_caught[item_name]["chance"]

            chance = random.uniform(0, 1)
            if chance <= item_chance:
                break

        item_value = item_caught[item_name]["value"]
        item_description = item_caught[item_name]["description"]
        embed = discord.Embed(
            title="It's fishing time!", description="", color=0xB40000
        )
        embed.add_field(name="You caught:", value=item_description)
        for item in fishitems.fishitemslist:
            if str(item).find(item_name) >= 0:
                if item[item_name]["emjid"] != None:
                    emjid = item[item_name]["emjid"]
                    embed.add_field(name=f"<:{item_name}:{emjid}>", value="")
                else:
                    embed.add_field(name=f":{item_name}:", value="")
        embed.add_field(name=f"Value: {item_value} {bitemj}", value="", inline=False)

        item_count = 0
        for item in fishitems.fishitemslist:
            item_count += 1
        calc = 1 / item_count * item_chance
        calcper = calc * 100
        embed.set_footer(text="Chance of catching: {0}%".format(round(calcper, 2)))
        await interaction.response.send_message(embed=embed)

        # DATABASE CODE
        query = {"userid": interaction.user.id}
        inventory = await exclamain.inventory.find_one(query)
        if inventory is None:
            data = {"userid": interaction.user.id, "bits": 0}
            await exclamain.inventory.insert_one(data)
            add_item = {"$inc": {f"{item_name}": 1}}
            await exclamain.inventory.update_one(query, add_item)
        else:
            add_item = {"$inc": {f"{item_name}": 1}}
            await exclamain.inventory.update_one(query, add_item)

    @fish.error
    async def fish_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # INVENTORY COMMAND
    @app_commands.command(
        name="inventory",
        description="See your inventory and the total value of your items!",
    )
    @app_commands.checks.cooldown(1, 5.0)
    async def inventory(self, interaction: discord.Interaction):
        bitemj = "<:bit:1137510432354095104>"
        query = {"userid": interaction.user.id}
        _filter = {"_id": 0, "userid": 0, "bits": 0}
        if await exclamain.inventory.find_one(query) is None:
            embed = discord.Embed(
                title="You don't have anything in your inventory!",
                description="",
                color=0xB40000,
            )
            embed.add_field(name="Try catching some fish with `/fish`!", value="")
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(
                title="Your Inventory", description="", color=0xB40000
            )
            total_value = 0
            index = 0
            inventory = await exclamain.inventory.find_one(query)
            invfilter = await exclamain.inventory.find_one(query, _filter)
            for item in invfilter:  # type: ignore
                if inventory[item] == 0:  # type: ignore
                    continue
                item_clean = item.replace("_", " ")
                for fish in fishitems.fishitemslist:
                    fishname = list(fish)[0]
                    if fishname == item:
                        value = fish[item]["value"]
                        if str(fish).find(item) >= 0:
                            if fish[item]["emjid"] != None:
                                emjid = fish[item]["emjid"]
                                embed.add_field(
                                    name=f"{item_clean.title()} <:{item}:{emjid}>" + f" x {inventory[item]}",  # type: ignore
                                    value=f"{inventory[item]*value} {bitemj} total @ {value} {bitemj}",  # type: ignore
                                    inline=False,
                                )
                            else:
                                embed.add_field(
                                    name=f"{item_clean.title()} :{item}:" + f" x {inventory[item]}",  # type: ignore
                                    value=f"{inventory[item]*value} {bitemj} total @ {value} {bitemj}",  # type: ignore
                                    inline=False,
                                )

            for item in invfilter:  # type: ignore
                amount = inventory[item]  # type: ignore
                for locfish in fishitems.fishitemslist:
                    locfishname = list(locfish)[0]
                    if locfishname == item:
                        value = locfish[item]["value"]
                        _calc = amount * value
                        total_value = total_value + _calc
                index += 1  # Increments the index by 1
            embed.set_footer(text=f"Total Value: {total_value}")
            await interaction.response.send_message(embed=embed)

    @inventory.error
    async def inventory_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # LEADERBOARD COMMAND
    @app_commands.command(name="leaderboard", description="See the leaderboard!")
    @app_commands.checks.cooldown(1, 5.0)
    async def leaderboard(self, interaction: discord.Interaction):
        bitemj = "<:bit:1137510432354095104>"
        await interaction.response.defer(thinking=True)
        embed = discord.Embed(
            title="Global Leaderboard - Top 5", description="", color=0xB40000
        )
        place = 1
        cursor = exclamain.inventory.find()
        cursor.sort("bits", -1).limit(10)
        async for inventory in cursor:
            tag_user = await self.bot.fetch_user(inventory["userid"])
            embed.add_field(
                name=f"{place} - {tag_user}",
                value=f"Bits: {inventory['bits']} {bitemj}",
                inline=False,
            )
            place += 1
            if place > 5:
                break
        await interaction.followup.send(embed=embed)

    @leaderboard.error
    async def leaderboard_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # BALANCE COMMAND
    @app_commands.command(name="balance", description="See your balance!")
    @app_commands.checks.cooldown(1, 5.0)
    async def balance(self, interaction: discord.Interaction):
        bitemj = "<:bit:1137510432354095104>"
        embed = discord.Embed(title="Your Balance:", description="", color=0xB40000)
        query = {"userid": interaction.user.id}
        inventory = await exclamain.inventory.find_one(query)
        if inventory is None:
            embed = discord.Embed(
                title="You don't have a balance yet!", description="", color=0xB40000
            )
            embed.add_field(name="Try selling some fish with /sell!", value="")
            await interaction.response.send_message(embed=embed)
        embed.add_field(name="", value=f"{inventory['bits']} {bitemj}")  # type: ignore
        await interaction.response.send_message(embed=embed)

    @balance.error
    async def balance_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # SELL & SELLALL AUTOCOMPLETE
    async def item_autocompletion(self, interaction: discord.Interaction, current: str):
        query = {"userid": interaction.user.id}
        _filter = {"_id": 0, "userid": 0, "bits": 0}
        itemlist = []
        inventory = await exclamain.inventory.find_one(query)
        invfilter = await exclamain.inventory.find_one(query, _filter)
        for _item in invfilter:  # type: ignore
            if inventory[_item] == 0:  # type: ignore
                continue
            item_clean = _item.replace("_", " ")
            itemlist.append(Choice(name=f"{item_clean.title()}", value=f"{_item}"))
        return itemlist

    # SELL COMMAND
    @app_commands.command(name="sell", description="Sell your items!")
    @app_commands.autocomplete(item=item_autocompletion)
    @app_commands.checks.cooldown(1, 5.0)
    async def sell(self, interaction: discord.Interaction, item: str, amount: int):
        bitemj = "<:bit:1137510432354095104>"
        query = {"userid": interaction.user.id}
        _filter = {item: 1}
        invfilter = await exclamain.inventory.find_one(query, _filter)
        if invfilter[item] == 0:  # type: ignore
            await interaction.response.send_message("You don't have that item!")
        else:
            if amount > invfilter[item]:  # type: ignore
                await interaction.response.send_message(
                    "You don't have that many items!"
                )
            elif amount <= 0:
                await interaction.response.send_message("You can't sell nothing!")
            else:
                for locfish in fishitems.fishitemslist:
                    locfishname = list(locfish)[0]
                    if locfishname == item:
                        value = locfish[item]["value"]
                        bit_calc = value * amount
                        updatecontent = {"$inc": {"bits": bit_calc, f"{item}": -amount}}
                        await exclamain.inventory.update_one(query, updatecontent)

                        item_clean = item.replace("_", " ")
                        embed = discord.Embed(
                            title="Sold!", description="", color=0xB40000
                        )
                        embed.add_field(
                            name="Item:",
                            value=f":{item}: {item_clean.title()}",
                            inline=False,
                        )
                        embed.add_field(name="Amount:", value=amount, inline=True)
                        embed.add_field(
                            name="Sold for:", value=f"{bit_calc} {bitemj}", inline=False
                        )
                        await interaction.response.send_message(embed=embed)

    @sell.error
    async def sell_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # SELL ALL COMMAND
    @app_commands.command(name="sellall", description="Sell your items!")
    @app_commands.autocomplete(item=item_autocompletion)
    @app_commands.checks.cooldown(1, 5.0)
    async def sellall(self, interaction: discord.Interaction, item: str):
        bitemj = "<:bit:1137510432354095104>"
        query = {"userid": interaction.user.id}
        _filter = {item: 1}
        invfilter = await exclamain.inventory.find_one(query, _filter)
        if invfilter[item] == 0:  # type: ignore
            await interaction.response.send_message("You don't have that item!")
        else:
            max_items = invfilter[item]  # type: ignore
            for locfish in fishitems.fishitemslist:
                locfishname = list(locfish)[0]
                if locfishname == item:
                    value = locfish[item]["value"]
                    bit_calc = value * max_items
                    updatecontent = {"$inc": {"bits": bit_calc, f"{item}": -max_items}}
                    await exclamain.inventory.update_one(query, updatecontent)
                    item_clean = item.replace("_", " ")
                    embed = discord.Embed(title="Sold!", description="", color=0xB40000)
                    embed.add_field(
                        name="Item:",
                        value=f":{item}: {item_clean.title()}",
                        inline=False,
                    )
                    embed.add_field(
                        name="Amount:", value=f"All ({max_items})", inline=True
                    )
                    embed.add_field(
                        name="Sold for:", value=f"{bit_calc} {bitemj}", inline=False
                    )
                    await interaction.response.send_message(embed=embed)

    @sellall.error
    async def sellall_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xB40000,
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Economy(bot))
