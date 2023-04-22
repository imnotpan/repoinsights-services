from db_connector.connector import DBConnector
from db_connector.database_handler import DatabaseHandler
from github_service.github_api.client import GitHubClient
from github_service.github_api.commit import GHCommit
from github_service.github_api.repository import GHRepository
from github_service.github_api.pull_request import GHPullRequest
from github_service.github_api.user import GHUser
from github_service.github_api.isssue import GHIssue
from pprint import pprint
import json
from typing import List, Union
from loguru import logger


class LoadData:
    def __init__(self, client: GitHubClient):
        self.temp_db = DatabaseHandler(DBConnector())
        self.repository = client.repository
        self.repository.set_repo_id(self.load_repository(self.repository))

    def load_repository(self, repository: GHRepository):
        logger.debug(
            "Loading repository {owner} {name}",
            owner=repository.owner.login,
            name=repository.name,
        )
        return self.temp_db.create_project(repository)

    def load_user(self, user: GHUser) -> int:
        logger.debug("Loading user {login}", login=user.login)
        return self.temp_db.create_user(user)

    def load_commit(self, commit: GHCommit) -> int:
        logger.debug("Loading commit {sha}", sha=commit.sha)
        return self.temp_db.create_commit(commit)

    def load_pull_request(self, pr: GHPullRequest):
        logger.debug("Loading pull request {number}", number=pr.number)
        self.temp_db.create_pull_request(pr)

    def load_watchers(self, watchers: List[GHUser]):
        logger.debug(
            "Loading watchers for repository {name}", name=self.repository.name
        )
        self.temp_db.create_watchers(watchers, self.repository.id)

    def load_data(self, results):
        for result in results:
            name, data = result["name"], result["data"]
            logger.critical(f"Loading {name}")
            if name == "owner":
                self.load_owner_data(data)
            elif name == "commit":
                self.load_commits_data(data)
            elif name == "watchers":
                self.load_watchers_data(data)
            elif name == "pull_request":
                self.load_pull_requests_data(data)
            elif name == "issues":
                self.load_issues_data(data)

    def load_issues_data(self, issues: List[GHIssue]):
        for iss in issues:
            pass

    def load_owner_data(self, owner: GHUser):
        self.repository.set_owner_id(self.load_user(owner))

    def load_commits_data(self, commits: List[GHCommit]):
        for commit in commits:
            commit.set_project_id(self.repository.id)
            commit.set_author_id(
                self.load_user(commit.author) if commit.author else None
            )
            commit.set_committer_id(
                self.load_user(commit.committer) if commit.committer else None
            )
            commit_id = self.load_commit(commit)
            # self.temp_db.create_commit_parents(commit_id, commit.parents)

    def load_watchers_data(self, watchers: List[GHUser]):
        self.load_watchers(watchers)

    def load_pull_requests_data(self, pull_requests: List[GHPullRequest]):
        for pr in pull_requests:
            pr.set_user_id(self.load_user(pr.author))
            self.update_repo_data(pr.head_repo)
            self.update_repo_data(pr.base_repo)
            self.update_commit_data(pr.head_commit)
            self.update_commit_data(pr.base_commit)
            pr.set_head_commit_id(self.load_commit(pr.head_commit))
            pr.set_base_commit_id(self.load_commit(pr.base_commit))
            if pr.head_repo is not None:
                pr.set_head_repo_id(self.load_repository(pr.head_repo))  # type: ignore
            if pr.base_repo is not None:
                pr.set_base_repo_id(self.load_repository(pr.base_repo))  # type: ignore
            self.load_pull_request(pr)

    def update_repo_data(self, pr_repo: Union[GHRepository, None]):
        if pr_repo is None:
            return

        if pr_repo.forked_from is True:
            pr_repo.set_forked_from_id(self.repository.id)
        if pr_repo.raw_repo["owner"] is not None:
            pr_repo.set_owner_id(self.load_user(pr_repo.owner))

    def update_commit_data(self, pr_commit: GHCommit):
        pr_commit.set_project_id(self.repository.id)
        if pr_commit.author is None:
            pr_commit.set_author_id(None)
        else:
            pr_commit.set_author_id(self.load_user(pr_commit.author))

        if pr_commit.committer is None:
            pr_commit.set_committer_id(None)
        else:
            pr_commit.set_committer_id(self.load_user(pr_commit.committer))
