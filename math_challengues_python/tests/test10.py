import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_10]''')
    rows = cursor.fetchall()
    for row in rows:
        numbers = [float(s) for s in row.list_numbers.split(',')]
        mean = sum(numbers)/len(numbers)
        solution = math.sqrt(sum([abs(s-mean) ** 2 for s in numbers])/len(numbers))
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_10] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question10]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)