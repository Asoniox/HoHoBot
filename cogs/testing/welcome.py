import discord
import random

from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from components import db

hohobotMain = db.client.hohobotMain
welcome = hohobotMain.welcome


#COG CLASS
class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    #WELCOME MESSAGE
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        pfp = member.avatar
        welcomemsg = [
            f"{member.mention} has joined the server! Would you like some hot tea?",
            f"{member.mention} has joined the server! Did you decorate your Christmas tree?",
            f"{member.mention} has joined the server! Do you like hot chocolate?",
            f"{member.mention} has joined the server! Did you buy cookies for Santa?"
            ]
        guild_id = member.guild.id
        query = {'guild_id': guild_id}
        if await welcome.find_one(query) is None:
            return
        else:
            welcomedb = await welcome.find_one(query)
            channel_id = welcomedb['welcome_channel'] #type: ignore
            welcome_channel = self.bot.get_channel(channel_id)
            embed = discord.Embed(
                title="Welcome!",
                description=random.choice(welcomemsg),
                color=0x38B6FF
                )
            embed.set_thumbnail(url=pfp)
            await welcome_channel.send(embed=embed) #type: ignore
    
    group = app_commands.Group(name="welcome", description="Welcome commands! Make sure HoHoBot has the correct permissions!")

    #CHANNEL SELECT AUTOCOMPLETE
    async def channel_autocomplete(self, interaction: discord.Interaction, current: str):
        channel_list = []
        if interaction.guild is None:
            channel_list.append(Choice(name = 'No Channels', value = '0'))
        else:
            index = 0
            for channel in interaction.guild.channels:
                    if index >= 25:
                        return channel_list
                    elif channel in interaction.guild.categories:
                        continue
                    elif channel in interaction.guild.voice_channels:
                        continue
                    elif channel in interaction.guild.forums:
                        continue
                    elif channel in interaction.guild.stage_channels:
                        continue
                    else:
                        channel_list.append(Choice(name = f'{channel.name}', value = str(channel.id)))
                        index += 1
        return channel_list

    #WELCOME COMMAND
    @group.command(name="addchannel", description="Add a channel for welcoming new members! Make sure HoHoBot has the correct permissions!")
    @app_commands.autocomplete(channel=channel_autocomplete)
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.describe(channel="Choose from options or input channel ID (Settings > Advanced > Developer Mode)")
    async def welcome_add(self, interaction: discord.Interaction, channel: str) -> None:
        channel_id = int(channel)
        try:
            welcome_channel = await self.bot.fetch_channel(channel_id)
            guild_id = welcome_channel.guild.id #type: ignore
            if welcome_channel is None:
                embed = discord.Embed(
                    title="Error!",
                    description="The ID you entered isn't a channel!",
                    color=0x38B6FF
                    )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        except ValueError:
            embed = discord.Embed(
                title="Error!",
                description="The ID you entered is not an ID!",
                color=0x38B6FF
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        except discord.NotFound:
            embed = discord.Embed(
                title="Error!",
                description="The ID you entered is invalid!",
                color=0x38B6FF
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error!",
                description="I don't have permission to send messages to that channel!",
                color=0x38B6FF
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return


        #SAVE TO DATABASE
        query = {'guild_id': guild_id}
        welcomedb = await welcome.find_one(query)
        if welcomedb is None:
            data = {
                'guild_id': guild_id,
                'welcome_channel': channel_id
                }
            await welcome.insert_one(data)
            embed = discord.Embed(
                title="Success!",
                description=f"Set up <#{channel_id}> as the welcome channel!",
                color=0x38B6FF
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            if welcomedb['welcome_channel'] != channel_id:
                data = {
                    'welcome_channel': channel_id
                    }
                update_id = { "$set": { 'welcome_channel': channel_id } }
                await welcome.update_one(query, update_id)
                embed = discord.Embed(
                    title="Updated!",
                    description=f"Set up <#{channel_id}> as the **new** welcome channel!",
                    color=0x38B6FF
                    )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                title="Wait!",
                description=f"<#{channel_id}> is already set up as the welcome channel!",
                color=0x38B6FF
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)


    @welcome_add.error
    async def welcome_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
                embed = discord.Embed(title="Error!", description=error, color=0xb40000)
                await interaction.response.send_message(embed=embed, ephemeral=True)

    
    @group.command(name="removechannel", description="Removes the saved welcome channel!")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def welcome_remove(self, interaction: discord.Interaction):
        if interaction.guild is None:
            embed = discord.Embed(
                title="Error!",
                description="You can only use this command in a server!",
                color=0x38B6FF
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            guild_id = interaction.guild.id
            query = {'guild_id': guild_id}
            if await welcome.find_one(query) is None:
                embed = discord.Embed(
                    title="Error!",
                    description="You don't have a welcome channel set up!",
                    color=0x38B6FF
                    )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                filter = {'guild_id': guild_id}
                await welcome.delete_one(filter)
                embed = discord.Embed(
                    title="Removed!",
                    description="Removed the welcome channel successfully!",
                    color=0x38B6FF
                    )
                await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @welcome_remove.error
    async def welcome_remove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
                embed = discord.Embed(title="Error!", description=error, color=0xb40000)
                await interaction.response.send_message(embed=embed, ephemeral=True)

    @group.command(name="prompts", description="See the prompts that welcome your users! (Non-Modifiable)")
    async def prompts(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Welcome Prompts (Non-Modifiable)",
            description="\
- {member.mention} has joined the server! Would you like some hot tea?\n\
- {member.mention} has joined the server! Did you decorate your Christmas tree?\n\
- {member.mention} has joined the server! Do you like hot chocolate?\n\
- {member.mention} has joined the server! Did you buy cookies for Santa?",
            color=0x38B6FF
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

            
async def setup(bot):
    await bot.add_cog(Welcome(bot))
