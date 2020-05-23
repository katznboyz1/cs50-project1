#import statements
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy.orm import scoped_session as sqlalchemy_orm_scoped_session
from sqlalchemy.orm import sessionmaker as sqlalchemy_orm_sessionmaker
import flask, flask_session, string, os, argon2

#create the database connection
databaseEngine = sqlalchemy_create_engine(os.getenv('DATABASE_URL'))
databaseDatabase = sqlalchemy_orm_scoped_session(sqlalchemy_orm_sessionmaker(bind = databaseEngine))

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

    #get a list of random books
    books = databaseDatabase.execute('SELECT * FROM books ORDER BY RANDOM() LIMIT 20') #make these books into clickable links
    
    #return the template for /
    return flask.render_template('rootIndex.html', loggedIn = False if flask.session.get('logged_in') == None else True, books = books)

#the individual page for a book
@app.route('/book/<string:isbn>', methods = ['GET'])
def route_rootBook(isbn):
    
    #return a test page
    return 'isbn: {}'.format(isbn)

#the login page
@app.route('/login', methods = ['GET', 'POST'])
def route_rootLogin():
    
    #return the template for /login
    return flask.render_template('rootLogin.html', loggedIn = False if flask.session.get('logged_in') == None else True, loginErrorMessage = '')

#the login authentication page
@app.route('/authlogin', methods = ['POST'])
def route_rootAuthLogin():
    
    #get the username and password from the form
    password, username = str(flask.request.form.get('password')), str(flask.request.form.get('username'))

    #check if the login was successful
    loginSuccess = False

    #hash the password
    passwordHasher = argon2.PasswordHasher()
    hashedPassword = passwordHasher.hash(password)

    #get whether or not the user exists
    usernameExists = databaseDatabase.execute('SELECT * FROM users WHERE username = :username', {'username':username}).rowcount > 0

    #if the username exists then verify the password
    if (usernameExists):

        #get the hashed user password
        hashedUserPassword = databaseDatabase.execute('SELECT password FROM users WHERE username = :username', {'username':username})
        for each in hashedUserPassword:
            hashedUserPassword = each[0]

        #match the passwords
        try:
            loginSuccess = passwordHasher.verify(hashedUserPassword, password)
        except argon2.exceptions.VerifyMismatchError:
            loginSuccess = False

    #serve the webpage
    if (loginSuccess):
        flask.session['logged_in'] = [username, password]
        return flask.redirect(flask.url_for('route_rootIndex'))
    else:

        #return the template for /login with an error message
        return flask.render_template('rootLogin.html', loggedIn = False if flask.session.get('logged_in') == None else True, loginErrorMessage = 'Incorrect username or password!')

#the register page
@app.route('/register', methods = ['GET', 'POST'])
def route_rootRegister():

    #return the template for /register
    return flask.render_template('rootRegister.html', loggedIn = False if flask.session.get('logged_in') == None else True, registerErrorMessage = '')

#the logout page
@app.route('/logout', methods = ['POST']) #make it so that this is only post accessable
def route_rootLogout():

    #log the user out
    del flask.session['logged_in']

    #send the user to the home page
    return flask.redirect(flask.url_for('route_rootIndex'))

#the register authentication page
@app.route('/authregister', methods = ['POST'])
def route_rootAuthRegister():

    #get the username and password from the form
    password, password2, username = str(flask.request.form.get('password')), str(flask.request.form.get('passwordRepeat')), str(flask.request.form.get('username'))

    #variable for whether or not the registry was successful
    registrySuccess = True

    #the registry error
    registryError = 'Unknown error'

    #a list of acceptable characters for the username
    acceptableUsernameCharacters = [*string.ascii_uppercase, *string.ascii_lowercase, *string.digits, '_']

    #iterate through the username and check that the username is proper
    for char in username:
        if (char not in acceptableUsernameCharacters):
            registryError = 'Your username can only contain letters of the english alphabet, numbers, and underscores.'
            registrySuccess = False
    
    #check that the username isnt empty
    if (len(username) == 0):
        registryError = 'Your username can\'t be empty.'
        registrySuccess = False
    
    #check that the password is greater than or equal to 8 characters
    if (len(password) <= 8):
        registryError = 'Your password must be 8+ characters long.'
        registrySuccess = False
    
    #check that the passwords match
    if (password != password2):
        registryError = 'The passwords you entered don\'t match.'
        registrySuccess = False
    
    #check if the username exists in the users table
    if (databaseDatabase.execute('SELECT * FROM users WHERE username = :username', {'username':username}).rowcount > 0):
        registryError = 'That username is already in use.'
        registrySuccess = False

    #the password hash information
    passwordHash, passwordHashVersion = '', ''
    
    #if the registry is valid then hash the password
    if (registrySuccess):

        #hash the password
        passwordHasher = argon2.PasswordHasher()
        passwordHash = passwordHasher.hash(password)
        passwordHashVersion = 'argon2'

        #verify that the hash is valid
        registrySuccess = passwordHasher.verify(passwordHash, password)
        
        #set the error message if the password hashing failed
        if (not registrySuccess):
            registryError = 'Error while hashing your password.'
    
    #if the registry is still valid then add the user to the table
    if (registrySuccess):
        databaseDatabase.execute(
            'INSERT INTO users (username, password, password_version) VALUES (:username, :password, :password_version)', 
            {'username':username, 'password':passwordHash, 'password_version':passwordHashVersion}
        )
        databaseDatabase.commit()

        #set up the session variables
        flask.session['logged_in'] = [username, password]

    #serve the webpage
    if (registrySuccess):
        return flask.redirect(flask.url_for('route_rootIndex'))
    else:
        return flask.render_template('rootRegister.html', loggedIn = False if flask.session.get('logged_in') == None else True, registerErrorMessage = registryError)

#the temporary development page
@app.route('/test', methods = ['GET', 'POST'])
def route_rootTest():

    #return a message
    return 'Testing page'