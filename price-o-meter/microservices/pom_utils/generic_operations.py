# this functions are wrappers that will write operations to other tables in order to control concurrency and locking problems

hostname = 'localhost'
username = 'price_o_meter'
password = 'use_FUAR-10Cl'
database = 'price_o_meter'

def select(connection, query):
    import psycopg2
    connection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
    cursor = connection.cursor()
    cursor.execute(query)
   
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    result = []
    for row in rows:
      tmp_row = dict(zip(columns, row))
      result.append(tmp_row)

    return result

def update(connection, query):
    print "A update was made"

def insert(connection, query):
    print "A insert was made"

def delete(connection, query):
    print "A delete was made"

### # Simple routine to run a query on a database and print the results:
### def doQuery( conn ) :
###     cur = conn.cursor()
### 
###     cur.execute( "SELECT fname, lname FROM employee" )
### 
###     for firstname, lastname in cur.fetchall() :
###         print firstname, lastname
### 
### 
### print "Using psycopg2"
### import psycopg2
### myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
### doQuery( myConnection )
### myConnection.close()
