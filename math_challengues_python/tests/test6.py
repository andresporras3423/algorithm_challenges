import sys
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_6]''')
    rows = cursor.fetchall()
    for row in rows:
        a=float(row.a)
        b=float(row.b)
        a_if_b=row.a_if_b
        b_if_a=''
        if(a==0):
            b_if_a='undefined'
        elif(b==0):
            b_if_a='0'
        else:
            b_if_a=str(float(a_if_b)*b/a)
        data_to_insert.append([row.id,b_if_a])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_6] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question6]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].total}")  
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)
