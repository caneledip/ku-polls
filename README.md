## KU Polls: Online Survey Questions 
[![Style checking](https://github.com/caneledip/ku-polls/actions/workflows/style-checking.yml/badge.svg)](https://github.com/caneledip/ku-polls/actions/workflows/style-checking.yml)
[![Python application](https://github.com/caneledip/ku-polls/actions/workflows/polls-testing.yml/badge.svg)](https://github.com/caneledip/ku-polls/actions/workflows/polls-testing.yml)

An application to conduct online polls and surveys based
on the [Django Tutorial project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/), with
additional features.

## Installation

- [Installation](Installation.md)

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

3. Run server:
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

## Demo Users
| User | Password |
|----|-----|
|admin|123|
|demo1|hackme11|
|demo2|hackme22|
|demo3|hackme33|


## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Vision Statement](../../wiki/Vision%20Statement)
- [Domain Model](../../wiki/Domain%Model)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Iteration 1](../../wiki/Iteration%201)
- [Iteration 2](../../wiki/Iteration%202)
- [Iteration 3](../../wiki/Iteration%203)
- [Iteration 4](../../wiki/Iteration%204)