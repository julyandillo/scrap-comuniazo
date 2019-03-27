from evento import Evento


class Gol(Evento):
    def __init__(self, jugador, minuto, penalti=False, propia_meta=False):
        super(Gol, self).__init__()

        self.url = "url/gol"

        self.setjugador(jugador)
        self.setminuto(minuto)
        self.modelo['penalti'] = penalti
        self.modelo['propiaMeta'] = propia_meta

    def __str__(self):
        return "Gol:" + super(Gol, self).__str__()

    @property
    def dict(self):
        """ devuelve el gol como un diccionario """
        gol = {
            "minuto": self.get_minuto(),
            "jugador": self.get_jugador(),
            "penalti": self.modelo['penalti'],
            "propiaMeta": self.modelo['propiaMeta']
        }

        return gol
