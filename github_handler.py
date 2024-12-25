from typing import Dict
import aiohttp
import asyncio

class GitHubHandler:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_notifications(self) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.github.com/notifications",
                headers=self.headers
            ) as response:
                return await response.json()
    
    async def get_repo_events(self, repo: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.github.com/repos/{repo}/events",
                headers=self.headers
            ) as response:
                return await response.json()