import contextlib
import mysql.connector
import config

@contextlib.contextmanager
def get_mysql_connection():

    """
    function to get a mysql database connection 

    Args:
        None

    Returns:
        mysql or SQLalchemy database connection  

    """
    

    mydb=mysql.connector.connect(
    host=config.host,
    user=config.username,
    password=config.password ,
    database=config.database

    )



    yield mydb


    mydb.close()


from sqlalchemy import create_engine
import pymysql


def get_alchemy_engine():
    """
        function to get a sql_alchemy db connection 

        Args:
            None

        Returns:
            SQLalchemy database connection 

         

    """



    db_connection_str = f'mysql+pymysql://{config.username}:{config.password}@{config.host}'
    return create_engine(db_connection_str)

    



    