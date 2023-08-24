import sys
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[questions_5]''')
    rows = cursor.fetchall()
    for row in rows:
        x=int(row.x)
        y=int(row.y)
        radius=((x*x)+(y*y))**0.5
        angle=str(math.atan(y/x)) if x!=0 else 'undefined'
        data_to_insert.append([row.id,angle, radius])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_5] values (?, ?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1], row[2]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question5]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].total}")  
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test)
