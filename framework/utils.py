from typing import Any
from urllib.parse import unquote
from datetime import datetime
import os


def parse_request_params(params):
    data = {}
    if params:
        for param in unquote(params).split("&"):
            key, value = param.split("=")
            data[key] = value
    return data

class BaseLogger(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}
    
    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs[name]

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]
        
class Logger(metaclass=BaseLogger):
        def __init__(self, name):
            self.name = name
            if not os.path.exists("./log_files/{self.name}.log"):
                os.makedirs("./log_files/{self.name}.log")
        
        def log(self, message):
            with open(f"./log_files/{self.name}.log", "a+", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] : {message}\n")


if __name__ == "__main__":
    print(parse_request_params("key=value&spam=eggs"))
    print(parse_request_params(""))
    logger = Logger(f"{__name__}")
    logger.log("Oki")