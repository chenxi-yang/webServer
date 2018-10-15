'''
Some helper functions
'''
def get_one_row(cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    print('result', result)
    if len(result) == 0:
        return None
    else:
        return result[0]

def get_all_row(cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchall()
    return result