## Running the Application

1. Clone github repository
    ```
    git clone https://github.com/caneledip/ku-polls.git
    ```

2. Change directory to ku-polls
    ```
    cd ku-polls
    ```

3. Create Virtual Environment
    ```
    python -m venv env
    ```
4. Start the server in the virtual environment. 
   ```
   # activate the virtual environment for this project. On Linux or MacOS:
   source env/bin/activate

   # on MS Windows:
   env/Scripts/activate
   ```
5. Install the requirements from requirements.txt
   ```
   pip install -r requirements.txt
   ```
6. Set up environment variables

    ```
    echo "DEBUG=False" >> .env
    ```
    ```
    echo "SECRET_KEY=your_secret_key_here" >> .env
    ```
    ```
    echo "TIME_ZONE=Asia/Bangkok" >> .env
    ```
    ```
    echo "ALLOWED_HOSTS=localhost,127.0.0.1,::1" >> .env
    ```
    
    You can set environment varialbe yourself, try looking at [sample.env](sample.env)

7. Load data
   </br>migrate model to create database
    ```
    python manage.py migrate
    ```
    load data from data file
    ```
    python manage.py loaddata data/users.json

    python manage.py loaddata data/polls-v4.json

    python manage.py loaddata data/votes.json
    ```
    You can also load all data in from one line.
    ```
    python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
    ```

8. Run server:
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

9. In a web browser, navigate to <http://localhost:8000>

10. To stop the server
</br>press CTRL-C in the terminal window. Exit the virtual environment by closing the window or by typing:
    ```
    deactivate
    ```