import os

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class ChannelButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="ch1", style=discord.ButtonStyle.primary)
    async def ch1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_nickname(interaction, "ch1")

    @discord.ui.button(label="ch2", style=discord.ButtonStyle.primary)
    async def ch2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_nickname(interaction, "ch2")

    @discord.ui.button(label="ch3", style=discord.ButtonStyle.primary)
    async def ch3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_nickname(interaction, "ch3")

    @discord.ui.button(label="ch4", style=discord.ButtonStyle.primary)
    async def ch4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await update_nickname(interaction, "ch4")

    @discord.ui.button(label="reset", style=discord.ButtonStyle.danger)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        await reset_nickname(interaction)


async def update_nickname(interaction: discord.Interaction, tag: str):
    guild = interaction.guild
    member = interaction.user

    # Remove tag from any other user who has it
    for m in guild.members:
        if m == member:
            continue
        if m.nick and tag in m.nick:
            new_nick = m.nick.replace(tag, "").strip()
            try:
                await m.edit(nick=new_nick)
            except discord.Forbidden:
                print(f"⚠️ Couldn't edit nickname of {m.display_name} (insufficient permissions)")

    # Now update the requesting user's nickname
    old_nick = member.nick or member.name

    # Remove any ch* tags
    new_nick = old_nick
    for i in range(1, 5):
        new_nick = new_nick.replace(f"ch{i}", "")
    new_nick = new_nick.strip()
    new_nick += f" {tag}"
    new_nick = new_nick.strip()

    try:
        await member.edit(nick=new_nick)
        await interaction.response.send_message(f"✅ You now have `{tag}`. If someone had it before — it's yours now 😎", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I can't change your nickname.", ephemeral=True)


async def reset_nickname(interaction: discord.Interaction):
    member = interaction.user
    old_nick = member.nick or member.name
    new_nick = old_nick
    for i in range(1, 5):
        new_nick = new_nick.replace(f"ch{i}", "")
    new_nick = new_nick.strip()

    try:
        await member.edit(nick=new_nick)
        await interaction.response.send_message("🔄 Your nickname has been reset.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I can't reset your nickname.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="start", description="Start interaction and choose channel")
async def start_command(interaction: discord.Interaction):
    await interaction.response.send_message("Choose your channel:", view=ChannelButtons(), ephemeral=True)


bot.run(str(os.getenv("LOGIN_TOKEN")))