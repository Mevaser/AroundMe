from flask import render_template, request, url_for
from flask_googlemaps import Map
from flask_mobility.decorators import mobile_template
from app import app

@app.route("/")
@mobile_template('{mobile/}get_location.html')
def home(template):
	return render_template(template)

@app.route('/favicon.<ext>')
def favicon(ext: str):
	return app.send_static_file(f'favicon.{ext}')

@app.route('/map')
def map():
	latitude = float(request.args.get('lat'))
	longitude = float(request.args.get('lng'))
	currLatitude = float(request.args.get('currLat'))
	currLongitude = float(request.args.get('currLng'))

	if not latitude or not longitude or not currLatitude or not currLongitude:
		return render_template("mobile/location_not_found.html")

	# The latitude must be a number between -90 and 90 and the longitude between -180 and 180.
	try:
		if int(latitude) < -90 or int(latitude) > 90 or \
			int(longitude) < -180 or int(longitude) > 180:
			raise ValueError

		if int(currLatitude) < -90 or int(currLatitude) > 90 or \
			int(currLongitude) < -180 or int(currLongitude) > 180:
			raise ValueError
	except ValueError:
		return render_template("mobile/location_not_found.html")


	# creating a map in the view
	mymap = Map(
		identifier="view-side",
		style=(
			"height:100%;"
			"width:100%;"
			"top:0;"
			"left:0;"
			"position:absolute;"
			"z-index:-1;"
		),
		lat=latitude,
		lng=longitude,
		zoom=16,
		zoom_control=True,
		language='he',
		maptype='ROADMAP',
		maptype_control=False,
		center_on_user_location=True,
		streetview_control=False,
		clickable=False,
		circles=[
			{
				"stroke_color": "#32a852",
				"fill_color": "#32a852",
				"fill_opacity": 0.1,
				"stroke_opacity": 1.0,
				"stroke_weight": 3,
				"center": {"lat": float(latitude), "lng": float(longitude)},
				"radius": 500,
				"clickable": False
			}],
		markers=[
			{
				'icon': url_for('static', filename="marker.png"),
				'lat': currLatitude,
				'lng': currLongitude,
				'infobox': "<h2><b style='color:green;'>המיקום הנוכחי</b></h2>"
			}]
	)
	if request.MOBILE:
		mymap.zoom = 14

	return render_template('map.html', mymap=mymap)

@app.errorhandler(404)
def not_found_error(_):
	return render_template('404.html'), 404
