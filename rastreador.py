from partido import Partido
from gol import Gol
from tarjeta import Tarjeta
from jugadores import Jugadores

import urllib.request
from pyquery import PyQuery


class Rastreador(object):
    url_calendario = "https://www.comuniazo.com/laliga/calendario"

    @classmethod
    def rastreajornada(cls, jornada):
        request = urllib.request.Request(cls.url_calendario, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})

        html = PyQuery(urllib.request.urlopen(request).read().decode('utf-8'))
        jornada = html('.box-gameweek').eq(jornada-1)
        partidos = []

        for partido in jornada('ul').children('li'):
            contenido = PyQuery(partido)
            partidos.append(contenido('a').attr('href'))

        return partidos

    @staticmethod
    def rastreapartido(url):
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})

        html = PyQuery(urllib.request.urlopen(request).read().decode('utf-8'))

        local = html('.home').text()
        visitante = html('.away').text()
        goles_local = html('.score>span:first').text()
        goles_visitante = html('.score>span:last').text()

        jornada = html('.mid>.info').text()
        njornada = jornada[:jornada.find("\n")]

        partido = Partido(local, visitante, goles_local, goles_visitante, njornada)

        equipos = {"local": local, "visitante": visitante}
        equipo_actual = "local"  # la primera iteracion parsea la parte de la izqda, el equipo local
        print("Rastreando {local} - {visitante}".format(local=local, visitante=visitante))

        for equipo in html('.player-list').children('ul'):
            for item in PyQuery(equipo).children('li'):
                jugador = PyQuery(item)

                if jugador('.events') is not None:
                    for eventoHtml in jugador('.events').children('i'):
                        evento = PyQuery(eventoHtml)

                        if evento.has_class('icon-circle') or evento.has_class('icon-up-circled') \
                                or evento.has_class('icon-stop') or evento.has_class('icon-half-square'):
                            """ solo interesan los goles y las tarjetas, para los cambios y demas no se hace nada """
                            id_jugador = Jugadores.get_jugador(jugador('strong').text(), equipos[equipo_actual])

                            if id_jugador is None:
                                """
                                si no se encuentra en nombre que se saca de comuniazo en la bbdd, se busca el
                                equivalente y se reeemplaza para que siempre concuerde con el que viene de comuniazo
                                """
                                print("Jugador no relacionado: {}".format(jugador('strong').text()))
                                print("jugadores del {}:".format(equipos[equipo_actual]))
                                for posible in Jugadores.get_jugadores(equipos[equipo_actual]):
                                    print("{}: {}".format(posible['id'], posible['nombre']))

                                id_jugador = input("cual corresponde ({})?: ".format(jugador('strong').text()))
                                if int(id_jugador) > 0:
                                    """
                                    si se le pone el id_jugador -1, es que el jugador del evento ya no está en
                                    la liga, se pasará a la API sin id, solo contara el evento para las estadisticas no 
                                    quien es el protagonista
                                    """
                                    Jugadores.reemplazar(id_jugador, jugador('strong').text())
                                elif int(id_jugador) == 0:
                                    """
                                    se introduce un nuevo jugador si no se encuentra en la lista
                                    """
                                    print("Nuevo jugador:")
                                    print("\tnombre: {}".format(jugador('strong').text()))
                                    posicion = input("\tposicion: ")
                                    dorsal = int(input("\tdorsal: "))
                                    fecha_nacimiento = input("\tfecha nacimiento: ")
                                    nacionalidad = input("\tnacionalidad: ")
                                    pais = input("\tpais de nacimiento: ")

                                    id_jugador = Jugadores.nuevo(equipos[equipo_actual], jugador('strong').text(),
                                                                 posicion, dorsal, nacionalidad, pais, fecha_nacimiento)

                            if evento.has_class('icon-circle'):
                                """ gol """
                                texto = evento.attr('title')
                                propia_meta = "en pp" in texto
                                minuto = texto[texto.find('minuto')+7:]
                                partido.addgol(Gol(id_jugador, minuto, False, propia_meta))

                            elif evento.has_class('icon-up-circled'):
                                """ penalti """
                                texto = evento.attr('title').split(" ")
                                partido.addgol(Gol(id_jugador, texto[4], True, False))

                            elif evento.has_class('icon-stop'):
                                """ tarjeta amarilla o roja """
                                texto = evento.attr('title').split(" ")
                                partido.addtarjeta(Tarjeta(id_jugador, texto[3], texto[1].replace(',', '')))

                            elif evento.has_class('icon-half-square'):
                                """ segunda amarilla que implica una roja también """
                                texto = evento.attr('title').split(" ")
                                partido.addtarjeta(Tarjeta(id_jugador, texto[3], 'amarilla'))
                                partido.addtarjeta(Tarjeta(id_jugador, texto[3], 'roja'))

            """ la segunda vuelta del for pertenece a la parte de la dcha, al equipo visitante """
            equipo_actual = "visitante"

        return partido
