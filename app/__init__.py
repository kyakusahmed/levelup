from flask import Flask
from flasgger import Swagger
from re import match

app = Flask("__name__")

swagger = Swagger(app)


from app.models import db_conn
from app.views import Migration 
from app.views import redflag
from app.views import auth
from app.views import interventions 
from app.views import redflag
from app.views import auth
from app.models import interventions 
from app.models import redflag
from app.models import auth



