import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_14]''')
    rows = cursor.fetchall()
    for row in rows:
        c= ((row.side_a**2) + (row.side_b**2) -(2*row.side_a*row.side_b*math.cos(math.radians(row.angle_c))))**0.5
        data_to_insert.append([row.id,c])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_14] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        #x=''
        cursor.execute('EXEC [dbo].[check_question14]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)