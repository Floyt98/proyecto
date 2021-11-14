class Config:
    SECRET_KEY = 'KcNju88dc9H9FDH75'

class DevelopmentConfig(Config):#Permite que el servido no se tenga que reiniciar
    DEBUG=True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}