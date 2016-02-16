from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, CatalogItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

### Connect to database and create database session ###
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

### Google login ###
# Read Google client secret file
CLIENT_ID = json.loads(
	open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to Google account
@app.route('/gconnect', methods=['POST'])
def gconnect():
	# Validate state token
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Obtain authorization code
	code = request.data

	try:
		# Upgrade the authorization code into a credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
	except FlowExchangeError:
		response = make_response(
			json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Check that the access token is valid.
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
		   % access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# If there was an error in the access token info, abort.
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'

	# Verify that the access token is used for the intended user.
	gplus_id = credentials.id_token['sub']
	if result['user_id'] != gplus_id:
		response = make_response(
			json.dumps("Token's user ID doesn't match given user ID."), 401)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Verify that the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(
			json.dumps("Token's client ID does not match app's."), 401)
		print "Token's client ID does not match app's."
		response.headers['Content-Type'] = 'application/json'
		return response

	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps('Current user is already connected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session for later use.
#	login_session['credentials'] = credentials
	login_session['gplus_id'] = gplus_id
	login_session['access_token'] = credentials.access_token

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)

	data = answer.json()

	login_session['username'] = data['name']
#	login_session['picture'] = data['picture']
	login_session['email'] = data['email']
	# ADD PROVIDER TO LOGIN SESSION
	login_session['provider'] = 'google'

	# see if user exists, if it doesn't make a new one
	user_id = getUserID(data["email"])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome, '
	output += login_session['username']
	output += '!</h1>'
#	output += '<img src="'
#	output += login_session['picture']
#	output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
	flash("you are now logged in as %s" % login_session['username'])
	print "done!"
	return output

# Disconnect from Google
@app.route('/gdisconnect')
def gdisconnect():
	# Only disconnect a connected user.
	credentials = login_session.get('access_token')
	if credentials is None:
		response = make_response(
			json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
#	access_token = credentials.access_token
	access_token = credentials
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]
	if result['status'] != '200':
		# For whatever reason, the given token was invalid.
		response = make_response(
			json.dumps('Failed to revoke token for given user.', 400))
		response.headers['Content-Type'] = 'application/json'
		return response

@app.route('/disconnect')
def disconnect():
	if 'provider' in login_session:
		if login_session['provider'] == 'google':
			gdisconnect()
			del login_session['gplus_id']
			del login_session['access_token']
#			del login_session['credentials']
#		if login_session['provider'] == 'facebook':
#			fbdisconnect()
#			del login_session['facebook_id']
		del login_session['username']
		del login_session['email']
#		del login_session['picture']
		del login_session['user_id']
		del login_session['provider']
		flash("You have successfully been logged out.")
		return redirect(url_for('showCatalogs'))
	else:
		flash("You were not logged in")
		return redirect(url_for('showCatalogs'))
### Ends Google login ###

# Create anti-forgery state token
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	return render_template('login.html', catalogs=catalogs, STATE=state)

### User ID ###
def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None

### CRUD ###

# Show all catalogs
@app.route('/')
@app.route('/catalog/')
def showCatalogs():
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	if 'username' not in login_session:
		return render_template('publiccatalog.html', catalogs=catalogs)
	else:
		return render_template('catalog.html', catalogs=catalogs)

# Show a single catalog
@app.route('/catalog/<string:catalog_name>/')
@app.route('/catalog/<string:catalog_name>/item/')
def showSingleCatalog(catalog_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
#	catalog_id = session.query(Catalog).filter_by(name=catalog_name).one().id
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	creator = getUserInfo(catalog.user_id)
	items = session.query(CatalogItem).filter_by(catalog=catalog).all()
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicsinglecatalog.html', items=items, catalog=catalog, catalogs=catalogs)
	else:
		return render_template('singlecatalog.html', items=items, catalog=catalog, catalogs=catalogs)

# Add new catagory
@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		try:
			catalog = session.query(Catalog).filter_by(name=request.form['name']).one()
			return render_template('erroraddcatalog.html', catalogs=catalogs, catalog=catalog)
		except:
			newCatalog = Catalog(name=request.form['name'], user_id=login_session['user_id'])
			session.add(newCatalog)
#		flash('Successfully add new catalog %s!' % newCatalog.name)
			session.commit()
			return redirect(url_for('showCatalogs'))
	else:
		return render_template('newcatalog.html', catalogs=catalogs)

# Edit a catalog
@app.route('/catalog/<string:catalog_name>/edit/', methods=['GET', 'POST'])
def editCatalog(catalog_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	editedCatalog = session.query(Catalog).filter_by(name=catalog_name).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedCatalog.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this catalog. Please create your own catlog in order to edit.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		if request.form['name']:
			try:
				catalog = session.query(Catalog).filter_by(name=request.form['name']).one()
				return render_template('erroreditcatalog.html', catalogs=catalogs, catalog=editedCatalog)
			except:
				editedCatalog.name = request.form['name']
#				flash('Catalog Successfully Edited %s' % editedCatalog.name)
				return redirect(url_for('showCatalogs'))
	else:
		return render_template('editCatalog.html', catalog=editedCatalog, catalogs=catalogs)

# Delete a catalog
@app.route('/catalog/<string:catalog_name>/delete/', methods=['GET', 'POST'])
def deleteCatalog(catalog_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	catalogToDelete = session.query(Catalog).filter_by(name=catalog_name).one()
	if 'username' not in login_session:
		return redirect('/login')
	if catalogToDelete.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this catalog. Please create your own catalog in order to delete.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(catalogToDelete)
#		flash('%s Successfully Deleted' % restaurantToDelete.name)
		session.commit()
		return redirect(url_for('showCatalogs'))
	else:
		return render_template('deleteCatalog.html', catalog=catalogToDelete, catalogs=catalogs)

# Show a single item in the catalog
@app.route('/catalog/<string:catalog_name>/<string:item_name>')
def showItem(catalog_name, item_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
#	catalog_id = session.query(Catalog).filter_by(name=catalog_name).one().id
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
#	item = session.query(CatalogItem).filter_by(id=catalog_id).one()
	creator = getUserInfo(catalog.user_id)
	item = session.query(CatalogItem).filter_by(catalog=catalog, name=item_name).one()
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicitem.html', item=item, catalog=catalog, catalogs=catalogs)
	else:
		return render_template('item.html', item=item, catalog=catalog, catalogs=catalogs)

# Create a new item in the catalog
@app.route('/catalog/<string:catalog_name>/item/new/', methods=['GET', 'POST'])
def newItem(catalog_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	if 'username' not in login_session:
		return redirect('/login')
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	if login_session['user_id'] != catalog.user_id:
		return "<script>function myFunction() {alert('You are not authorized to add menu items to this catalog. Please create your own catalog in order to add items.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		try:
			item = session.query(CatalogItem).filter_by(catalog=catalog, name=request.form['name']).one()
			return render_template('erroradditem.html', catalogs=catalogs, catalog=catalog, item=item)
		except:
			newItem = CatalogItem(name=request.form['name'], description=request.form['description'],
				catalog=catalog, user=catalog.user)
			session.add(newItem)
			session.commit()
#			flash('New Menu %s Item Successfully Created' % (newItem.name))
			return redirect(url_for('showSingleCatalog', catalog_name=catalog.name))
	else:
		return render_template('newitem.html', catalog=catalog, catalogs=catalogs)

# Edit an item
@app.route('/catalog/<string:catalog_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def editItem(catalog_name, item_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	if 'username' not in login_session:
		return redirect('/login')
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	editedItem = session.query(CatalogItem).filter_by(name=item_name, catalog=catalog).one()
	if login_session['user_id'] != catalog.user_id:
		return "<script>function myFunction() {alert('You are not authorized to edit items to this catalog. Please create your own catalog in order to edit items.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		try:
			item = session.query(CatalogItem).filter_by(catalog=catalog, name=request.form['name']).one()
			return render_template('erroredititem.html', catalogs=catalogs, catalog=catalog, item=item, editedItem=editedItem)
		except:
			if request.form['name']:
				editedItem.name = request.form['name']
			if request.form['description']:
				editedItem.description = request.form['description']
			session.add(editedItem)
			session.commit()
#			flash('Menu Item Successfully Edited')
			return redirect(url_for('showItem', catalog_name=catalog.name, item_name=editedItem.name))
	else:
		return render_template('edititem.html', catalog=catalog, item=editedItem, catalogs=catalogs)

# Delete an item
@app.route('/catalog/<string:catalog_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def deleteItem(catalog_name, item_name):
	catalogs = session.query(Catalog).order_by(asc(Catalog.name))
	if 'username' not in login_session:
		return redirect('/login')
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	itemToDelete = session.query(CatalogItem).filter_by(name=item_name).one()
	if login_session['user_id'] != catalog.user_id:
		return "<script>function myFunction() {alert('You are not authorized to delete items to this catalog. Please create your own catalog in order to delete items.');}</script><body onload='myFunction()''>"
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
#		flash('Menu Item Successfully Deleted')
		return redirect(url_for('showSingleCatalog', catalog_name=catalog.name))
	else:
		return render_template('deleteitem.html', item=itemToDelete, catalog=catalog, catalogs=catalogs)

### JSON APIs to view catalog ###
@app.route('/catalog/JSON')
def catalogJSON():
	catalogs = session.query(Catalog).all()
	return jsonify(catalogs=[r.serialize for r in catalogs])

@app.route('/catalog/<string:catalog_name>/item/JSON')
def singleCatalogJSON(catalog_name):
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	items = session.query(CatalogItem).filter_by(catalog=catalog).all()
	return jsonify(CatalogItems=[i.serialize for i in items])

@app.route('/catalog/<string:catalog_name>/<string:item_name>/JSON')
def itemJSON(catalog_name, item_name):
	catalog = session.query(Catalog).filter_by(name=catalog_name).one()
	item = session.query(CatalogItem).filter_by(catalog=catalog, name=item_name).one()
	return jsonify(CatalogItem=item.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=8000)