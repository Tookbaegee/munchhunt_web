To get project running on your local machine:

1. Ensure python and pip are working. You may need to use 'python3' and 'pip3' in certain cases.
2. Clone the project. 
3. In the project directory, type 'python -m venv venv'
4. Activate the virtual environment. Do this by typing 'venv\scripts\Activate' on Windows, and 'source venv/bin/activate' on Linux.
5. Install the package dependencies with the following command: 'pip install flask flask-wtf python-dotenv flask-bootstrap4 flask-mail flask-sitemap 
6. Set the environment variable for running the project. On a standard Linux shell, the command for this is 'export FLASK_APP=fsite.py'. On windows, in powershell, '$env:FLASK_APP = "fsite.py"'. 
7. Optional: set debug environment variable so that the server refreshes whenever files are changed. This environment variable is called 'FLASK_DEBUG' and it should be set to a value of '1'.