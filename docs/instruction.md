## Instruction

Make sure that python 3.12 is installed in your system. You also need to install redis. After that follow the instruction below.
1. Download MedEasy.zip from the email attachment.
2. Unzip the project and navigate to project root folder where `requirements.txt` file is located.
3. Now create a virtual env using the following command.

    ```
   python -m venv myEnv
   ```
4. Now activate the activate the virtual env using the command below.
   
   ```bash
   myEnv\Scripts\activate
   ```
5. After activating the virtual env, now install the dependencies
   
   ```bash
   pip install -r requirements.txt
    ```

6. Everything is almost ready. Make sure that you run the `redis server`
7. Now run the following command to create migrations and migrate the model with database.
   
   ```bash
   python manage.py migrate

   python manage.py makemigrations medicine
   
   python manage.py migrate
    ```
8. Now run the project using the command 
   ```bash
   python manage.py runserver
   ```
9. It will run the project in port `8000`. URL will be [127.0.0.1:8000](http://127.0.0.1:8000)
10. You can access the api docs at [127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Unit Test

Run the following command to test the API.
```bash
python manage.py test
```
## Docker instruction

Open terminal in project root folder where `Dockerfile` is located.
Run the following command to setup the project and run.
   ```bash
   docker-compose up -d
   ```
You can also update the port and network in `docker-compose.yml` file.