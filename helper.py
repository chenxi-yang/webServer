'''
Some helper functions
'''
def get_one_row(cursor, sql):
    cursor.execute(sql)
    result = cursor.fetchone()
    if result is None:
        return None
    else:
        return cursor.fetchone()[0]