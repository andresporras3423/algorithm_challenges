# from .. import sql_connection
import sys
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection

def test1(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[question_1]''')
    rows = cursor.fetchall()
    for row in rows:
        a=row.a
        b=row.b
        c=row.c
        sol1 = ((-1*b)+((b**2)-(4*a*c))**0.5)/(2*a)
        sol2 = ((-1*b)-((b**2)-(4*a*c))**0.5)/(2*a)
        data_to_insert.append([row.id,sol1,sol2])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_1] values (?, ?, ?)"
    cursor.executemany(insert_query, [(row[0], row[1], row[2]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question1]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].correct}, totals: {rows[0].total}")  
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test1)
