class EmployeerRepository:
    _employeers = [
        {
            "id": 1,
            "username": "employeer",
            "email": "email@gmail.com",
            "password": "123",
            "role": "employer"
        }
    ]
    _next_id = 2

    @classmethod
    def create(cls, data):
        employeer = {
            "id": cls._next_id,
            "username": data.get("username"),
            "email": data.get("email"),
            "password": data.get("password"),
            "role": "employer"
        }
        cls._employeers.append(employeer)
        cls._next_id += 1
        return employeer

    @classmethod
    def list_all(cls):
        return cls._employeers

    @classmethod
    def find_by_id(cls, employeer_id):
        return next((employeer for employeer in cls._employeers if employeer['id'] == employeer_id), None)

    @classmethod
    def authenticate(cls, email, password):
        """
        Procura um empregado pelo e-mail e senha correspondentes.
        Devolve o dicionário do usuário se encontrar, ou None caso contrário.
        """
        for employeer in cls._employeers:
            if employeer.get("email") == email and employeer.get("password") == password:
                return employeer
        return None

    @classmethod
    def update(cls, employeer_id, new_data):
        employeer = cls.find_by_id(employeer_id)
        if employeer:
            if "username" in new_data: employeer["username"] = new_data["username"]
            if "email" in new_data: employeer["email"] = new_data["email"]
            if "password" in new_data: employeer["password"] = new_data["password"]
            return employeer
        return None

    @classmethod
    def delete(cls, employeer_id):
        employeer = cls.find_by_id(employeer_id)
        if employeer:
            cls._employeers.remove(employeer)
            return True
        return False