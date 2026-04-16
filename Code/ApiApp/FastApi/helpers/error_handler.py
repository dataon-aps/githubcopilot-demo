import sqlite3
import logging
from functools import wraps
from fastapi import HTTPException, status


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except sqlite3.OperationalError as e:
            logging.error("[%s] SQLite operational error: %s", func.__name__, e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database error, please retry shortly.",
            )
        except sqlite3.IntegrityError as e:
            logging.error("[%s] SQLite integrity error: %s", func.__name__, e)
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Data conflict — the record may already exist.",
            )
        except sqlite3.Error as e:
            logging.error("[%s] SQLite error: %s", func.__name__, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected database error occurred.",
            )
        except HTTPException:
            raise
        except Exception as e:
            logging.error("[%s] Unhandled error: %s", func.__name__, e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred.",
            )
    return wrapper
