## Running the Application

1. Start the server in the virtual environment. 
   ```
   # activate the virtual environment for this project. On Linux or MacOS:
   source env/bin/activate

   # on MS Windows:
   env\Scripts\activate

   # Configure virtual environment by looking at sample.env
   ```
   This starts a web server listening on port 8000.

2. Install the requirements from requirements.txt
   ```
   pip install -r requirements.txt
   ```
3. Load data
    ```
    # migrate model to create database
    python manage.py migrate

    # load data from data file
    python manage.py loaddata data/users.json

    python manage.py loaddata data/polls-v4.json

    python manage.py loaddata data/votes.json
    ```
    You can also load all data in from one line.
    ```
    python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
    ```

4. Run server:
   ```
   python manage.py runserver
   ```
   You should see this message printed in the terminal window:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
   If you get a message that the port is unavailable, then run the server on a different port (1024 thru 65535) such as:
   ```
   python3 manage.py runserver 12345
   ```

4. In a web browser, navigate to <http://localhost:8000>

5. To stop the server, press CTRL-C in the terminal window. Exit the virtual environment by closing the window or by typing:
   ```
   deactivate
   ```