# coding: utf-8
import os
from flask import Flask, Markup, request, render_template, redirect, json, url_for, jsonify, Response
from sighting import Sighting
app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
static = os.path.join(SITE_ROOT, 'static')
app.config['static'] = static

@app.route("/home/", methods=['POST','GET'])
def home():
	if request.method == 'POST':
		searched = False
		if request.form['name'] != '':
			results=[]
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			name = request.form['name']
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			print image
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			urltype = "year"
			
			for sighting in data["sightings"]:
				name1 = sighting["name"]
				country = sighting["country"]

				if name.upper() == name1.upper():
					searched = True
					results.append(sighting)

				if sighting["year"] ==name:
					searched = True
					results.append(sighting)

				if country.upper() == name.upper():
					searched = True
					results.append(sighting)
	


			if searched == True:
				return  render_template('template5.html', results = results, csssheet = url, image = image)



			if searched == False:
				title = "I'm sorry we couldn't find that"
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist then add it using our new upload feature!'

			return render_template('template2.html', title = title, result = result, csssheet = url, image = image)


				

	#This will redirect the user to the page that matches their search. This redirects to their input	

	else:

		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
	

		return render_template('templateex.html', csssheet = url, image = image)

#this allows the user to report their own sighting. They also have the option of adding an image.
@app.route("/upload/",methods=['POST','GET'])
def upload():

	if request.method == 'POST':
		Ysearch = False
		Csearch = False
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		if 'datafile' not in request.files:
			img = ''
		else:
			f = request.files['datafile']
			fname = f.filename
			f.save(os.path.join(app.config['static'], fname))	
			img = url_for('static',filename = fname)	
		name = request.form['uplName']
		year = request.form['uplYear']
		country = request.form['uplCountry']
		description = request.form['uplDescription']
		sighting = {'name':name, 'year':year, 'country':country, 'description':description, 'img':img}
		with open(json_url) as f:
			data = json.load(f)
			data["sightings"].append(sighting)
			for dYear in data["years"]:
				if dYear == year:
					Ysearch = True
			for dCountry in data["countries"]:
				if dCountry == country:
					Csearch = True

			if Ysearch == False:
				data["years"].append(year)
			if Csearch == False:
				data["countries"].append(country)


		with open(json_url, 'w') as f:
    			json.dump(data, f)


		return redirect("/all/")

	else:
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')


		return render_template('uplTemplate.html', csssheet = url, image = image)









#stacking the routes makes them the same
#this shows all years in which there are reported ufo sightings
@app.route("/year/")
@app.route("/Year/")
def Year():
	searched = False
	results = []
	year = request.args.get('year', '')
	if year == '':
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
	
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		title = "All years with reported ufo sightings"
		return render_template('template3.html', results = data["years"], title = title, csssheet = url, image = image)
	else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			for sighting in data["sightings"]:
				if sighting["year"] == year:
					searched = True
					results.append(sighting)
			if searched == True:

				return  render_template('template5.html', results = results, csssheet = url, image = image)


			if searched == False:
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist, try adding it to our database using our new upload feature!'

			return render_template('template2.html', title = result, csssheet = url, image = image)


#this shows all countries in which ufo sightings have happened
@app.route("/country/")
@app.route("/Country/")
def Country():
	searched = False
	results = []
	country = request.args.get('country', '')
	if country == '':
	
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "static", "everything.json")
		url = url_for('static',filename='csstest.css')
		image = url_for('static',filename='logo1.png')
	
		ro = open(json_url, "r")
		data = json.loads(ro.read())
		title = "All Countries with reported ufo sightings"

		return render_template('template6.html', results = data["countries"],title = title, csssheet = url, image = image)
	else:
			SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
			json_url = os.path.join(SITE_ROOT, "static", "everything.json")
			url = url_for('static',filename='csstest.css')
			image = url_for('static',filename='logo1.png')
			ro = open(json_url, "r")
			data = json.loads(ro.read())
			for sighting in data["sightings"]:
				if sighting["country"] == country:
					searched = True
					results.append(sighting)
			if searched == True:

				return  render_template('template5.html', results = results, csssheet = url, image = image)


			if searched == False:
				result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist then add it using our new upload feature!'

			return render_template('template2.html', title = result, csssheet = url, image = image)




@app.route("/all/")
@app.route("/All/")
def All():
#This lists all sightings saved in the directory
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "everything.json")
	url = url_for('static',filename='csstest.css')
	image = url_for('static',filename='logo1.png')
	ro = open(json_url, "r")
	data = json.loads(ro.read())
	results = data["sightings"]
	return  render_template('template5.html', results = results, csssheet = url, image = image)




#if a page is not found a friendly error message will appear
@app.errorhandler(404)
def page_not_found(error): 
	
	url = url_for('static',filename='csstest.css')
	image = url_for('static',filename='logo1.png')
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static", "everything.json")
	
	ro = open(json_url, "r")
	data = json.loads(ro.read())
	title = "I'm sorry we couldn't find that"
	result = 'The page you requested does not exist. If you are having trouble finding things, try navigating using the alien head. If you think it should exist then add it using our new upload feature!'

	return render_template('template2.html', title = title, result = result, csssheet = url, image = image)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
