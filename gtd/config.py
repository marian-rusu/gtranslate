from os import getenv


class Config:
    QUERIES_PER_SEC = int(getenv('QUERIES_PER_SEC', 5))
    RPYC_PORT = int(getenv('RYPC_PORT', 19961))

