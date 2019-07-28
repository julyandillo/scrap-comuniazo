import pymysql


class Mysql:

    __conexion = None
    __cursor = None

    @classmethod
    def conectar(cls):
        if cls.__conexion is None:
            cls.__conexion = pymysql.connect(host='localhost',
                                           user='liga1819',
                                           passwd='liga1819',
                                           db='liga1819',
                                           charset='utf8',
                                           autocommit=True,
                                           cursorclass=pymysql.cursors.DictCursor)

            cls.__cursor = cls.__conexion.cursor()

        return cls.__cursor

    @classmethod
    def cerrar(cls):
        if cls.__cursor is not None:
            cls.__cursor.close()
