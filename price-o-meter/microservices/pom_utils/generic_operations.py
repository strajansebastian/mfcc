# this functions are wrappers that will write operations to other tables in order to control concurrency and locking problems
import psycopg2

hostname = 'localhost'
username = 'price_o_meter'
# haha password in plain text - need to provide some sort of configuration to avoid this shit
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
    status = False
    affected_row_no = 0

    connection = init_connection()
    cursor = connection.cursor()
    print query, bind_variables
    try:
      cursor.execute(query, bind_variables)
      affected_row_no = cursor.rowcount
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    connection.close()

    return (status, affected_row_no)

def insert(query, bind_variables):
    status = False
    affected_row_no = 0

    connection = init_connection()
    cursor = connection.cursor()
    try:
      cursor.execute(query, bind_variables)
      affected_row_no = cursor.rowcount
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    connection.close()

    return (status, affected_row_no)

def delete(query, bind_variables):
    status = False
    affected_row_no = 0

    connection = init_connection()
    cursor = connection.cursor()
    try:
      cursor.execute(query, bind_variables)
      affected_row_no = cursor.rowcount
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    connection.close()

    return (status, affected_row_no)

