import sqlite3


def sql_start():
    global base, cursor
    base = sqlite3.connect('db.sqlite3')
    cursor = base.cursor()
    if base:
        print('Database connected')

        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS course(
                course_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                name TEXT
            )
            '''
        )
        base.execute(
            '''
            CREATE TABLE IF NOT EXISTS student(
                student_id INTEGER PRIMARY KEY NOT NULL, 
                name TEXT, 
                photo TEXT, 
                course INTEGER,
                FOREIGN KEY(course) REFERENCES course(course_id)
            )
            '''
        )
        base.commit()


async def get_all_courses():
    return cursor.execute("SELECT * FROM course").fetchall()


async def sql_delete_course(data):
    cursor.execute("DELETE FROM course WHERE course_id == ?", (data, ))
    base.commit()


async def sql_add_command(state, table=None):
    if table is None:
        return 
    if table == 'student':
        insert_query = f'INSERT INTO {table} VALUES (?, ?, ?, ?)'
    elif table == 'course':
        insert_query = f'INSERT INTO {table} VALUES (?, ?)'

    async with state.proxy() as data:
        cursor.execute(
            insert_query, (None, *data.values())
        )
        base.commit()
