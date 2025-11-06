from src.core import database_client


get_db = database_client.get_db


__all__ = [
    'get_db',
]
