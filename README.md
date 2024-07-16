# ToDo List API

Todo List API with Email and Google Sign-In Authentication

### Instructions on how to set up and run the project.

```sh
git clone https://github.com/pnasonov/todo-list-test-task
cd todo-list-test-task/
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create .env file from .env.sample and put proper values (Google OAuth 2.0 at https://console.developers.google.com/)

```sh
python manage.py migrate
python manage.py runserver
```

### Available endpoints

* http://localhost:8000/accounts/login/ - sign in page
* http://localhost:8000/accounts/signup/ - sign up page
* http://localhost:8000/accounts/google/login/?process=login - google auth page

Only authenticated users access ToDo tasks endpoints!

* http://localhost:8000/api/tasks/ all tasks for authenticated user, accept POST for creating ToDo
* http://localhost:8000/api/tasks/1/ detail ToDo view, accept PUT, DELETE methods




