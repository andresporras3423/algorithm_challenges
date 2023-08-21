import sys
sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce

def test2(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT *
       FROM [math_challenges].[dbo].[question_2]''')
    rows = cursor.fetchall()
    for row in rows:
        solution=reduce(lambda x, y: x * y, range(1,int(row.val)+1),1)
        data_to_insert.append([row.id,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_2] values (?, ?)"
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        cursor.execute('EXEC [dbo].[check_question2]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].total}")  
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)  

sql_connection.get_con(test2)
