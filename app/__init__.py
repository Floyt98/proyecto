from flask import Flask, render_template#librerias a usar

app = Flask(__name__)

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
    app.register_error_handler(404, pagina_no_encontrada)
    return app  