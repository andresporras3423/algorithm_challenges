import pyodbc

def get_con(n_test):
    server = 'DESKTOP-C4J7U97\SQLEXPRESS'
    database = 'math_challenges'
    conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=' + server + ';'
    'Database=' + database + ';'
    'Trusted_Connection=yes;'  # Aquí se habilita la autenticación de Windows
    )
    cursor = conn.cursor()
    n_test(cursor,conn)
    cursor.close()
    conn.close()
