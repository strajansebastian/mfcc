# this functions are wrappers that will write operations to other tables in order to control concurrency and locking problems
import psycopg2
import time
import datetime
import re

import random

hostname = 'localhost'
username = 'price_o_meter'
# haha password in plain text - need to provide some sort of configuration to avoid this shit
password = 'use_FUAR-10Cl'
database = 'price_o_meter'

def init_connection():
    connection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

    return connection

def scheduler():
    connection = init_connection()
    query_locks = "SELECT * FROM transhadow_locks"
    query_next_transactions_in_queue = "INSERT INTO transhadow_locks(transaction_id, transaction_query, locked_table, lock_type) SELECT transaction_id, transaction_query, locked_table, lock_request_type FROM transhadow_lock_requests WHERE transaction_status != 'finished' AND transaction_time IN (SELECT MIN(transaction_time) FROM transhadow_lock_requests WHERE transaction_status != 'finished')"
    query_next_transactions_in_queue_update_selected = "UPDATE transhadow_lock_requests SET transaction_status = 'processing' WHERE transaction_id IN (SELECT transaction_id FROM transhadow_locks)"
    
    # check if there are entries in transhadow_locks
    # if yes then wait
    # if no then take most old transactions based on the transaction_time and add them into the transhadow_locks (change state transaction_status to processing)
    while True:
        cursor = connection.cursor()
        cursor.execute(query_locks)
        rows = cursor.fetchall()
        if len(rows) > 0:
            # wait for transactions to process
            # check if there is a lock
            print datetime.datetime.now(), "Checking if there are some sheduling problems (deadlock?)"
            time.sleep(1)

            # check here if deadlock is present

        else:
            # no active locks - get next round of transactions
            cursor.execute(query_locks)
            cursor.execute(query_next_transactions_in_queue)
            cursor.execute(query_next_transactions_in_queue_update_selected)
            if (cursor.rowcount > 0):
                print datetime.datetime.now(), "No active transactions found! Getting next (%s) transaction batch!" % (cursor.rowcount)

            connection.commit()
    
        cursor.close()

    connection.close()

    return True

def add_transaction(connection, table, request_type, transaction_query, transaction_status='queued', transaction_state='begin'):
    status = False
    transaction_id = -1

    query = "INSERT into transhadow_lock_requests(transaction_time, transaction_status, transaction_state, transaction_query, locked_table, lock_request_type) VALUES (now(), %s, %s, %s, %s, %s); SELECT currval('transhadow_lock_requests_transaction_id_seq'); "

    cursor = connection.cursor()
    
    try:
      cursor.execute(query, (transaction_status, transaction_state, transaction_query, table, request_type,))
      rows = cursor.fetchall()
      transaction_id = rows[0]
      # print transaction_id
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)
    
    return (status, transaction_id)

def check_transaction_status(connection, transaction_id):
    # return status
    #- if status is queued then the process will wait
    #- if status is processing then the query will move on
    #- if status is finished then eveything is fine
    status = "none"
    query = "SELECT transaction_status FROM transhadow_lock_requests WHERE transaction_id = %s"

    while status != "processing":
        cursor = connection.cursor()
        cursor.execute(query, (transaction_id,))
        rows = cursor.fetchall()
        status = rows[0][0]
        # print "check_transaction_status %s rows %s: " % (status, rows)
        connection.commit()
        cursor.close()
    
    return status

def finish_transaction(connection, transaction_id):
    # move transaction to finish state
    # MAY NEED TO REMOVE LOCKS from transhadow_locks TOO - at this step in order for the scheduler to be able to continue
    status = False
    query_change_status = "UPDATE transhadow_lock_requests SET transaction_status = 'finished' WHERE transaction_id = %s"
    query_clean_lock = "DELETE FROM transhadow_locks WHERE transaction_id = %s"
    
    cursor = connection.cursor()
    try:
      cursor.execute(query_change_status, (transaction_id,))
      cursor.execute(query_clean_lock, (transaction_id,))
      cursor.close()
      connection.commit()
      status = True
    except Exception as e:
      print str(e)

    return status

def clean_backup_table(connection, table_name):
    status = False
    query = "DELETE FROM transhadow_%s" % (table_name)
    
    print "run %s" % (query)
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    return status


def backup_table(connection, table_name):
    status = False
    print "start backup_table %s" % (table_name)

    clean_backup_table(connection, table_name)

    query = "INSERT INTO transhadow_%s SELECT * from %s" % (table_name, table_name)
    
    cursor = connection.cursor()
    try:
      cursor.execute(query)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    print "end backup_table %s" % (table_name)

    return status

def rollback_table(connection, table_name):
    status = False

    query_clean_origin = "DELETE FROM %s" % (table_name)
    query_bring_backup = "INSERT INTO %s SELECT * from transhadow_%s" % (table_name, table_name)
    
    print "Rollback in making:"
    cursor = connection.cursor()
    try:
      cursor.execute(query_clean_origin)
      cursor.execute(query_bring_backup)
      cursor.close()
      connection.commit()
      status = True
    except Exception as e: 
      print str(e)

    return status

def get_table_name(query, query_type):
    table_name = 'none'
    
    if query_type == "SELECT":
       table_name = "invalid_select_tab"
       m = re.search('FROM ([a-zA-Z0-9_]+)(\s*$|\s+)', query)
       if m:
           table_name = m.group(1)
    elif query_type == "UPDATE":
       table_name = "invalid_update_tab"
       m = re.search('UPDATE ([a-zA-Z0-9_]+)\s+', query)
       if m:
           table_name = m.group(1)
    elif query_type == "INSERT":
       table_name = "invalid_insert_tab"
       m = re.search('INSERT INTO ([a-zA-Z0-9_]+)', query)
       if m:
           table_name = m.group(1)
    elif query_type == "DELETE":
       table_name = "invalid_delete_tab"
       m = re.search('DELETE FROM ([a-zA-Z0-9_]+)(\s*$|\s+)', query)
       if m:
           table_name = m.group(1)

    return table_name

def select(query):
    table_name = get_table_name(query, "SELECT")
    affected_row_no = 0
    connection = init_connection()
    cursor = connection.cursor()

    (transtat, transid) = add_transaction(connection, table_name, 'read', query, 'queued', 'begin')
    transtat = check_transaction_status(connection, transid)

    cursor.execute(query)
    affected_row_no = cursor.rowcount
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    result = []
    for row in rows:
      tmp_row = dict(zip(columns, row))
      result.append(tmp_row)

    cursor.close()
    finish_transaction(connection, transid)
    
    connection.close()

    return result

def update(query, bind_variables):
    table_name = get_table_name(query, "UPDATE")
    status = False
    affected_row_no = 0

    connection = init_connection()

    (transtat, transid) = add_transaction(connection, table_name, 'write', query, 'queued', 'begin')
    transtat = check_transaction_status(connection, transid)
  
    if transtat == 'processing':
        try:
          backup_table(connection, table_name)
          
          try: 
            cursor = connection.cursor()
            cursor.execute(query, bind_variables)
            affected_row_no = cursor.rowcount
            cursor.close()
            if random.randint(0,4) == 0:
              raise Exception('random query update fail', 'haha redo operation')
          except Exception as e: 
            print "Rollback needs to be done!", str(e)
            if (affected_row_no > 0):
              # rollback is needed
              rollback_table(connection, table_name)
              affected_row_no = -999

          connection.commit()
          status = True
        except Exception as e: 
          print str(e)
    else:
        # scheduler failed?
        print "Schedule failed (%s) for trans id (%s)" % (transtat, transid)

    finish_transaction(connection, transid)

    connection.close()

    return (status, affected_row_no)

def insert(query, bind_variables):
    table_name = get_table_name(query, "INSERT")
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
    table_name = get_table_name(query, "DELETE")
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

