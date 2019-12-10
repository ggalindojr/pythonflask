import MySQLdb

host = 'localhost'
user = 'root'
password = '123456'
db = 'seubanco'
port = 3306

con = MySQLdb.connect(host, user, password, db, port)
c = con.cursor()

def select(fields, table, where=None):
    global c
    query = "SELECT " + fields + " FROM " + table
    if (where):
        query += "" + " WHERE " + where
    c.execute(query)
    return c.fetchall()

def insert(values, table, fields=None):
    global c, con
    query = "INSERT INTO " + table
    if (fields):
        query = query + " (" + fields + ") "
    query += "" + " VALUES " + "," .join(["(" + V + ")" for V in values])
    c.execute(query)
    con.commit()    
    
def update(sets, table, where=None):
    global c, con
    query = "UPDATE " + table
    query += "" + " SET " + "," .join([key + " = '" + value + "'" for key, value in sets.items()])
    if (where):
        query += "" + " WHERE " + where
    c.execute(query)
    con.commit()

def delete(table, where):
    global c, con
    query = "DELETE FROM " + table + " WHERE " + where
    c.execute(query)
    con.commit()
    # print(query)


""" values = [  #formato para inserir
    "DEFAULT, 'Benedita', 'Florida'",
    "DEFAULT, 'Aparecida', 'Bizantina'"
]
insert(values, "testedev") """

""" values = { "descricao":"Benedito", "descricao2":"Consultor" }  #formato para atualizar
update(values, "testedev", "idtestedev = 3") """

# delete("testedev", "idtestedev = 2")
# print(select('*', 'testedev'))