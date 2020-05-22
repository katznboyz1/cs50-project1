#import statements
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import scoped_session as sqlalchemy_orm_scoped_session
from sqlalchemy.orm import sessionmaker as sqlalchemy_orm_sessionmaker
import flask, flask_session

#the application variable for flask
app = flask.Flask(__name__)

#the path to the static directory
app._static_folder = 'static'

#set up the session
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
flask_session.Session(app)

#the home page/search page for books
@app.route('/', methods = ['GET', 'POST'])
def route_rootIndex():

    #get if the user is logged in
    if (flask.session.get('logged_in') is None):
        loggedIn = False
    else:
        loggedIn = True
    
    #return the template for /
    return flask.render_template('rootIndex.html', loggedIn = loggedIn)

#the login page
@app.route('/login', methods = ['GET', 'POST'])
def route_rootLogin():

    return 'tmp login page'

#the register page
@app.route('/register', methods = ['GET', 'POST'])
def route_rootRegister():

    return 'tmp register page'

#the temporary development page
@app.route('/test', methods = ['GET', 'POST'])
def route_rootTest():

    #return a message
    return 'Testing page'