from objeto import Objeto


class Evento(Objeto):
    def setjugador(self, jugador):
        self.modelo['jugador'] = jugador

    def setminuto(self, minuto):
        self.modelo['minuto'] = minuto

    def set_partido(self, id_partido):
        self.modelo['partido'] = id_partido

    def get_minuto(self):
        return self.modelo['minuto']

    def get_jugador(self):
        return self.modelo['jugador']
