from pprint import pprint
from github.Commit import Commit
from github.GitAuthor import GitAuthor
from github.NamedUser import NamedUser
from github.PullRequestPart import PullRequestPart
from .user import InsightsUser
from datetime import datetime
from .comment import InsightsCommitComment
from typing import List, Union, Any, Dict
import json


class InsightsCommit:
    def __init__(self, commit: Dict[str, Any]):
        self.sha = commit["sha"]
        self.message = commit["commit"]["message"]
        self.author = InsightsUser(commit["author"]) if commit["author"] else None
        self.committer = (
            InsightsUser(commit["committer"]) if commit["committer"] else None
        )
        self.date = commit["commit"]["author"]["date"]
        self.parents = [parent["sha"] for parent in commit["parents"]]
        self.comments: List[InsightsCommitComment] = []

        self.raw_commit = commit

    def set_comments(self, comments: list[InsightsCommitComment]):
        self.comments = comments

    def set_author_id(self, author_id: Union[None, int]):
        self.author_id = author_id

    def set_committer_id(self, committer_id: Union[None, int]):
        self.committer_id = committer_id

    def set_project_id(self, project_id: int):
        self.project_id = project_id

    def get_comments(self) -> list[InsightsCommitComment]:
        return self.comments

    def to_dict(self) -> dict:
        return {
            "sha": self.sha,
            "author_id": self.author_id,
            "committer_id": self.committer_id,
            "created_at": self.date,
            "project_id": self.project_id,
        }
