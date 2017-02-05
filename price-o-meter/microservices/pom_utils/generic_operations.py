# this functions are wrappers that will write operations to other tables in order to control concurrency and locking problems

def select(connection, query):
    print "A select was made"

def update(connection, query):
    print "A update was made"

def insert(connection, query):
    print "A insert was made"

def delete(connection, query):
    print "A delete was made"
