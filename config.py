class Config:
    pass

class DevelopmentConfig(Config):#Permite que el servido no se tenga que reiniciar
    DEBUG=True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}