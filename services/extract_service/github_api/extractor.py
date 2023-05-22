from typing import Optional, Dict, Any, List, Set, Iterator
from services.extract_service.github_api.controllers.user import (
    Repository,
    Commit,
    User,
)
from services.extract_service.github_api.controllers.issue import Issue
from services.extract_service.github_api.controllers.pull_request import PullRequest
from services.extract_service.github_api.github_api import GitHubAPI
from datetime import datetime


class GitHubExtractor:
    def __init__(
        self,
        usuario: str,
        repositorio: str,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None,
    ):
        self.usuario = usuario
        self.since = since
        self.until = until
        self.api = GitHubAPI()

        self.repositorio = Repository(self.api, repositorio, usuario)
        self.user_repo = User(self.api)
        self.commit_repo = Commit(self.api, usuario, repositorio)
        self.issue = Issue(self.api, usuario, repositorio)
        self.pull_request = PullRequest(self.api, usuario, repositorio)

    def obtener_repo_info(self):
        return self.repositorio.obtener_repositorio()

    def obtener_contribuidores(self):
        return self.repositorio.obtener_contribuidores()

    def obtener_usuario(self, usuario):
        return self.user_repo.obtener_usuario(usuario)

    def obtener_commits(self, since: Optional[datetime] = None, until=None):
        return self.commit_repo.obtener_commits(since=since, until=until)

    def obtener_commit(self, commit_sha):
        return self.commit_repo.obtener_commit(commit_sha)

    def obtener_commit_comments(self, commit_sha):
        return self.commit_repo.obtener_commit_comments(commit_sha)

    def obtener_comments(self):
        return self.commit_repo.obtener_comments()

    def obtener_issues(self, since=None, until=None, state=None):
        return self.issue.obtener_issues(since=since, until=until, state=state)

    def obtener_issues_comments(self):
        return self.issue.obtener_issues_comments()

    def obtener_issue_events(self, issue_id: str) -> List[Dict[str, Any]]:
        return self.issue.obtener_issue_events(issue_id)

    def obtener_issues_events(self):
        return self.issue.obtener_issues_events()

    def obtener_pull_requests(
        self, state=None, sort=None, direction=None, since=None, until=None
    ):
        return self.pull_request.obtener_pull_requests(
            state=state, sort=sort, direction=direction, since=since, until=until
        )

    def obtener_pull_requests_comments(self):
        return self.pull_request.obtener_pull_requests_comments()

    def obtener_labels(self):
        return self.repositorio.obtener_labels()

    def obtener_stargazers(self):
        return self.repositorio.obtener_stargazers()

    def obtener_milestone(self, state=None):
        return self.repositorio.obtener_milestone(state=state)
