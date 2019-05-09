from sqlite3 import connect


class ConnSqlite:

    # 构造方法
    def __init__(self):

        self.cx = connect("./../../db/ssq.db")

    def get_sql(self):

        return self.cx
