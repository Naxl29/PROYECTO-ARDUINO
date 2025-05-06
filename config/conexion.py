from flaskext.mysql import MySQL # Se importa la extención MySQL para manejar bases de datos

mysql = MySQL() # Se utiliza la libreria MySQL de flaskext

def init_mysql(app):
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = 'blockchain'
    mysql.init_app(app)

__all__ = ['mysql', 'init_mysql']