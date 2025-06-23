import httpx
from config import get_settings

settings = get_settings()

class BaseDeezerClient:
    def __init__(self):
        self.base_url = settings.deezer_base_url
        self.client = httpx.AsyncClient()

    async def _get(self, endpoint: str, params: dict = None) -> dict:
        response = await self.client.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
