from flask import Flask, render_template#librerias a usar
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf=CSRFProtect()#Seguridad para que otra pagina no pueda mandara valores por nuestros formularios

#CSRF Cross-Site Request Foregery):solicitud de falsificacion entre sitios
#<input type="hiden" name="csrf_token" value="{{csrf_token()}}"---Esto se pone adentro del formulario
#que se utilice aqui, para la seguridad
@app.route('/')
def home():
    return render_template('home.html')#N-Gramas: Representación y Clasificación  

@app.route('/about')
def about():
    return render_template('about.html')#acerca de

@app.route('/entle')
def entle():
    return render_template('entle.html')#Entrada y caracteristica

@app.route('/est')
def est():
    return render_template('est.html')#Estadistica

@app.route('/mues')
def mues():
    return render_template('mues.html')#Muestreo

def pagina_no_encontrada(error):
    return render_template('errores/404.html'),404#Manejador de error

def inicializar_app(config):#iInicia la app
    app.config.from_object(config)
    csrf.init_app(app)#Configuracion para CSRF
    app.register_error_handler(404, pagina_no_encontrada)
    return app  