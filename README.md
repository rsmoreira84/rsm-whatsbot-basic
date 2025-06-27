# RSM Whatsbot Basic app

Whatsapp automation messages example app. 

This app has been created to build a very basic Whatsapp automated app. 

It has a Twilio integration and all interactions with the user are handled in the code.


## Running locally:

Install pip
Install Python (3.9) - if using mac, try pyenv
Install Docker - if using mac, try Docker Desktop

### Installing dependencies locally
> $ pip install -r requirements.txt

### Starting docker
It will run MongoDB and Redis locally.
> $ docker compose up -d

### Starting the app
At the project root folder:
> $ python app.py


## Atlas 
### MongoDB
Create a free tier instance.

## Heroku
Create a free tier heroku app. 

### Redis
On Heroku, go to Resources and add a Redis instance (Rediscloud). 
Once it's provisioned, an environment variable will be added to Heroku (REDISCLOUD_URL). 
Adjust the key at the configurations/config.py if needed. 

### Mongo DB
Add the MongoDB connection string (uri) to Heroku variables.

### Deployment Process
On Heroku, configure Github to deploy versions everytime a push is done to the main branch.
Check the option to perform a deployment once the configuration is completed.

## Twilio
This app is using Twilio as the middleware for whatsapp integration. 
### How to configure it
Go to Twilio, create an account.

On Twillio console, go to *Messaging*, then *Try it out*, and choose *Send a Whatsapp message*.

On the Sandbox settings, configure your heroku app URL. (heroku app / open app)

On the Sandbox, configure your whatsapp. 


## APP ENDPOINTS
When running locally, it's not possible to simulate a whatsapp number sending messages. 

For solving this problem, an endpoint has been created (cURL):
> curl --location --request GET 'http://localhost:3000/http-sim' \
--header 'Content-Type: application/json' \
--data '{
    "from": "RSM-SIMULATOR",
    "body": "Hi!!!"
}'

Once you send a message, the collection users will be updated with your message. 



## PYTHON ENVIRONMENT - Version Config

Configuring the Python Version for this project.

It helps when you need to have different python versions per project.

Minimal version required: 3.10

_These instructions are based on Macos command lines._

### pyenv

Please, before starting the process, make sure you have pyenv correctly installed. 

### Python Version

Configure your Python version using pyenv. 

Lowest version required: 3.10.

### Configuring Virtual Env

This process will use your installed Python version to configure a pyenv Virtual Env and a Local Env, to be used by your project.

To configure it, you just need to execute the file ./pyenv-config.sh. 

> $ chmod +x pyenv-config.sh
> $ ./pyenv-config.sh

### Installing pip, setuptools, wheel, AND the project lib (requirements.txt) in your new Virtual Env

#### Activate your pyenv virtual environment in your terminal:
> $ pyenv activate whatsbot-env-3.12.9 

#### Upgrade pip and then install/upgrade setuptools and wheel:
> $ pip install --upgrade pip setuptools wheel

#### Install project libraries
> $ pip install -r requirements.txt

#### Deactivate the environment (optional, but good practice):
> $ pyenv deactivate

### Pycharm

1. Open your project.
2. Go to Pycharm Settings
3. Project / Python Interpreter
4. Add new interpreter
5. Select Virtual Environment > "Existing"
6. Then select the folder you have added your pyenv Virtual Env
   * usually: ~/.pyenv/versions/your-pyenv-virtual-env/bin/python3


## Running Unit Tests

The unit tests we have are covering only the most crucial files with the real rules. 

To run it, we need to use the virtual environment. 

Activating the virtual envirionment:
> $ pyenv activate whatsbot-env-3.12.9

Install any missing lib 
> (whatsbot-env-3.12.9) $ pip install {missing-lib}

Executing all tests
> (whatsbot-env-3.12.9) $ python -m unittest discover -v

Deactivate the environment (optional, but good practice):
> $ pyenv deactivate