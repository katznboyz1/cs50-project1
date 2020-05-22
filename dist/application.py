#import statements
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import scoped_session as sqlalchemy_orm_scoped_session
from sqlalchemy.orm import sessionmaker as sqlalchemy_orm_sessionmaker
import flask

#the application variable for flask
app = flask.Flask(__name__)

#the path to the static directory
app._static_folder = 'static'

#the home page/search page for books
@app.route('/', methods = ['GET', 'POST'])
def route_rootIndex():
    
    #return the template for /
    return flask.render_template('rootIndex.html')