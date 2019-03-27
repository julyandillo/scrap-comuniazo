from tokenjwt import Token

import json
import requests


class Objeto:
    def __init__(self):
        """ el modelo es un diccionario que se convertira en un json para pasarlo a la API y actualizar la info """
        self.modelo = {}
        self.url = ""

    def __str__(self):
        string = ""
        for key, valor in self.modelo.items():
            string += "\n\t{key}: {valor}".format(key=key, valor=valor)

        return string

    def guardar(self):
        """ se conecta a la API para poder guardar la informacion obtenida """
        # print(self.url)
        # print(json.dumps(self.modelo))
        headers = {
            'Authorization': 'Bearer ' + Token.get_token()
        }

        response = requests.post(self.url, headers=headers, json=self.modelo)
        # print(response.status_code)
        # print(response.text)
        data = response.json()

        print(data['message'])
