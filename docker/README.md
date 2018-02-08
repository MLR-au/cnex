# Docker stuff

## Preamble

This folder contains the Dockerfiles and associated scripts for building
both the UI (interface) and API (service) containers.

## Build the containers

Build the containers with the following commands:

```
API:
> docker build --rm=true --tag "cnex/api" api

UI:
> docker build --rm=true --tag "cnex/ui" ui
```

## Run the containers

Ensure you have docker compose in your path then run:

```
> docker-compose -f {your-compose-file}.yml up -d
```

Obvisouly replace `{your-compose-file}.yml` with the fully qualified path
to your compose file (copy mlarosa-compose.yml and customise volume mounts
as required).

## Stopping the containers and cleaning up

```
> docker-compose -f {your-compose-file}.yml stop
> docker-compose -f {your-compose-file}.yml rm -f
```
