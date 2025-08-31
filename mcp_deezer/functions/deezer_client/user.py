from typing import List, Optional
from pydantic import BaseModel
from mcp_deezer.types import DeezerUserBase, DeezerUserSearch
from .base import BaseDeezerClient


class UserNameClient(BaseDeezerClient):
    async def search_users_by_name(self, user_name: str, limit: int = 10, strict: Optional[bool] = None, order: Optional[str] = None) -> List[DeezerUserSearch]:
        params = {
            "q": user_name,
            "limit": limit
        }
        
        if strict is not None:
            params["strict"] = "on" if strict else "off"
        
        if order:
            params["order"] = order
        
        try:
            data = await self._get("search/user", params)
            users = []
            for user_data in data.get("data", []):
                try:
                    user = DeezerUserSearch(**user_data)
                    users.append(user)
                except Exception as e:
                    continue
            return users
        except Exception as e:
            return []
    
    async def get_user(self, user_id: int) -> Optional[DeezerUserBase]:
        try:
            data = await self._get(f"user/{user_id}")
            return DeezerUserBase(**data)
        except Exception as e:
            return None