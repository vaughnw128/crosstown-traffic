"""Discord cog module for invoking app commands and views."""

# built-in
import os
from datetime import datetime
from io import BytesIO

import aiohttp

# external
import discord
from discord.ext import commands
from magika import Magika

from crosstown_traffic.models import Location

from crosstown_traffic.helpers.logging import logger

magika = Magika()


class MapsView(discord.ui.View):
    def __init__(self, location: Location):
        super().__init__()
        self.location = location

    # UI button to get the static google map
    @discord.ui.button(label="Maps", style=discord.ButtonStyle.green)
    async def maps_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        static_map_url = (
            f"https://maps.googleapis.com/maps/api/staticmap?"
            f"center={round(self.location.latitude, 6)},{round(self.location.longitude, 6)}"
            "&zoom=17&size=400x400&maptype=hybrid"
            f"&markers=color:blue%7Clabel:V%7C{round(self.location.latitude, 6)},{round(self.location.longitude, 6)}"
            f"&key={os.getenv('GOOGLE_MAPS_KEY')}"
        )
        print(static_map_url)
        fb = await grab_file_bytes(static_map_url)
        try:
            await interaction.followup.send(
                file=discord.File(fp=fb, filename="map.png")
            )
        except Exception as e:
            logger.error(e)

    # UI button to get the static streetview
    @discord.ui.button(label="Street View", style=discord.ButtonStyle.green)
    async def streetview_button_callback(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        static_street_view_url = (
            f"https://maps.googleapis.com/maps/api/streetview?size=400x400"
            f"&location={round(self.location.latitude, 6)},{round(self.location.longitude, 6)}"
            f"&fov=80"
            f"&pitch=0&key={os.getenv('GOOGLE_MAPS_KEY')}"
        )
        fb = await grab_file_bytes(static_street_view_url)
        await interaction.followup.send(
            file=discord.File(fp=fb, filename="streetview.png")
        )


class Traffic(commands.Cog):
    """Location class to handle the all location subtasks."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize location."""
        self.bot = bot


async def setup(bot: commands.Bot) -> None:
    """Sets up the cog"""
    await bot.add_cog(Traffic(bot))
    logger.info("Loaded")


def get_location_embed(location: Location):
    embed = discord.Embed(title="Tracker", color=0xE8921E)
    embed.add_field(name="Timestamp", value=datetime.now(), inline=True)
    embed.add_field(
        name="Coordinates",
        value=f"{location.latitude}, {location.longitude}",
        inline=True,
    )
    embed.add_field(name="Altitude", value=location.altitude, inline=True)
    embed.add_field(name="Battery Level", value=location.battery, inline=True)
    embed.add_field(name="Network", value=location.network, inline=True)
    embed.add_field(name="Address", value=location.address, inline=True)
    return embed


async def grab_file_bytes(url: str) -> BytesIO:
    """Grabs the bytes of a file from the URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return BytesIO(await resp.read())
