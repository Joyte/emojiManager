import os
import discord
from discord import app_commands
from discord.ext.commands import has_permissions

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")


@tree.command(name="manageemoji", description="Manage your emojis")
async def manage_emoji(interacton: discord.Interaction):
    await interacton.response.send_message(
        "To manage your emoji, please [visit the website](https://emoji.joyte.dev)!",
        ephemeral=True,
    )


def run_bot():
    if not os.getenv("TOKEN"):
        raise ValueError(
            "No token provided, please set the TOKEN environment variable."
        )

    client.run(os.getenv("TOKEN"))
