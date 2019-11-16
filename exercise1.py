import psycopg2
from contextlib import closing

with closing(psycopg2.connect(dbname='mybase', user='postgres', password='pyjq',
                              host='192.168.1.49', port='5555')) as connection:

    with connection.cursor() as cursor:
        cursor.execute("SELECT department "
                        "FROM employee")
        departments = set(cursor.fetchall())

        for i in departments:
            dept = str(i[0])
            cursor.execute("SELECT name, salary "
                           "FROM employee "
                           "WHERE department = '{0}' "
                           "AND salary = (SELECT max(salary) FROM employee "
                           "WHERE department = '{0}'); ".format(dept))
            rich = cursor.fetchall()
            print('{0} - {1}'.format(dept, rich))
