import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_15]''')
    rows = cursor.fetchall()
    solution=''
    for row in rows:
        list_values= [float(item) for item in row.list_values.split(',')]
        max_value = max(list_values)
        min_value = min(list_values)
        mean_value = sum(list_values)/len(list_values)
        if(mean_value==0):
            solution='no solution'
        else:
            solution=f"{100*(max_value-min_value)/mean_value}"
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_15] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        #x=''
        cursor.execute('EXEC [dbo].[check_question15]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)