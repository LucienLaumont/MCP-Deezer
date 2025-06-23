# types/chart.py
from pydantic import BaseModel
from typing import List
from types.album import Album
from types.track import Track
from types.artist import Artist

class ChartSection(BaseModel):
    data: list[dict]

class Chart(BaseModel):
    tracks: ChartSection
    albums: ChartSection
    artists: ChartSection
    playlists: ChartSection
