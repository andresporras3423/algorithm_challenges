import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math


def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_16]''')
    rows = cursor.fetchall()
    solution=''
    f=lambda z:math.factorial(z)
    for row in rows:
        n=int(row.attempts)
        x=int(row.success)
        p=float(row.probability)
        q=1-p
        solution=f(n)*(p**x)*(q**(n-x))/(f(x)*f(n-x))
        solution=round(solution,4)
        # print(solution)
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_16] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        #x=''
        cursor.execute('EXEC [dbo].[check_question16]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)