# RepoInsights
Software to extract, generate, and visualize development process metrics.

This repository contains software for metric extraction and generation.

## Dependencies
1. Docker
2. Python
3. Pipenv
4. Redis
5. Postgres
6. RabbitMQ

## How to run locally with Docker

Our Docker compose file creates a container with all necessary dependencies ready to use.
Steps: 
1. Clone the project.
2. Create a `.env` file based on .env.example.
3. Add a `tokens.json` file to `/services/extract_service`.
4. Create the containers using the docker-compose.local.yml ` docker compose -f docker-compose.local.yml up `.

## Format of `tokens.json` 
The `tokens.json` file contains the [personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to extract information from the GitHub API. 
The GitHub API allows up to 5,000 calls per token per hour.
`tokens.json` format:

`{ "keys": [ "ghp_", "ghp_", "ghp_" ] } `

If the token doesn't exist in the extract_service, you should see an error in the service logs, the error is something like:
```
2024-04-02 20:04:46 2024-04-02 23:04:46.488 | CRITICAL | services.extract_service.client:check_tokens:155 - Error al obtener tokens: ('Error al obtener tokens', FileNotFoundError(2, 'No such file or directory'))
```


# Documentation
The documentation is available in the docs folder.
1. [Metabase](docs/metabase.md)
2. [Consolidada database](docs/consolidada.md)
