from src.core import database_client


get_db = database_client.get_session


__all__ = [
    'get_db',
]
