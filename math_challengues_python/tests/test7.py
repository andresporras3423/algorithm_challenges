import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_7]''')
    rows = cursor.fetchall()
    for row in rows:
        numbers=[float(num) for num in row.numbers.split(',')]
        numbers.sort()
        median = numbers[int((len(numbers)-1)/2)] if (len(numbers)%2)==1 else  (numbers[int((len(numbers)/2)-1)]+numbers[int(len(numbers)/2)])/2.0
        data_to_insert.append([row.id,median])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_7] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute("EXEC [dbo].[check_question7];")
        conn.commit()
        cursor.execute("EXEC [dbo].[get_results];")
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].total}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)