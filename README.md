# Task Manager API

A RESTful Task Management API built with FastAPI and MongoDB. This project allows users to register, authenticate using JWT, and manage their personal tasks with features such as priority levels, due dates, task status tracking, filtering, searching, pagination, and dashboard statistics.

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication
* Protected Routes

### Task Management

* Create Task
* Get Task by ID
* Get All Tasks
* Update Task
* Delete Task

### Task Attributes

* Priority (Low, Medium, High)
* Status (Pending, In Progress, Completed)
* Due Date
* Completed At Timestamp
* Created At Timestamp
* Updated At Timestamp

### Advanced Features

* Filter Tasks by:

  * Priority
  * Status
  * Due Date

* Search Tasks by:

  * Title
  * Description

* Pagination

  * Page Number
  * Limit

* Dashboard Statistics

  * Total Tasks
  * Completed Tasks
  * Pending Tasks
  * In Progress Tasks

## Tech Stack

* FastAPI
* MongoDB
* Motor (Async MongoDB Driver)
* Pydantic
* JWT Authentication
* Passlib (Password Hashing)

## Installation

### Prerequisites

Make sure you have installed:

* Python 3.10+
* MongoDB
* Git

### Clone the Repository

```bash
git clone https://github.com/hlaingminthant172210-dev/Task_Manager.git
cd Task_Manager
```

### Create a Virtual Environment

```bash
python -m venv myenv
```

### Activate the Virtual Environment

#### Linux 

```bash
source myenv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=your_database_name
```

### Run the Application

```bash
uvicorn App.Routes.main:app --reload

(or)

Check:

$which uvicorn

If it shows something like:

/usr/bin/uvicorn

that's the problem.

It should look more like:

.../myenv/bin/uvicorn

Try running:

python -m uvicorn App.Routes.main:app --reload

instead of:

uvicorn App.Routes.main:app --reload

This forces Python to use packages from the active virtual environment.
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

## Project Structure

Task_Manager/
├── App/
│   ├── CRUD/
│   ├── Models/
│   ├── Routes/
│   ├── Utils/
├── .env
├── .gitignore
├── requirements.txt
└── README.md


## API Endpoints

### Authentication

POST /register

POST /login

### Tasks

POST /tasks/

GET /tasks/{task_id}

GET /tasks/

PUT /tasks/{task_id}

DELETE /tasks/{task_id}

### Filtering

GET /tasks/filters

Example:

/tasks/filters?priority=high

/tasks/filters?status=completed

/tasks/filters?due_date=2026-07-08

### Search

GET /tasks/search?keyword=project

### Pagination

GET /tasks/pagination?page=1&limit=10

### Dashboard Statistics

GET /tasks/dashboard

## Learning Outcomes

This project helped me practice:

* FastAPI Development
* MongoDB CRUD Operations
* JWT Authentication
* Password Hashing
* Dependency Injection
* Data Validation using Pydantic
* Query Parameters
* Filtering and Searching
* Pagination
* Project Structure Organization

## Future Improvements

* Task Sorting
* Category Management
* Task Tags
* Email Reminders
* File Attachments
* Unit Testing
* Docker Deployment

## Author

Hlaing Min Thant
A Mechanical Engineering student learning Python and Data Structures.Interested in backend development and IoT,building projects to grow into a software engineer.