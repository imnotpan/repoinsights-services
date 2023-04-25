from ..config import GHToken
from .repository import GHRepository
from .handlers.commit_handler import CommitHandler
from .handlers.project_user_handler import ProjectUserHandler
from .handlers.label_handler import LabelHandler
from .handlers.issue_handler import IssueHandler
from .handlers.user_handler import UserHandler
from .handlers.pull_request_handler import PullRequestHandler

from ..requests.github import GitHubExtractor


class GitHubClient:
    def __init__(self, owner: str, repo: str):
        token = GHToken().get_token()
        self.repo = GitHubExtractor(owner, repo, token)
        if self.repo.repo is None:
            raise Exception("Repository not found")
        self.repository = GHRepository(self.repo.repo)
        self.commit_handler = CommitHandler(self.repo)
        # self.repository = GHRepository(self.repo)
        self.project_handler = ProjectUserHandler(self.repo)
        self.pull_request_handler = PullRequestHandler(self.repo)
        # self.user_handler = UserHandler()
        # self.label_handler = LabelHandler(self.repo)
        self.issue_handler = IssueHandler(self.repo)
