from evento import Evento


class Tarjeta(Evento):
    def __init__(self, jugador, minuto, tipo):
        super(Tarjeta, self).__init__()
        self.settipo(tipo)
        self.setjugador(jugador)
        self.setminuto(minuto)

        self.url = "api/tarjeta"
        
    def __str__(self):
        return "Tarjeta:" + super(Tarjeta, self).__str__()

    def settipo(self, tipo):
        if tipo == 'amarilla':
            self.modelo['tipo'] = 1
        else:
            self.modelo['tipo'] = 2

    @property
    def dict(self):
        """ devuelve la tarjeta como diccionario """
        tarjeta = {
            "minuto": self.get_minuto(),
            "jugador": self.get_jugador(),
            "tipo": self.modelo['tipo']
        }

        return tarjeta
