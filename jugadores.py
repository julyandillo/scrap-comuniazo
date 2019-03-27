import pymysql as mysql


class Jugadores:
    __jugadores = {}

    @classmethod
    def load_jugadores(cls):
        bd = mysql.connect(host='localhost',
                           user='liga1819',
                           passwd='liga1819',
                           db='liga1819',
                           charset='utf8',
                           autocommit=True,
                           cursorclass=mysql.cursors.DictCursor)

        with bd.cursor() as sql:
            sql.execute("""select e.nombre as equipo, j.id, j.nombre
                            from jugador j
                            inner join equipo e ON e.id=j.id_equipo
                            order by e.nombre, j.nombre""")

            for fila in sql.fetchall():
                equipo = str(fila['equipo'])
                if equipo not in cls.__jugadores.keys():
                    """ 
                    si no existe el equipo como key del diccionario es crea una una key con una lista vacia para poder 
                    incorporar los jugadores despues
                    """
                    cls.__jugadores[equipo] = []

                cls.__jugadores[equipo].append({"nombre": str(fila['nombre']), "id": int(fila['id'])})

        bd.close()

    @classmethod
    def get_jugador(cls, nombre, equipo):
        if len(cls.__jugadores) == 0:
            Jugadores.load_jugadores()
            # print("Jugadores cargados ({})".format(len(cls.__jugadores)))

        for jugador in cls.__jugadores[equipo]:
            if nombre == jugador['nombre']:
                # print("{} {} {}".format(equipo, nombre, jugador['id']))
                return jugador['id']

        return None

    @classmethod
    def get_jugadores(cls, equipo):
        if len(cls.__jugadores) == 0:
            Jugadores.load_jugadores()

        return cls.__jugadores[equipo]

    @classmethod
    def reemplazar(cls, id_jugador, nombre_nuevo):
        """ reemplaza el nombre del jugador parseado por el que esta almacenado en la bbdd"""
        bd = mysql.connect(host='localhost',
                           user='liga1819',
                           passwd='liga1819',
                           db='liga1819',
                           charset='utf8',
                           autocommit=True,
                           cursorclass=mysql.cursors.DictCursor)

        with bd.cursor() as sql:
            sql.execute("UPDATE jugador SET nombre=%s WHERE id=%s", (nombre_nuevo, id_jugador))
        bd.close()

        cls.__jugadores.clear()
        Jugadores.load_jugadores()

    @classmethod
    def nuevo(cls, equipo, nombre, posicion, dorsal, nacionalidad, pais_nacimiento, fecha_nacimiento):
        """ inserta un nuevo jugador que no existe en la bbdd """

        bd = mysql.connect(host='localhost',
                           user='liga1819',
                           passwd='liga1819',
                           db='liga1819',
                           charset='utf8',
                           autocommit=True,
                           cursorclass=mysql.cursors.DictCursor)
        # id_jugador = 0

        with bd.cursor() as sql:
            sql.execute("SELECT id FROM equipo WHERE nombre='{}'".format(equipo))
            id_equipo = sql.fetchone()
            sql.execute("""INSERT INTO jugador (nombre, id_equipo, posicion, nacionalidad, pais_nacimiento, 
                          fecha_nacimiento, dorsal, imagen) VALUES ('{}', {}, '{}', '{}', '{}', '{}', {}, '')""".format(
                nombre, str(id_equipo['id']), posicion, nacionalidad, pais_nacimiento, fecha_nacimiento, dorsal
            ))

            sql.execute("SELECT id FROM jugador ORDER BY id DESC LIMIT 1")
            id_nuevo = sql.fetchone()
            id_jugador = id_nuevo['id']
        bd.close()

        cls.__jugadores.clear()
        cls.load_jugadores()

        return id_jugador

