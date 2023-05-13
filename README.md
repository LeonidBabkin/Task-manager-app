##                          A simple and flexible task management web application:

![Task manager image](https://hygger.io/wp-content/uploads/2019/01/02.-Break-down-your-tasks-to-smaller-time-units.jpg)                               
[![Actions Status](https://github.com/LeonidBabkin/python-project-52/workflows/hexlet-check/badge.svg)](https://github.com/LeonidBabkin/python-project-52/actions)
[![Actions Status](https://github.com/LeonidBabkin/python-project-52/workflows/run-tests/badge.svg)](https://github.com/LeonidBabkin/python-project-52/actions)
[![Actions Status](https://github.com/LeonidBabkin/python-project-52/workflows/run-linter/badge.svg)](https://github.com/LeonidBabkin/python-project-52/actions)
<a href="https://codeclimate.com/github/LeonidBabkin/python-project-52/maintainability"><img src="https://api.codeclimate.com/v1/badges/c1a8a775517c39eb83c5/maintainability" /></a>
<a href="https://codeclimate.com/github/LeonidBabkin/python-project-52/test_coverage"><img src="https://api.codeclimate.com/v1/badges/c1a8a775517c39eb83c5/test_coverage" /></a>

You can get familiar with the task manager app on the [Render.com](https://task-manager-app-kzsy.onrender.com).

The task management web application built with Python and Django framework. It allows you to set tasks, assign executors and change their statuses. Registration and authentication are required. 

To provide users with a convenient, adaptive, modern interface, the project uses the Bootstrap framework.

The frontend is rendered on the backend. This means that the page is built by the DjangoTemplates backend, which returns prepared HTML. And this HTML is rendered by the server.

PostgreSQL is used as the object-relational database system.


### Features

 * Set tasks
 * Assign executors
 * Assign task statuses
 * Set multiple tasks labels
 * Filter and list the tasks
 * User authentication and registration

 ### Technologies stack

* Python
* Django
* Poetry
* Bootstrap 4
* PostgreSQL
* Gunicorn
* Whitenoise
* Rollbar
* Flake8
* Pytest

### Installation prerequisites

#### Python 

 Before installing the package make sure you have Python version ^3.10

#### Poetry

The project uses the Poetry dependency manager. You can install Poetry via its official [website](https://python-poetry.org/docs/#installing-with-the-official-installer)

#### PostgreSQL

PostgreSQL is used as the main object-relational database system. You have to install it  via [website](https://www.postgresql.org/download/)

###  Application installation

```
git clone https://github.com/LeonidBabkin/python-project-52.git
cd python-project-52
make install
make migrate

```

### Utilization

Start the Gunicorn Web-server by running --> By default, the server will be available at http://0.0.0.0:8000.; 
Start it local in development mode --> The dev server will be at http://127.0.0.1:8000.;




