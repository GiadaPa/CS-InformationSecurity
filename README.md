# InformationSecurity
PenTesting

## Table of contents

- [Gettings started](#getting-started)
- [Docker environment](#docker-environment)
- [Usage](#usage)
- [Information](#information)

## Getting started

These instructions will get you a copy of the project up and running
on your local machine for development and testing purposes.

### Prerequisites

For a ready to use Docker environment with all Joomla and its dependencies already installed and prepared, you can check out the [Docker environment](#docker-environment) section.

To run the attacks, the following prerequisites must be met:

- Python 3.4+ with pip

A package manager was used to simplify command execution. To use it, the following prerequisites must be met:

- NPM 6 / YARN 1.22

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

Using the package manager, run the following command:

```bash
yarn install-dependencies
```
or alternatively:
```bash
npm run install-dependencies
```

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

### Joomla

Joomla can be accessed at [localhost:8080](localhost:8080)

#### Configuration details

You will need your database server address, database name, and database user credentials to install Joomla.

- Database Type: MySQL (PDO)
- Host Name: joomladb
- Username: root
- Password: password
- Database name: joomladb

## Usage

The following section describes how to perform attacks through the package manager.

### Remote Code Execution

Run the following command:

```bash
yarn attack:rce VICTIM_URL
```
or alternatively:
```bash
npm run attack:rce VICTIM_URL
```

**VICTIM_URL** need to be specified with the relative protocol

If you are using the docker environment: 

```bash
yarn attack:rce http://localhost:8080/
```

### SQL injection

Run the following command:

```bash
yarn attack:sqli
```
or alternatively:
```bash
npm run attack:sqli
```

### XSS

Run the following command:

```bash
yarn attack:xss
```
or alternatively:
```bash
npm run attack:xss
```

## Information

### Documentation

More documentation can be found at ...

### Contributor
