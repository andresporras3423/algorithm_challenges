import sys
import pyodbc
import pandas as pd

sys.path.append('Y:\\Desktop\\algorithm_challenges')
from math_challengues_python import sql_connection
from functools import reduce
import math

def test(cursor, conn):
    data_to_insert = []
    cursor.execute('''SELECT * FROM [math_challenges].[dbo].[questions_13_rows] order by id, row_number''')
    rows = cursor.fetchall()
    dict_sols = {}
    for row in rows:
        if dict_sols.get(row.id) is None:
            dict_sols[row.id]=[row.row_content.split(',')]
        else:
            dict_sols[row.id].append(row.row_content.split(','))
    for k, v in dict_sols.items():
        df_v = pd.DataFrame(v)
        solution= get_determinant(df_v)
        data_to_insert.append([k,solution])
    insert_query = "INSERT INTO [math_challenges].[dbo].[solutions_13] values (?, ?)"
    # print(data_to_insert)
    cursor.executemany(insert_query, [(row[0], row[1]) for row in data_to_insert])
    conn.commit()
    try:
        #x=''
        cursor.execute('EXEC [dbo].[check_question13]')
        rows = cursor.fetchall()
        conn.commit()  # Commit the transaction
        print(f"corrects: {rows[0].corrects}, totals: {rows[0].totals}") 
    except Exception as e:
        conn.rollback()  # Roll back the transaction
        print("Error:", e)

def get_determinant(df):
    if df.shape[0]==2:
        return (float(df.iloc[0, 0]) * float(df.iloc[1, 1])) - (float(df.iloc[0, 1]) * float(df.iloc[1, 0]))
    else:
        total=0
        df_without_first = df.iloc[1:, :]
        # print("with fist:")
        # print(df)
        # print("without fist:")
        # print(df_without_first)
        for i in range(df.shape[0]):
            df_copy = df_without_first.copy()
            df_temp = df_copy.drop(df_copy.columns[i], axis=1)
            total+=(float(df.iloc[0, i])*get_determinant(df_temp)*((-1)**i))
        return total       

    #     m_a= math.sqrt((float(row.a_x)**2)+(float(row.a_y)**2))
    #     m_b= math.sqrt((float(row.b_x)**2)+(float(row.b_y)**2))
    #     a_dot_b= (float(row.a_x)*float(row.b_x))+(float(row.a_y)*float(row.b_y))
    #     solution=math.acos(a_dot_b/(m_a*m_b))
    #     # print(row.id)
    #     # print(solution)
    #     data_to_insert.append([row.id,solution])
      

sql_connection.get_con(test)