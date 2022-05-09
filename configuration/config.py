from os import environ
from dotenv import load_dotenv
USE_DOTENV = environ.get("USE_DOTENV")

if(USE_DOTENV):
    load_dotenv()

variables = {
    ## Your Development Environment
    "ENV": environ.get("ENV") if environ.get("ENV") else "development",
    ## SECRET_KEY
    "SECRET_KEY": environ.get("SECRET_KEY") if environ.get("SECRET_KEY") else "secret",
    ## PORT
    "PORT": environ.get("PORT") if environ.get("PORT") else 7000,
}