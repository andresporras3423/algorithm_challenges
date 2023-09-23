import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_12]''')
    rows = cursor.fetchall()
    for row in rows:
        m_a= math.sqrt((float(row.a_x)**2)+(float(row.a_y)**2))
        m_b= math.sqrt((float(row.b_x)**2)+(float(row.b_y)**2))
        a_dot_b= (float(row.a_x)*float(row.b_x))+(float(row.a_y)*float(row.b_y))
        solution=math.acos(a_dot_b/(m_a*m_b))
        # print(row.id)
        # print(solution)
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_12] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        #x=''
        cursor.execute('EXEC [dbo].[check_question12]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)