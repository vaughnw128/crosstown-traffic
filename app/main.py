"""Main module for the running of the FastAPI handler"""

# built-in
import asyncio
import os
from contextlib import asynccontextmanager

# external
import discord

# project
from .exts import traffic
from .exts.traffic import MapsView
from .models import TrafficRequest
from fastapi import FastAPI
from .bot import CrosstownTraffic

DISCORD_CHANNEL = int(os.getenv("CHANNEL_ID"))

# Initialize the discord bot and all of it's intents
intents = discord.Intents.all()

client = CrosstownTraffic(
    command_prefix="~",
    intents=intents,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    # noinspection PyAsyncCall
    loop.create_task(client.start(os.getenv("DISCORD_TOKEN")))

    yield

    print("Shutting down!")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Nothing here, friend!"}

@app.post("/api/mta")
async def mta(request: TrafficRequest):
    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has boarded the subway!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)


@app.post("/api/arrived_home")
async def arrived_home(request: TrafficRequest):
    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has arrived home!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)


@app.post("/api/left_home")
async def left_home(request: TrafficRequest):
    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has left home!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)
