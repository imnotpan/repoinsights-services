from .extract_client import ExtractDataClient
from .load_client import LoadDataClient
from .enqueue_client import QueueClient
import json
from typing import Dict, Any, List, Union
from datetime import datetime
from ..utils.utils import format_dt, gh_api_to_datetime
from loguru import logger
import uuid


class EmptyQueueError(Exception):
    pass


class ExtractError(Exception):
    pass


class LoadError(Exception):
    pass


class InsightsClient:
    def __init__(self, data_types: List) -> None:
        self.data_types = data_types
        self.until = datetime.now()
        self.uuid = uuid.uuid4().hex

    def get_from_pendientes(self):
        queue_repo = QueueClient().get_from_queue()
        if queue_repo:
            self.owner = queue_repo["owner"]
            self.repo = queue_repo["project"]
            self.since: Union[datetime, None] = (
                gh_api_to_datetime(queue_repo["last_extraction"])
                if queue_repo["last_extraction"]
                else None
            )
            logger.critical("QUEUE pendientes {project}", project=queue_repo)
        else:
            raise EmptyQueueError("No hay proyectos en la cola")

    def extract(self) -> List[Dict[str, Any]]:
        logger.critical(
            "Extracting from GitHub {owner}/{project} DESDE -> {since} HASTA -> {until} {data_types}",
            owner=self.owner,
            project=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )

        extract_data = ExtractDataClient(
            owner=self.owner,
            repo=self.repo,
            since=self.since,
            until=self.until,
            data_types=self.data_types,
        )
        try:
            data = extract_data.extract()
            return data
        except Exception as e:
            logger.critical(f"Error extracting data from GitHub: {e}")
            raise ExtractError("Error extracting data from GitHub")

    def load(self, results) -> None:
        logger.critical(f"Loading to TEMP DB")
        try:
            load_client = LoadDataClient(results, self.uuid)
            load_client.load_to_temp_db()
            self.project_id = load_client.get_project_id()
        except Exception as e:
            logger.critical(f"Error loading data to TEMP DB: {e}")
            raise LoadError("Error loading data to TEMP DB")

    def enqueue_to_curado(self) -> None:
        project_data = {
            "uuid": self.uuid,
            "owner": self.owner,
            "repo": self.repo,
            "project_id": self.project_id,
            "since": format_dt(self.since) if self.since else None,
            "until": format_dt(self.until) if self.until else None,
            "data_types": self.data_types,
        }
        json_data = json.dumps(project_data)
        QueueClient().enqueue(json_data)
        logger.critical(f"Project ENQUEUE to CURADO published")
