## patients-counseling
A Backend Application for Patients-Counseling. It includes models for Patient, Counsellor, and Appointment, with functionalities for creating, updating, reading, and deleting records.


## Prerequisites
Make sure you have the following installed:
- Python 3.10 or higher
- Docker


## Docker Setup
Follow the steps below to start the containerized application:
1. Clone the repository
    ```console
    git clone https://github.com/Engr-Asad-Hussain/patients-counseling.git
    ```

2. Navigate to the project
    ```console
    cd patients-counseling
    ```

3. Build and start docker-compose file
    ```console
    docker-compose -f "./docker-compose.yaml" up -d
    ```

4. Check the logs of docker-compose
    ```console
    docker-compose logs -f patients
    ```
    Following logs will be printed ...
    ```
    patients  | Waiting for MySQL server to start...
    patients  | Waiting for MySQL server to start...
    patients  | Waiting for MySQL server to start...
    patients  | Waiting for MySQL server to start...
    patients  | Waiting for MySQL server to start...
    ```

5. When the MySQL server started. Press `ctrl + C`, then run the following command
    ```console
    docker-compose run --rm patients python manage.py migrate
    ```

6. Start making request in the Postman Collection. Follow the [docs](https://github.com/Engr-Asad-Hussain/patients-counseling/tree/main/docs) to get started with Postman Collection and documentation of endpoints.


## Local Setup
Follow the steps below to start the application in development environment:
1. Clone the repository
    ```console
    git clone https://github.com/Engr-Asad-Hussain/patients-counseling.git
    ```

2. Navigate to the project
    ```console
    cd patients-counseling
    ```

3. Create a virtual environment
    ```console
    python -m virtualenv venv
    ```

4. Activate the virtual environment - May vary depending on the OS.
    ```console
    . .\venv\Scripts\activate
    ```

5. Install Dependencies
    ```console
    pip install -r requirements.txt
    ```

6. Setup `.env` file. Create a `.env` file (`mkdir .env`) and placed all the environmental variables:
    ```console
    DEBUG=True
    SECRET_KEY="django-insecure-^(e^45o%hyibp#ut@7sy^e6(6j8sj844d*l9w7dcm-5=+zet=h"
    ```

7. Change the database configurations in `settings.json` file. Replace `DATABASE` settings with the following:
    ```console
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
            # "ENGINE": "django.db.backends.mysql",
            # "NAME": config("MYSQL_DATABASE"),
            # "USER": config("MYSQL_USER"),
            # "PASSWORD": config("MYSQL_PASSWORD"),
            # "HOST": config("MYSQL_HOST"),
            # "PORT": config("MYSQL_PORT"),
        }
    }
    ```

8. Make the migrations in the `sqlite`:
    ```console
    py ./manage.py migrate
    ```

9. Start the development server:
    ```console
    py ./manage.py runserver
    ```

10. Start making request in the Postman Collection. Follow the [docs](https://github.com/Engr-Asad-Hussain/patients-counseling/tree/main/docs) to get started with Postman Collection and documentation of endpoints.
