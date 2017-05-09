from string import Template
from flask import Blueprint, request, render_template

from models import Hospital


mod_geo = Blueprint('geo', __name__, url_prefix='/geo')

mapadict = {'Htal. Italiano': '-34.9361913,-57.9738275',
            'Htal. Espanol': '-34.9055514,-57.9694866',
            'IPENSA': '-34.917127,-57.9413647',
            'Htal. San Martin': '-34.9232868,-57.9257116',
            'Mapa': '0,0'}


STATIC_MAP_TEMPLATE = Template("""<img src="https://maps.googleapis.com/maps/api/staticmap?size=700x300&markers=${place_name}" alt="map of ${place_name}">""")
STREET_VIEW_TEMPLATE = Template("""<img src="https://maps.googleapis.com/maps/api/streetview?size=700x300&location=${place_name}" alt="street view of ${place_name}">""")


@mod_geo.route('/')
def ciudad_page():
    place = Hospital('Mapa' ,mapadict['Mapa'])
    return render_template('ciudad.html', place=place)


@mod_geo.route("/ciudad" , methods=['GET', 'POST'])
def ciudad():
    seleccion = request.form.get('comp_select')

    place = Hospital(seleccion, mapadict[seleccion])

    if request.method == 'POST':
        return render_template('ciudad.html', place=place)
    else:
        place = Hospital('Mapa', mapadict['Mapa'])
        return render_template('ciudad.html', place=place)


@mod_geo.route('/laplata')
def laplata_page():
    return("""<h1>La Plata</h1>""" +
            STATIC_MAP_TEMPLATE.substitute(place_name="la_plata") +
            STREET_VIEW_TEMPLATE.substitute(place_name="la_plata"))

@mod_geo.route('/estudiantes')
def estudiantes_page():
    return("""<h1>Estadio Unico</h1>""" +
            STATIC_MAP_TEMPLATE.substitute(place_name="estadio_unico") +
            STREET_VIEW_TEMPLATE.substitute(place_name="estadio_unico"))

@mod_geo.route('/gimnasia')
def gimnasia_page():
    return("""<h1>Estadio Gimnasia</h1>""" +
            STATIC_MAP_TEMPLATE.substitute(place_name="estadio_gimnasia") +
            STREET_VIEW_TEMPLATE.substitute(place_name="estadio_gimnasia") +
            """<p><a class="btn btn-lg btn-primary btn-block submitbutton" href="/" role="button" >Volver</a></p>""")