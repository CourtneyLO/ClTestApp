# DeploymenTestAppCL

The backend api, database and infrastructure for DeploymenTestAppCL

## Content

- [Setup and Running Backend Locally](#setup-and-running-locally)
	- [Setup Virtual Environment](#setup=virtual-environment)
	- [Install Dependencies](#install-dependencies)
	- [Setup Postgresql Database Locally](./docs/DATABASE-LOCAL-SETUP.md)
	- [Run Migration](#run-migration)
	- [Create Super](#create-super-user)
	- [Run Server](#run-server)
- [Routes](#routes)
- [Other Commands](#other-commands)
- [Environments](#environments)
- [Deployment](#deployment)
- [Tests](#tests)

## Setup and Running Backend Locally

### Setup Virtual Environment

You need to create and activate your virtual environment.

For information on how to do this, go [here](../docs/VIRTUAL-ENVIRONMENT.md)

### Install Dependencies

Run the following:

```
(virtualenvironment) $ make install
```

### Create environment variables file

```
(virtualenvironment) $ touch .env
```
Look at example.env file for variable names

Note: Environment should be set to local-development otherwise there will be no styling for the Django admin

### Setup Postgresql Database Locally

- If you are unsure how do do this, go [here](../docs/DATABASE-LOCAL-SETUP.md)

### Run Migration

```
$ make migrate
```

### Create Super User

- This will allow you access to the admin panel

```
$ make create-su
```

### Populate Database

- This will populate the database with the all the required data. See [here](../backend/populate-database.json). Exemplar and Universe data are just examples and will not necessarily be found in the production database

```
$ make populate
```

### Run Server

```
$ make run
```

- Go to http://localhost:8000/admin
- Use the username and password used to setup the super user to login to admin

## Routes

To see the routes, requests and response go [here](../docs/API_REQUESTS_AND_RESPONSES.md)

## Contribute

To create an app, run:

```
$ make app app=<app-name>
```

## Other Commands

### Create Tables locally

```
$ create-all-tables
```

This command:

- Runs the migration for each app
- Migrates each table

You will just have to upload all the table information

```
$ drop-all-tables
```

This command:

- Deletes all custom tables (each app's model) in the database
- Deletes each migration row related to the tables that have been deleted in the step above

All data for the custom tables will be deleted

## Environments

- Production
	- Api: [Production URL Here]

- Staging
	- API: [Staging URL Here]


## Deployment

Production and Staging get deployed through Github Actions using Zappa

## Tests

All tests:

```
make run
```

Single app test:

```
make run app=<app name>
```
