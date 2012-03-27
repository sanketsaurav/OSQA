import logging
from forum.base import get_database_engine
database_type = get_database_engine()

NAME = 'Mysql Full Text Search'
DESCRIPTION = "Enables Mysql full text search functionality."

try:
    import MySQLdb
    import settings_local
    CAN_USE = 'mysql' in database_type
except ImportError:
    logging.warning('Disabling MySQL Full Text Search module. MySQLdb not available')
    CAN_USE = False
except Exception, e:
    logging.exception('Error while processing MySQL FT imports', e)
    CAN_USE = False
