class Token:
    __token = None

    @classmethod
    def get_token(cls):
        if cls.__token is None:
            with open('token') as file:
                cls.__token = file.readline()

        return cls.__token
