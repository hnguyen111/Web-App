# Importing the Flask Framework

from modules import *
from flask import *
import database
import configparser


page = {}
session = {}

# Initialise the FLASK application
app = Flask(__name__)
app.secret_key = 'SoMeSeCrEtKeYhErE'


# Debug = true if you want debug output on error ; change to false if you dont
app.debug = True


# Read my unikey to show me a personalised app
config = configparser.ConfigParser()
config.read('config.ini')
unikey = config['DATABASE']['user']
portchoice = config['FLASK']['port']

#####################################################
##  INDEX
#####################################################

# What happens when we go to our website
@app.route('/')
def index():
    # If the user is not logged in, then make them go to the login page
    if( 'logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['unikey'] = unikey
    page['title'] = 'Welcome'
    return render_template('welcome.html', session=session, page=page)

################################################################################
# Login Page
################################################################################

# This is for the login
# Look at the methods [post, get] that corresponds with form actions etc.
@app.route('/login', methods=['POST', 'GET'])
def login():
    page = {'title' : 'Login', 'unikey' : unikey}
    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our login value
        val = database.check_login(request.form['sid'], request.form['password'])

        # If our database connection gave back an error
        if(val == None):
            flash("""Error with the database connection. Please check your terminal
            and make sure you updated your INI files.""")
            return redirect(url_for('login'))

        # If it's null, or nothing came up, flash a message saying error
        # And make them go back to the login screen
        if(val is None or len(val) < 1):
            flash('There was an error logging you in')
            return redirect(url_for('login'))
        # If it was successful, then we can log them in :)
        session['name'] = val[1]
        session['sid'] = request.form['sid']
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        # Else, they're just looking at the page :)
        if('logged_in' in session and session['logged_in'] == True):
            return redirect(url_for('index'))
        return render_template('index.html', page=page)


################################################################################
# Logout Endpoint
################################################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    flash('You have been logged out')
    return redirect(url_for('index'))


################################################################################
# Transcript Page
################################################################################

@app.route('/transcript')
def transcript():
    # TODO
    # Now it's your turn to add to this ;)
    # Good luck!
    #   Look at the function below
    #   Look at database.py
    #   Look at units.html and transcript.html
    grades = database.get_transcript(session['sid'])
    # What happens if units are null?
    if (grades is None):
        # Set it to an empty list and show error message
        grades = []
        flash('Error, there are no transcript')
    page['title'] = 'Transcript'
    return render_template('transcript.html', page=page, session=session, grades=grades)


################################################################################
# List Units page
################################################################################

# List the units of study
@app.route('/list-units')
def list_units():
    # Go into the database file and get the list_units() function
    units = database.list_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Units of Study'
    return render_template('units.html', page=page, session=session, units=units)


@app.route('/list-textbooks')
def list_textbooks():
    # Go into the database file and get the list_units() function
    textbooks = database.list_textbooks()

    # What happens if classes are null?
    if (textbooks is None):
        # Set it to an empty list and show error message
        textbooks = []
        flash('Error, there are no textbook to show')
    page['title'] = 'Textbooks'
    return render_template('textbooks.html', page=page, session=session, textbooks=textbooks)


@app.route('/search_units')
def search_units():   
    return redirect(url_for('perform_units_search'))


@app.route('/perform_units_search', methods=['POST', 'GET'])
def perform_units_search():
    page = {'title' : 'Units Search'}
    unitofferings = []
    display_message = "Enter a textbook then press search."

    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our query values
        textbook = request.form['textbook']

        # If it's null, or nothing came up, flash a message saying error
        if(textbook is None):
            flash('There was an error getting your input')
            return redirect(url_for('perform_units_search'))

        # If it was successful, then we can perform the search:)
        unitofferings = database.search_units(textbook)

        if (unitofferings is None):
            # Set it to an empty list
            unitofferings = []
        display_message = "Found " + str(len(unitofferings)) + " unit(s) for textbook " + textbook + "'."
        return render_template('search_units.html', page=page, session=session, unitofferings=unitofferings, query_text=display_message)

    else:
        # Else, they're just looking at the page :)
        return render_template('search_units.html', page=page, session=session, unitofferings=unitofferings, query_text=display_message)


# Count the units of study
@app.route('/count-units')
def count_units():
    # Go into the database file and get the list_units() function
    units = database.count_units()

    # What happens if units are null?
    if (units is None):
        # Set it to an empty list and show error message
        units = []
        flash('Error, there are no units of study')
    page['title'] = 'Count Units of Study'
    return render_template('count_units.html', page=page, session=session, units=units)


@app.route('/update_textbook')
def update_textbook():   
    return redirect(url_for('perform_textbook_update'))

@app.route('/perform_textbook_update', methods=['POST', 'GET'])
def perform_textbook_update():
    page = {'title' : 'Update Textbook'}
    display_message = "Enter unitofering details then press update."

    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our query values
        uoSCode = request.form['uoSCode']
        semester = request.form['semester']
        year = request.form['year']
        textbook = request.form['textbook']

        # If it's null, or nothing came up, flash a message saying error
        if(textbook is None or uoSCode is None or semester is None or year is None):
            flash('There was an error getting your input')
            return redirect(url_for('perform_textbook_update'))

        # If it was successful, then we can perform the search:)
        database.update_textbook(textbook, uoSCode, semester, year)
        display_message = "Updated"
        return render_template('update_textbook.html', page=page, session=session, query_text=display_message)

    else:
        # Else, they're just looking at the page :)
        return render_template('update_textbook.html', page=page, session=session, query_text=display_message)
    
    
@app.route('/search_books')
def search_books():   
    return redirect(url_for('perform_books_search'))

@app.route('/perform_books_search', methods=['POST', 'GET'])
def perform_books_search():
    page = {'title' : 'Books Search'}
    books = []
    display_message = "Enter a textbook then press search."

    # If it's a post method handle it nicely
    if(request.method == 'POST'):
        # Get our query values
        textbook = request.form['textbook']

        # If it's null, or nothing came up, flash a message saying error
        if(textbook is None):
            flash('There was an error getting your input')
            return redirect(url_for('perform_books_search'))

        # If it was successful, then we can perform the search:)
        books = database.search_books(textbook)

        if (books is None):
            # Set it to an empty list
            books = []
        display_message = "Found " + str(len(books)) + " book(s) with this(these) author(s) " + "."
        return render_template('search_books.html', page=page, session=session, books=books, query_text=display_message)

    else:
        # Else, they're just looking at the page :)
        return render_template('search_books.html', page=page, session=session, books=books, query_text=display_message)







