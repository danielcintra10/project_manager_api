# Project Manager
### API to help Project Managers with projects & team tasks. Developed using Django & Django REST Framework.

### What is this project about:
Project manager API makes it easier to manage projects and tasks in developer teams. Users authenticated as project managers will be able to create new projects and create 
tasks associated with these projects that will be entrusted to users authenticated as developers. These tasks have a deadline for completion and arrival. 
This deadline is notified to the project managers via email, and developers who are assigned tasks are notified using email when a new task is created. 
Project managers will be able to list the created projects with their respective tasks, see the specific information of a certain project, delete or deactivate projects, 
as well as list the created tasks, see the specific information of a task, deactivate or delete tasks, filter the tasks by project, by developer, see the developers available 
for new tasks among other functions. In the case of developers, their functions are a little more limited, mainly their access is closely related to the tasks and projects 
in which they participate. The project has all the configuration for user management based on the roles of project manager and developers.

>[!Note]
> 
> This is an example project to show some of my skills and my working methodology through the commit history.

### What will you see in this project:

- Work with Django.
- Creation of models.
- Relations between models.
- Custom user model.
- Use of managers.
- Work with signals.
- Work with the Django ORM.
- Admin site.
- Use of django-simple-history to audit models.
- Views and routing.
- Permissions.
- Authentication using JWT.
- Management and creation of API with Django REST Framework.
- Work with serializers.
- Creation of unit tests for models, serializers and API endpoints.
- Redis and Django.
- Creation of asynchronous tasks with Celery.
- Task scheduling with celery-beat.
- Cache in views.
- Creation of Django custom commands.
- Mail server configuration.
- API documentation using drf-spectacular.
- Work with environment variables.
- Work with virtual environments.
- Requirements file.
- Code formatting using Black.

## Getting started

### Required: 
- Python 3.11 or later
- PostgreSQL
- Redis

### Clone repository
First you will need to clone down the repository.

1) Create a new directory on your computer. This will be the 'root directory'.

2) Open a terminal and cd into the root directory.

3) You can now clone the project from GitHub. You can do this a few different ways.
I use HTTPS.
```
- git clone https://github.com/danielcintra10/project_manager_api.git .
```
### Virtual environment
Create a virtual environment to run the project.
1) Inside the root directory open a terminal and use the following command 
to create a virtual environment.

```
python -m venv venv
```
2) Now activate the virtual environment with the following command.
#### windows machine
```
venv\Scripts\activate.bat
```

#### mac/linux
```
source venv/bin/activate
```

You will know your virtual environment is active when your terminal displays the following:
```
(venv) path\to\project\
```

### Project Requirements 
Let's go ahead and install the project requirements. 
Add the following code to you terminal.
```
pip install -r requirements.txt
```

### Secrets and Environment Variables
It is good practice to separate sensitive information from your project. 
I have installed a package called 'python-dotenv' that helps me manage secrets easily. 
Let's go ahead and create an .env file to store information that is specific to our working environment. 
Use the following command in your terminal.

#### windows machine
```
copy .env.template .env
```
#### mac/linux
```
cp .env.template .env
```
You can use the .env file to store API keys, secret_keys, app_passwords, db_secret_info, and you will gain access to these in the Django app.
Use the .env.template file as a reference to configure the environment variables that are required in this project.

### Email server configuration
It is necessary to configure the SMTP mail server you want to use. 
In my case I used gmail as SMTP server, in the .env.template file there are the necessary instructions to configure the mail server.
In case of errors in the operation of the mail server, it is possible to review the EmailLog on the administration site.

### Database migrations
Before starting the project, it is necessary to create a database. The project is structured to use PostgreSQL databases. 
If you need to use another database management system, you need to make extra configurations in the settings.py file to make the project work correctly.  
Remember after creating the database, create the necessary environment variables to achieve the correct connection between the database and Django.
Then let's create the database tables.
Use the following command:

~~~~
python manage.py migrate
~~~~

### Redis Database
In the case of Redis, its use in the project is related to caching and as a broker between celery and django, no additional configurations are necessary 
for its correct functioning. The Redis server simply needs to be enabled and working correctly.

To check that redis is successfully installed in our system, open redis-cli and enter ping. 
If you get PONG as output then congratulations you have successfully installed redis in your system.

### Celery
In this project, Celery is used for the execution of asynchronous tasks by the server. Especially the sending of emails is configured to be carried out through 
asynchronous tasks, which improves the performance of the API. The dependencies necessary to use celery were installed correctly if you installed the necessary 
project requirements set in the requirements.txt file.

The project does not need additional configurations regarding the use of celery, but it is important to clarify that for celery to send the processes that you
want to execute to the task queue and for them to be carried out, a celery worker must be running.
To execute a celery worker run the following command:

~~~~
celery -A core.celery worker --loglevel=info -P eventlet 
~~~~

I use eventlet to manage concurrency.

### Celery-beat
There are tasks that need to execute repeatedly after regular intervals of time like sending a push notification to every user 
on a new item's arrival on an e-commerce site. Celery beat helps us to schedule such tasks at regular intervals.

#### How celery-beat works
Celery beat creates two tables in the database, one that is responsible for storing the time intervals and another that stores the tasks to be executed, 
in the case of the latter one of its fields refers to the time intervals table and this is how a task is related to a time interval.

In this project I use celery-beat to schedule an asynchronous task that will be executed every day at 9:00 AM, this is responsible for reviewing the tasks assigned 
to developers and verifying if they reached their deadline, if so, it is emailed the project manager to notify said event.

The creation of new tasks can be handled easily from the administration site but in this case I have created a custom django command that can be executed from the terminal which is responsible for the correct configuration of this task.
It is important to clarify that to run this command it is necessary to perform the relevant migrations in the database beforehand and once it is executed it is not necessary to do this action again because the task will be configured correctly.
Run this command to configure celery-beat correctly:

~~~~
python manage.py config_periodic_task
~~~~

As in the case of celery, for this task to be executed asynchronously in the established time interval, a worker must be running.
To execute a celery-beat worker run the following command:

~~~~
celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler 
~~~~

### Administration Site
You need a user with administrator permissions specially to access to the admin site,
you can run the following command and follow the instructions to create a superuser

~~~~
python manage.py createsuperuser
~~~~

### Test
To test the correct operation of the project, unit tests were created for models, serializers and endpoints. 
To execute these tests you simply have to execute the following command:

~~~
python manage.py test
~~~

### Run the project
Now you can run the server:

~~~
python manage.py runserver
~~~

### API Documentation
To create documentation for this API I use drf-spectacular. 
With the server running you can read this documentation using the urls created for this purpose.

~~~
api/v1/schema/swagger-ui/
~~~

~~~
api/v1/schema/redoc/
~~~


***
***
