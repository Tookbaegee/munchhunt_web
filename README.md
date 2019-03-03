# Munch Hunt Website

## Running on Local Machine For Development 

To get project running on your local machine:

1. Ensure python and pip are working. You may need to use `python3` and `pip3` in certain cases.
2. Clone the project. Ensure you are in the right directory by typing `cd munch-hunt-website` so that you're in the root of the site.
3. In the project directory, type `python -m venv venv`. This creates the python virtual environment.
4. Activate the virtual environment. Do this by typing `venv\Scripts\activate` on Windows, and `source venv/bin/activate` on Linux.
5. Install the package dependencies with the following command: `pip install flask flask-wtf python-dotenv flask-bootstrap4 flask-mail flask-sitemap flask-recaptcha flask-sqlalchemy flask-migrate flask-login flask-argon2 pyjwt autoenv psycopg` 
6. Set the environment variable for running the project. On a standard Linux shell, the command for this is `export FLASK_APP=site_dev.py`. On windows, in powershell, `$env:FLASK_APP = "site_dev.py"`. 
7. Optional: set debug environment variable so that the server refreshes whenever files are changed. This environment variable is called `FLASK_DEBUG` and it should be set to a value of `1`.
8. For development, sqlite or PostgreSQL can be used. To not use PostgreSQL, remove the DATABASE_URL line from the .env file. Otherwise, install postgresql-11
9. If using postgreSQL, create a database called `munch_hunt` with a user `munch_hunt` which has permissions to access `munch_hunt` database. Give it a password and change the DATABASE_URL in .env to match this new password.
10. Type the following commands: `flask db init; flask db migrate; flask db upgrade`
11. Type `flask run` in the console to run the application.
12. Hit CTRL + C to quit the application. 

## Running on Deployment Server (LINUX ONLY!!! Do NOT use root user.)

Preface: Ensure ports 80 and 443 are open (HTTP and HTTPS), and that you are using a non-root user. You could use root user, but it's best to have the site files owned by a non-root user.

1. Type the following commands to make sure everything is set up properly:

```bash
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
sudo apt install nginx
sudo apt install python3-certbot-nginx
```

2. Create a new file called 'site' in `/etc/nginx/sites-available/` using `sudo vi /etc/nginx/sites-available/site`. Copy paste these contents into it:

```
server {
    server_name _;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/site/site.sock;
    }

    listen 80; # managed by Certbot
}
```

Note: change the `_` next to `server_name` whenever you get a domain name set up pointing at the IP address of your server (A record for ipv4 which is standard, AAAA record for ipv6 which is new)

3. Symbolically link the new config file by typing: `sudo ln -s /etc/nginx/sites-available/site /etc/nginx/sites-enabled/`.  
4. Disable the default Nginx config by typing `sudo rm /etc/nginx/sites-enabled/default`. The default config can still be found in `/etc/nginx/sites-available`.  
5. cd to the www folder by typing `cd /var/www/`.   
6. Clone this git repository into this directory with `sudo git clone [REPOSITORY LINK]`.   
7. Rename the folder by typing `sudo mv /var/www/munch-hunt-website /var/www/site`  
8. cd to this folder, `cd /var/www/site`.  
9. In the project directory, type `python -m venv venv`. This creates the python virtual environment.  
10. Activate the virtual environment by typing `source venv/bin/activate`.   
11. Install the package dependencies with the following command: `pip install flask flask-wtf python-dotenv flask-bootstrap4 flask-mail flask-sitemap flask-recaptcha flask-sqlalchemy flask-migrate flask-login flask-argon2 pyjwt autoenv psycopg`  
12. Set the permissions of the website (VERY IMPORTANT) with this command: `sudo chown -R [YOUR_USERNAME]:www-data /var/www/site`   
13. It is now time to create the service that starts the site. Type `sudo vi /etc/systemd/system/site.service` and paste the following cotents:  

```
[Unit]
Description="uwsgi instance which serves the flask_site app"
After=network.target

[Service]
User=[YOUR_USERNAME]
Group=www-data
WorkingDirectory=/var/www/site/
Environment="PATH=/var/www/site/venv/bin"
ExecStart=/var/www/site/venv/bin/uwsgi --ini site.ini

[Install]
WantedBy=multi-user.target
```
14. Install postgresql-11 by following the instructions on their website to add the proper repository and install from there. 
15. Create a database called `munch_hunt` with a user `munch_hunt` which has permissions to access `munch_hunt` database.
16. Type the following commands: `flask db init; flask db migrate; flask db upgrade`
17. Type the following command to start the site: `sudo systemctl start site`  
18. Go to the IP address or domain name of the server and the site will be running.   
Optional: For a domain name, once you get it pointed, type `sudo certbot`. Follow the steps to create a Let's Encrypt certificate, it is pretty straightforward. The only thing to watch out for is ensure that you select 'redirect all'.   
Now your site will have HTTPS on its domain.  