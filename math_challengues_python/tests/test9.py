import sys
import pyodbc
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_9]''')
    rows = cursor.fetchall()
    for row in rows:
        numbers = [str(s) for s in row.init_position]
        i=0
        list_changes=[]
        while i<len(numbers):
            j=1
            while j<len(numbers)-i:
                if(int(numbers[j])<int(numbers[j-1])):
                    temp=numbers[j]
                    numbers[j]=numbers[j-1]
                    numbers[j-1]=temp
                    list_changes.append("".join(numbers))
                j+=1
            i+=1
        solution= "-".join(list_changes)
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_9] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question9]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)