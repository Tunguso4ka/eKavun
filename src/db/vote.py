from typing import Dict, Optional, Union

from .base_db import DB
from .passport import PassportDB
from .party import PartyDB
from models import VoteInfo, Candidates

class VoteDB(PartyDB, PassportDB, DB):
    async def get_vote_info(self) -> VoteInfo:
        async with self.connection.execute("""
            SELECT title, text FROM VOTE_INFO
        """) as cursor:
            res = await cursor.fetchall()
            if res: return res[0]
            return 0

    async def save_vote_info(self, title: str, text: str) -> int:
        await self.connection.execute("""
            INSERT OR REPLACE INTO VOTE_INFO VALUES (?, ?)
        """, (title, text))
        await self.commit()
        return 0

    async def get_candidates(self) -> Candidates:
        async with self.connection.execute("""
            SELECT id, name FROM CANDIDATES
        """) as cursor:
            res = await cursor.fetchall()
            if res: return res
            return 0

    async def save_candidates(self, id: int, name: str) -> int:
        await self.connection.execute("""
            INSERT INTO CANDIDATES VALUES (?, ?)
        """, (id, name))
        await self.commit()
        return 0

    async def update_candidates(self, id: int, name: str) -> int:
        await self.connection.execute("""
            UPDATE CANDIDATES SET name=? WHERE id=?
        """, (name, id))
        await self.commit()
        return 0
    
    async def save_vote(self, id: int, vote: int) -> int:
        await self.connection.execute("""
            INSERT OR REPLACE INTO VOTED_FOR VALUES (?, ?)
        """, (id, vote))
        await self.commit()
        return 0

    async def get_voted_for(self) -> int:
        async with self.connection.execute("""
            SELECT id, voted FROM VOTED_FOR
        """) as cursor:
            res = await cursor.fetchall()
            if res: return res
            return 0

    async def delete_vote(self) -> int:
        await self.connection.execute("DELETE FROM VOTED_FOR")
        await self.connection.execute("DELETE FROM CANDIDATES")
        await self.connection.execute("DELETE FROM VOTE_INFO")
        await self.commit()
        return 0
