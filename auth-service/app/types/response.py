class Response:

    def __init__(self, sucess: bool, body: str, status_code: int):
        self.success = sucess
        self.body = body
        self.status_code = status_code
        super().__init__()

