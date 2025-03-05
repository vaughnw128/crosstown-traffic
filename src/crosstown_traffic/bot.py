# built-in
import importlib
import inspect
import os
import pkgutil
import traceback
import types
from dataclasses import dataclass

# external
import discord
from discord import app_commands
from discord.ext import commands

# project modules
import crosstown_traffic.exts as exts

from crosstown_traffic.helpers.logging import logger


@dataclass
class CrosstownTraffic(commands.Bot):
    """Discord bot subclass for CrosstownTraffic"""

    def __init__(self, *args, **kwargs):
        """Initialize the bot class"""
        super().__init__(*args, **kwargs)

    async def sync_app_commands(self) -> None:
        """Sync the command tree to the guild"""
        await self.tree.sync()
        await self.tree.sync(guild=discord.Object(os.getenv("GUILD_ID")))

        logger.info("Command tree synced")

    async def load_extensions(self, module: types.ModuleType) -> None:
        """Load all cogs by walking the packages in exts."""
        logger.info("Loading extensions")
        for module_info in pkgutil.walk_packages(
            module.__path__, f"{module.__name__}."
        ):
            if module_info.ispkg:
                imported = importlib.import_module(module_info.name)
                if not inspect.isfunction(getattr(imported, "setup", None)):
                    continue
            await self.load_extension(module_info.name)
        logger.info("Extensions loaded")

    async def setup_hook(self) -> None:
        """Replacing default setup_hook to run on startup"""
        await self.load_extensions(exts)
        # await self.sync_app_commands()
        # self.tree.on_error = self.global_app_command_error
        logger.info("Started")

    async def global_app_command_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        """Handles app command errors"""
        if isinstance(error, discord.app_commands.CommandInvokeError):
            logger.error(traceback.format_exc())
            await interaction.followup.send("An unexpected error has occurred.")
        elif isinstance(error, app_commands.AppCommandError):
            await interaction.followup.send(error)
        else:
            logger.error(traceback.format_exc())

    async def on_error(self, event: str, *args, **kwargs) -> None:
        """Handles exts errors"""
        message = args[0]
        logger.warning("ERROR CAUGHT")
        logger.warning(f"Event: {event}")
        logger.warning(f"Message: {message}")
        logger.warning(traceback.format_exc())
