import sys

from rastreador import Rastreador


def main():
    if len(sys.argv) != 3:
        print("Usa {script} jornada destino\nEj:\n\t{script} 1 API\n\t{script} 1 fichero".format(script=sys.argv[0]))
        sys.exit(1)

    jornada = Rastreador.rastreajornada(int(sys.argv[1]))
    # jornada = Rastreador.rastreajornada(1)

    partidos = [Rastreador.rastreapartido(enlace) for enlace in jornada]
    # partidos[3].guardar()

    if sys.argv[2] != "API":
        for partido in partidos:
            partido.vistaprevia()
    else:
        for partido in partidos:
            partido.guardar()


if __name__ == '__main__':
    main()
