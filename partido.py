from objeto import Objeto


class Partido(Objeto):
    def __init__(self, local, visitante, goleslocal, golesvisitante, jornada):
        super().__init__()

        self.url = "http://localhost:8000/guardarpartido"
        self.modelo['local'] = local
        self.modelo['visitante'] = visitante
        self.modelo['golesLocal'] = goleslocal
        self.modelo['golesVisitante'] = golesvisitante
        self.modelo['jornada'] = jornada
        self.goles = []
        self.tarjetas = []

    def __str__(self):
        return "Partido\n" + super(Partido, self).__str__()

    def addgol(self, gol):
        self.goles.append(gol)

    def addtarjeta(self, tarjeta):
        self.tarjetas.append(tarjeta)

    def guardar(self):
        self.modelo['goles'] = [gol.dict for gol in self.goles]

        self.modelo['tarjetas'] = [tarjeta.dict for tarjeta in self.tarjetas]

        super(Partido, self).guardar()

    def vistaprevia(self):
        print("{local} {gl} - {gv} {visitante}".format(local=self.modelo['local'], visitante=self.modelo['visitante'],
                                                       gl=self.modelo['golesLocal'], gv=self.modelo['golesVisitante']))
        for gol in self.goles:
            print(gol)
        for tarjeta in self.tarjetas:
            print(tarjeta)

        print("---------------------------------------------------------")
