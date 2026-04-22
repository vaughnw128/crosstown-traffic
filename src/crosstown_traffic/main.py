"""Main module for the running of the FastAPI handler"""

# built-in
import asyncio
import os
from contextlib import asynccontextmanager

# external
import discord

# project
from crosstown_traffic.exts import traffic
from crosstown_traffic.exts.traffic import MapsView
from crosstown_traffic.models import TrafficRequest, StatusResponse
from crosstown_traffic import db
from fastapi import FastAPI
from crosstown_traffic.bot import CrosstownTraffic

DISCORD_CHANNEL = int(os.getenv("CHANNEL_ID"))

# Initialize the discord bot and all of it's intents
intents = discord.Intents.all()

client = CrosstownTraffic(
    command_prefix="~",
    intents=intents,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    loop = asyncio.get_event_loop()
    # noinspection PyAsyncCall
    loop.create_task(client.start(os.getenv("DISCORD_TOKEN")))

    yield

    print("Shutting down!")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Nothing here, teehehheheheheheh!"}

@app.post("/api/mta")
async def mta(request: TrafficRequest):
    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has boarded the subway!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)


@app.post("/api/arrived_home")
async def arrived_home(request: TrafficRequest):
    await db.record_event("home")

    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has arrived home!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)


@app.post("/api/left_home")
async def left_home(request: TrafficRequest):
    await db.record_event("away")

    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has left home!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(embed=embed, view=location_view)


@app.get("/api/status", response_model=StatusResponse)
async def status():
    return await db.get_status()


@app.post("/api/arrived_luca")
async def arrived_luca(request: TrafficRequest):

    if "lexington" not in request.location.address.lower():
        return

    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has arrived luca!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(content="<@195332546551087104>", embed=embed, view=location_view)


@app.post("/api/left_luca")
async def left_luca(request: TrafficRequest):

    if "lexington" not in request.location.address.lower():
        return

    embed = traffic.get_location_embed(request.location)
    embed.title = "Vaughn has left luca!"

    location_view = MapsView(request.location)

    channel = await client.fetch_channel(DISCORD_CHANNEL)
    await channel.send(content="<@195332546551087104>", embed=embed, view=location_view)
