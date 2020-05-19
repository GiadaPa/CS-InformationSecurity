# InformationSecurity
PenTesting

## Table of contents

- [Gettings started](#getting-started)
- [Docker environment](#docker-environment)
- [Information](#information)

## Getting started

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

### Prerequisites

For a ready to use Docker environment with all prerequisites already installed and prepared, you can check out the [Docker environment](#docker-environment) section.

### Source code

Get a copy of the repository:

```bash
git clone git@github.com:GiadaPa/InformationSecurity.git
```
or alternatively:
```bash
git clone https://github.com/GiadaPa/InformationSecurity.git
```

Change directory:

```bash
cd InformationSecurity/
```

### Dependencies

## Docker environment

For the project a Docker environment is already prepared and ready to use with all necessary prerequisites.

These Docker containers are the same as used by the continuous integration servers.

### Installation

Install [Docker](https://docs.docker.com/install/) (with Docker Compose) locally on your machine.

### Start and stop the containers

Before start working you have to start the Docker containers:

```
docker-compose up --build --detach
```

After finished working you can stop the Docker containers:

```
docker-compose stop
```

### Running commands inside the container

When the containers are running, you can execute any command inside the environment. Just replace the dots `...` in the following example with the command you wish to execute:

```bash
docker-compose run --rm app /bin/bash -c "..."
```

Some examples are:

```bash
docker-compose run --rm app /bin/bash -c "npm run start"
```

## Joomla

Joomla can be accessed at [localhost:8080](localhost:8080)

### Configuration details

You will need your database server address, database name, and database user credentials to install Joomla.

- Database Type: MySQL (PDO)
- Host Name: joomladb
- Username: root
- Password: password
- Database name: joomladb

## Information

### Documentation

More documentation can be found at ...

### Contributor
