from flask_script import Manager, Server
from app import inicializar_app#manda a llamar a la app
from config import config

configuracion=config['development']#Llama a congig
app = inicializar_app(configuracion)

manager=Manager(app)
manager.add_command('runserver',Server(host='127.0.0.1',port=5010))#Se puede realizar la configuracion del puerto

if __name__=='__main__': 
    manager.run() 