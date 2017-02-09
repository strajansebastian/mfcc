# this functions are wrappers that will write operations to other tables in order to control concurrency and locking problems
import psycopg2


hostname = 'localhost'
username = 'price_o_meter'
password = 'use_FUAR-10Cl'
database = 'price_o_meter'

def init_connection():
    connection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

    return connection 

def select(query):
    connection = init_connection()
    cursor = connection.cursor()
    cursor.execute(query)
   
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    result = []
    for row in rows:
      tmp_row = dict(zip(columns, row))
      result.append(tmp_row)

    cursor.close()
    connection.close()

    return result

def update(query, bind_variables):
    connection = init_connection()
    cursor = connection.cursor()
    try:
      cursor.execute(query, bind_variables)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)
      status = False

    connection.close()

    return status

def insert(query, bind_variables):
    connection = init_connection()
    cursor = connection.cursor()
    try:
      cursor.execute(query, bind_variables)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)
      status = False

    connection.close()

    return status

def delete(query, bind_variables):
    connection = init_connection()
    cursor = connection.cursor()
    try:
      cursor.execute(query, bind_variables)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)
      status = False

    connection.close()

    return status

