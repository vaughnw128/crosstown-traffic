"""Simple models for locational ease."""

# built-in
from __future__ import annotations

# external
from pydantic import BaseModel


class Location(BaseModel):
    address: str
    longitude: float
    altitude: float
    latitude: float
    battery: str
    ip: str
    network: str


class TrafficRequest(BaseModel):
    location: Location
    trigger: str
