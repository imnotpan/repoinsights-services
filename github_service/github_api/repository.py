from ..config import GHToken
from ..github import GitHubExtractor
from github.Repository import Repository
from .user import GHUser
from typing import Dict, Any
import json


class GHRepository:
    def __init__(self, repo: Dict[str, Any]) -> None:
        self.url = repo["url"]
        self.owner = GHUser(repo["owner"])
        self.name = repo["name"]
        self.description = repo["description"]
        self.language = repo["language"]
        self.created_at = repo["created_at"]
        self.forked_from = False if repo["fork"] is False else True
        self.forked_from_id = None
        self.raw_repo = repo

    def set_forked_from_id(self, forked_from_id: int) -> None:
        self.forked_from_id = forked_from_id

    def set_owner_id(self, owner_id: int) -> None:
        self.owner_id = owner_id

    def set_repo_id(self, id: int) -> None:
        self.id = id

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "name": self.name,
            "owner_id": self.owner_id,
            "description": self.description,
            "language": self.language,
            "created_at": self.created_at,
            "forked_from": self.forked_from_id,
        }
