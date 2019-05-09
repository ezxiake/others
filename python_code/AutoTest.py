# coding=utf8
import traceback, re, cx_Oracle, time, copy, random, datetime, os
# import configparser
import logging, logging.handlers
from sqlite3 import connect
import wx.lib.mixins.listctrl as listmix
import wx


# 定义字符串
chinese_set = '北国风光千里冰封万里雪飘望长城内外惟余莽莽大河上下顿失滔滔山舞银蛇原驰蜡象欲与天公试比高须晴日看红装素裹分外妖娆江山如此多娇引无数英雄竞折腰惜秦皇汉武略输文采唐宗宋祖稍逊风骚一代天骄成吉思汗只识弯弓射大雕俱往矣数风流人物还看今朝'
english_set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


class InitLog:
    """
    eg:
    log = InitLog("logFileName").get_log()
    log.debug("debug message")
    log.info("info message")
    log.warn("warn message")
    log.error("error message")
    log.critical("critical message")
    """
    def __init__(self, logFileName):

        try:
            self.cx = connect("./autotest.db")
            self.sql = self.cx.cursor()
            rst = self.sql.execute("select * from conf_log").fetchone()

            # 读取配置文件
            # filename = "./config/general.ini"
            # cc = configparser.ConfigParser()
            # cc.read(filename)  # 文件路径

            # logPath = cc.get("logger", "logPath").strip()
            # level = cc.get("logger", "level")
            # logMaxBytes = cc.get("logger", "logMaxBytes")
            # logBackupCount = cc.get("logger", "logBackupCount")
            # fileHandlerLevel = cc.get("handler", "fileHandlerLevel")
            # screenHandlerLevel = cc.get("handler", "screenHandlerLevel")

            logPath = rst[0].strip()
            level = rst[1]
            logMaxBytes = rst[2]
            logBackupCount = rst[3]
            fileHandlerLevel = rst[4]
            screenHandlerLevel = rst[5]
        except Exception as e:
            traceback.print_exc(e)
        finally:
            self.sql.close()
            self.cx.close()

        # 判断日志目录是否存在，不存在则创建
        if not os.path.exists(logPath): os.makedirs(logPath)

        # 设定日志格式
        # myFormat = '%(asctime)s [%(levelname)s] [%(filename)s][line:%(lineno)d][%(funcName)s] %(message)s'
        myFormat = '%(asctime)s [%(levelname)s]  %(message)s'

        # 公共参数初始化
        DEBUG = logging.DEBUG
        INFO = logging.INFO
        ERROR = logging.ERROR
        WARNING = logging.WARNING
        CRITICAL = logging.CRITICAL

        current_date = datetime.date.today() - datetime.timedelta(days=0)
        self.log_name = logPath + "/" + logFileName + "_%s.log" % current_date
        formatter = logging.Formatter(myFormat)
        # 获取Logger
        self.log = logging.getLogger(logFileName + str(int(time.time())))
        self.log.setLevel(locals()[level])

        # 初始化fileHandler
        file_handler = logging.handlers.RotatingFileHandler(self.log_name, 'a', int(logMaxBytes), int(logBackupCount), "UTF-8")
        file_handler.setLevel(locals()[fileHandlerLevel])
        file_handler.setFormatter(formatter)

        # 初始化screenHandler
        screen_handler = logging.StreamHandler()
        screen_handler.setFormatter(formatter)
        screen_handler.setLevel(locals()[screenHandlerLevel])

        # 装载Handler into Logger
        # if not self.log.handlers:  # 如果log中没有handler则添加，避免日志打印重复的问题
        self.log.addHandler(file_handler)
        self.log.addHandler(screen_handler)

    def get_log(self):
        return self.log

class DoDb2:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass

class DoMysql:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        pass

class DoOracle:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, control1, control2, where):
        """Constructor"""

        self.log = InitLog("auto_test").get_log()

        self.control1 = control1
        self.control2 = control2
        self.where = where

        try:

            self.start = time.clock()

            # 读取配置文件
            # filename = "./config/general.ini"
            # cc = configparser.ConfigParser()
            # cc.read(filename)
            # username = cc.get("oracle", "username")
            # password = cc.get("oracle", "password")
            # ip = cc.get("oracle", "ip")
            # service_name = cc.get("oracle", "service_name")

            self.cx = connect("./autotest.db")
            self.sql = self.cx.cursor()
            v_sql = "select * from conf_data_source" + self.where
            rst = self.sql.execute(v_sql).fetchone()
            username = rst[2]
            password = rst[3]
            ip = rst[4]
            service_name = rst[5]

            # 链接oracle数据库
            self.conn = cx_Oracle.connect(username + '/' + password + '@' + ip + '/' + service_name)
            self.c = self.conn.cursor()
            self.log.debug(" Oracle 数据库链接成功")

            # 加载配置文件
            # self.opt_oracle = open('./config/opt_oracle.cfg', 'r')
            # self.check_table_ddl = open('./config/check_table_ddl.dat', 'r')
            # self.log.debug(" opt_oracle.cfg 配置文件加载成功")

        except Exception as e:
            self.log.error(str(e))
            traceback.print_exc(e)
        finally:
            self.sql.close()
            self.cx.close()
        # else:
        #     pass

    def finish(self):
        # self.opt_oracle.close()
        # self.check_table_ddl.close()
        self.c.close()
        self.conn.close()
        self.log.info("")
        self.log.info(" ===== All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "] =====")

    def get_date(self):
        str_year = "20" + str(random.randint(10, 99))
        str_month = str(random.randint(1, 12))
        if len(str_month) == 1: str_month = "0" + str_month
        str_day = str(random.randint(1, 28))
        if len(str_day) == 1: str_day = "0" + str_day

        yyyymmdd = str_year + str_month + str_day
        return "to_date('" + yyyymmdd + "', 'YYYYMMDD')"

    def get_timestamp(self):
        str_year = "20" + str(random.randint(10, 99))

        str_month = str(random.randint(1, 12))
        if len(str_month) == 1: str_month = "0" + str_month

        str_day = str(random.randint(1, 28))
        if len(str_day) == 1: str_day = "0" + str_day

        str_hour = str(random.randint(0, 23))
        if len(str_hour) == 1: str_hour = "0" + str_hour

        str_minute = str(random.randint(1, 59))
        if len(str_minute) == 1: str_minute = "0" + str_minute

        str_second = str(random.randint(1, 59))
        if len(str_second) == 1: str_second = "0" + str_second

        yyyymmddhh24miss = str_year + str_month + str_day + str_hour + str_minute + str_second
        return "to_timestamp('" + yyyymmddhh24miss + "', 'YYYYMMDDHH24MISS')"

    def get_character(self, opt_flag, char_length):

        rst = ""
        if opt_flag == 'chinese':
            rst = "".join(random.sample(chinese_set, int(char_length)))
        elif opt_flag == 'english':
            rst = "".join(random.sample(english_set, int(char_length)))
        elif opt_flag == 'chinglish':
            rst = "".join(random.sample(chinese_set + english_set, int(char_length)))

        return rst

    def get_number(self, precision, scale):
        # 处理为空或*的情况
        if precision == "NONE" or precision == "*":
            int_precision = 0
        else:
            int_precision = int(precision)

        if scale == "NONE" or scale == "*":
            int_scale = 0
        else:
            int_scale = int(scale)

        # 开始分场景拼接返回不同的number类型数字
        if int_precision == 0:  # NUMBER NUMBER(*) NUMBER(*, 0) NUMBER(*, 3) NUMBER(*, -3)
            rst = random.uniform(9999, 999999999)
        elif int_precision != 0 and int_scale == 0:  # NUMBER(1) NUMBER(1, 0)
            rst = random.uniform(1, int(str(99999999999999999999999999999999999)[:int_precision]))
        elif int_precision != 0 and 0 < int_scale < int_precision:  # NUMBER(32, 2)
            rst = random.uniform(1, int(str(99999999999999999999999999999999999)[:int_precision - int_scale]))
        elif int_precision != 0 and int_scale < 0 < int_precision:  # NUMBER(2, -20)
            rst = 0
        else:  # NUMBER(1, 2)
            rst = 0

        return rst

    def get_date_list(self, beginDate, endDate):
        dates = []
        dt = datetime.datetime.strptime(beginDate, "%Y%m%d")
        date = beginDate[:]
        while date <= endDate:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y%m%d")
        return dates

    # 根据配置文件中读取到的操作类型来分别处理
    def execute(self):

        try:

            # 按配置文件记录数循环处理
            control1 = self.control1.strip()
            conf1 = control1.split("\n", control1.count("\n"))
            if conf1[0] != '' and conf1[0][0:2] != '粘贴':
                for line in conf1:

                    # 读取配置文件信息
                    new_line = line.split(',', line.count(','))
                    conf_opt_type = str(new_line[0]).upper()

                    if conf_opt_type == "": raise Exception(" 配置模式 不可为空")

                    # 生成测试数据
                    if conf_opt_type == 'INSERT_DATA':

                        conf_schema = str(new_line[1]).upper()
                        conf_table_name = str(new_line[2]).upper()
                        conf_date_col = str(new_line[3]).upper()
                        conf_start_date = str(new_line[4])
                        conf_end_date = str(new_line[5])
                        conf_record_count = str(new_line[6])

                        self.log.debug("   " + conf_schema + '.' + conf_table_name + ' ' + conf_date_col + ' ' + conf_start_date + ' ' + conf_end_date + ' ' + conf_record_count)

                        # 查询oracle字典表
                        self.log.debug("   查询 oracle 字典表")
                        dict_table_ddl = {}
                        int_counts = self.c.execute("SELECT COUNT(*) FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' AND TABLE_NAME = '" + conf_table_name + "' ORDER BY TABLE_NAME, COLUMN_ID")
                        if int_counts.fetchone()[0] == 0: raise Exception(" 表 " + conf_schema + "." + conf_table_name + " 在字典中不存在")

                        rst = self.c.execute("SELECT COLUMN_NAME, DATA_TYPE, DATA_LENGTH, DATA_PRECISION, DATA_SCALE FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' AND TABLE_NAME = '" + conf_table_name + "' ORDER BY TABLE_NAME, COLUMN_ID")

                        # 循环处理查询Oracle字典表返回的结果
                        list_data_type = ['VARCHAR', 'NUMBER', 'NVARCHAR', 'LONG', 'TIMESTAMP', 'CHAR', 'DATE', 'CLOB']
                        str_sql_root = "INSERT INTO " + conf_schema + '.' + conf_table_name + " ("
                        list_col_name = []

                        self.log.debug("   将字典表记录循环插入dict类型变量中保存")
                        for record_list in rst:

                            # 读取返回记录
                            col_name = str(record_list[0]).upper()
                            data_type = "".join(re.findall(r"[A-Z]", str(record_list[1]).upper()))  # 格式化数据类型 eg: timestamp(6) -> TIMESTAMP, varchar2 -> VARCHAR
                            data_length = str(record_list[2]).upper()
                            data_precision = str(record_list[3]).upper()
                            data_scale = str(record_list[4]).upper()

                            # 只处理list_data_type中预先设定的类型
                            if data_type in list_data_type:

                                # 将字段名对应的类型长度等信息装入字典中保存
                                dict_table_ddl[col_name] = [data_type, data_length, data_precision, data_scale]

                                # 将字段名拼接至insert语句中
                                str_sql_root = str_sql_root + col_name + ","
                                list_col_name.append(col_name)

                        # 字段已拼接到insert语句中，等待拼接VALUES
                        str_sql_root = str_sql_root[:len(str_sql_root) - 1] + ") VALUES ("

                        self.log.debug("   " + str_sql_root)
                        self.log.debug("   " + str(dict_table_ddl))

                        # 无需处理日期字段
                        if conf_date_col == "":

                            self.log.info("  INSERT_DATA 正在处理表 " + conf_table_name + " , 操作类型为：无需处理日期字段 .")

                            for i in range(0, int(conf_record_count)):
                                str_insert_sql = str_sql_root
                                # 遍历字典中的key（字段名）
                                chinese_flag = 0  # 当遇到第一个key属于 CHAR 或 VARCHAR, 且长度大于3时, 将 chinese_flag 赋值为1，表示预将该字段中插入中文
                                str_value = ""
                                for key in list_col_name:

                                    str_col_type = dict_table_ddl[key][0]
                                    int_col_length = int(dict_table_ddl[key][1])
                                    if chinese_flag == 0:
                                        if (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length >= 3:
                                            chinese_flag = 1
                                            str_value = self.get_character('chinese', int(int_col_length / 3))
                                        elif (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length < 3:
                                            str_value = self.get_character('english', int_col_length)
                                        elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                            str_value = self.get_character('chinglish', 200)
                                        elif str_col_type == 'NUMBER':
                                            str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                        elif str_col_type == 'DATE':
                                            str_value = self.get_date()
                                        elif str_col_type == 'TIMESTAMP': str_value = self.get_timestamp()
                                    else:
                                        if str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR':
                                            str_value = self.get_character('english', int_col_length)
                                        elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                            str_value = self.get_character('chinglish', 200)
                                        elif str_col_type == 'NUMBER':
                                            str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                        elif str_col_type == 'DATE':
                                            str_value = self.get_date()
                                        elif str_col_type == 'TIMESTAMP': str_value = self.get_timestamp()

                                    if str_col_type in ['CHAR', 'VARCHAR', 'NVARCHAR', 'LONG', 'CLOB']:
                                        str_insert_sql = str_insert_sql + "'" + str(str_value) + "',"
                                    else:
                                        str_insert_sql = str_insert_sql + str(str_value) + ","

                                str_insert_sql = str_insert_sql[:len(str_insert_sql) - 1] + ")"
                                self.log.debug("   " + str_insert_sql)
                                self.c.execute(str_insert_sql)
                            self.conn.commit()

                        # 有日期字段，且处理一天
                        elif (conf_start_date != "" and conf_end_date == "") or (conf_start_date != "" and conf_end_date != "" and conf_start_date == conf_end_date):

                            self.log.info("  INSERT_DATA 正在处理表 " + conf_table_name + " , 操作类型为：需处理日期字段（单日），日期为　" + conf_start_date + " .")

                            for i in range(0, int(conf_record_count)):
                                str_insert_sql = str_sql_root
                                # 遍历字典中的key（字段名）
                                chinese_flag = 0  # 当遇到第一个key属于 CHAR 或 VARCHAR, 且长度大于3时, 将 chinese_flag 赋值为1，表示预将该字段中插入中文
                                str_value = ""
                                for key in list_col_name:

                                    str_col_type = dict_table_ddl[key][0]
                                    int_col_length = int(dict_table_ddl[key][1])

                                    if key == conf_date_col:
                                        if str_col_type in ['CHAR', 'VARCHAR', 'NVARCHAR', 'LONG', 'CLOB']:
                                            str_value = conf_start_date
                                        elif str_col_type == 'DATE':
                                            str_value = "to_date('" + conf_start_date + "', 'YYYYMMDD')"
                                        elif str_col_type == 'TIMESTAMP':
                                            str_value = "to_timestamp('" + conf_start_date + "', 'YYYYMMDD')"
                                    else:

                                        if chinese_flag == 0:
                                            if (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length >= 3:
                                                chinese_flag = 1
                                                str_value = self.get_character('chinese', int(int_col_length / 3))
                                            elif (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length < 3:
                                                str_value = self.get_character('english', int_col_length)
                                            elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                                str_value = self.get_character('chinglish', 200)
                                            elif str_col_type == 'NUMBER':
                                                str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                            elif str_col_type == 'DATE':
                                                str_value = self.get_date()
                                            elif str_col_type == 'TIMESTAMP': str_value = self.get_timestamp()
                                        else:
                                            if str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR':
                                                str_value = self.get_character('english', int_col_length)
                                            elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                                str_value = self.get_character('chinglish', 200)
                                            elif str_col_type == 'NUMBER':
                                                str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                            elif str_col_type == 'DATE':
                                                str_value = self.get_date()
                                            elif str_col_type == 'TIMESTAMP': str_value = self.get_timestamp()

                                    if str_col_type in ['CHAR', 'VARCHAR', 'NVARCHAR', 'LONG', 'CLOB']:
                                        str_insert_sql = str_insert_sql + "'" + str(str_value) + "',"
                                    else:
                                        str_insert_sql = str_insert_sql + str(str_value) + ","

                                str_insert_sql = str_insert_sql[:len(str_insert_sql) - 1] + ")"
                                self.log.debug("   " + str_insert_sql)
                                self.c.execute(str_insert_sql)
                            self.conn.commit()

                        # 有日期字段，且处理多天
                        elif conf_start_date != "" and conf_end_date != "":

                            self.log.info("  INSERT_DATA 正在处理表 " + conf_table_name + " , 操作类型为：需处理日期字段（多日），开始日期为　" + conf_start_date + " ,结束日期为 " + conf_end_date + " .")

                            # 执行多日期
                            for opt_date in self.get_date_list(conf_start_date, conf_end_date):
                                for i in range(0, int(conf_record_count)):
                                    str_insert_sql = str_sql_root
                                    # 遍历字典中的key（字段名）
                                    chinese_flag = 0  # 当遇到第一个key属于 CHAR 或 VARCHAR, 且长度大于3时, 将 chinese_flag 赋值为1，表示预将该字段中插入中文
                                    str_value = ""
                                    for key in list_col_name:

                                        str_col_type = dict_table_ddl[key][0]
                                        int_col_length = int(dict_table_ddl[key][1])

                                        if key == conf_date_col:
                                            if str_col_type in ['CHAR', 'VARCHAR', 'NVARCHAR', 'LONG', 'CLOB']:
                                                str_value = opt_date
                                            elif str_col_type == 'DATE':
                                                str_value = "to_date('" + opt_date + "', 'YYYYMMDD')"
                                            elif str_col_type == 'TIMESTAMP':
                                                str_value = "to_timestamp('" + opt_date + "', 'YYYYMMDD')"
                                        else:

                                            if chinese_flag == 0:
                                                if (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length >= 3:
                                                    chinese_flag = 1
                                                    str_value = self.get_character('chinese', int(int_col_length / 3))
                                                elif (str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR') and int_col_length < 3:
                                                    str_value = self.get_character('english', int_col_length)
                                                elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                                    str_value = self.get_character('chinglish', 200)
                                                elif str_col_type == 'NUMBER':
                                                    str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                                elif str_col_type == 'DATE':
                                                    str_value = self.get_date()
                                                elif str_col_type == 'TIMESTAMP':
                                                    str_value = self.get_timestamp()
                                            else:
                                                if str_col_type == 'CHAR' or str_col_type == 'VARCHAR' or str_col_type == 'NVARCHAR':
                                                    str_value = self.get_character('english', int_col_length)
                                                elif str_col_type == 'LONG' or str_col_type == 'CLOB':
                                                    str_value = self.get_character('chinglish', 200)
                                                elif str_col_type == 'NUMBER':
                                                    str_value = self.get_number(dict_table_ddl[key][2], dict_table_ddl[key][3])
                                                elif str_col_type == 'DATE':
                                                    str_value = self.get_date()
                                                elif str_col_type == 'TIMESTAMP':
                                                    str_value = self.get_timestamp()

                                        if str_col_type in ['CHAR', 'VARCHAR', 'NVARCHAR', 'LONG', 'CLOB']:
                                            str_insert_sql = str_insert_sql + "'" + str(str_value) + "',"
                                        else:
                                            str_insert_sql = str_insert_sql + str(str_value) + ","

                                    str_insert_sql = str_insert_sql[:len(str_insert_sql) - 1] + ")"
                                    self.log.debug("   " + str_insert_sql)
                                    self.c.execute(str_insert_sql)
                                self.conn.commit()
                        else:
                            self.log.error("  程序无法判断执行的类型， 请检查 '日期字段、开始日期、结束日期' 是否合法")

                    # 测试存储过程
                    elif conf_opt_type == 'PROCEDURES':

                        # 定义存储过程输出参数类型枚举
                        cx_Oracle_STRING = ['VARCHAR2', 'NVARCHAR2', 'LONG']  # python's 'str' type
                        cx_Oracle_FIXED_CHAR = ['CHAR']  # python's 'str' type
                        cx_Oracle_NUMBER = ['NUMBER']  # python's 'int' type

                        conf_schema = str(new_line[1]).upper()
                        conf_procedure_name = str(new_line[2]).upper()
                        conf_arguments = str(new_line[3])

                        # 检查用户输入的配置信息是否合法

                        if conf_schema == "": raise Exception(" SCHEMA 不可为空")
                        if conf_procedure_name == "": raise Exception(" 存储过程名不可为空")

                        self.log.info("  PROCEDURES 开始准备执行存储过程 : " + conf_procedure_name)
                        self.log.debug("   " + conf_schema + '.' + conf_procedure_name + ' ' + conf_arguments)

                        # 查询oracle字典表
                        self.log.debug("   查询 oracle 字典表")

                        # 判断存储过程是否存在，不存在则报错退出
                        int_is_exists = self.c.execute("SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'PROCEDURE' AND OBJECT_NAME = '" + conf_procedure_name + "'")
                        if int_is_exists.fetchone()[0] == 0: raise Exception(" 存储过程 " + conf_schema + "." + conf_procedure_name + " 不存在")

                        # 定义变量
                        list_prc_in_argms = []
                        list_prc_in_argms_for_placeholder = []
                        # list_prc_in_argms_for_py = []
                        dict_prc_in_argms_and_type = {}
                        list_prc_out_argms = []
                        list_prc_out_argms_for_py = []
                        dict_prc_out_argms_and_type = {}

                        # 检查存储过程定义的输入参数个数， 有参数则装入字典中保存
                        int_in_counts_rst_set = self.c.execute("SELECT count(*) FROM ALL_ARGUMENTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_NAME = '" + conf_procedure_name + "' AND IN_OUT = 'IN' ORDER BY SEQUENCE")
                        int_in_counts = int_in_counts_rst_set.fetchone()[0]
                        if int_in_counts == 0:
                            self.log.info("     通过字典查询发现：存储过程 " + conf_schema + '.' + conf_procedure_name + " 无输入参数")
                        else:
                            rst = self.c.execute("SELECT ARGUMENT_NAME, DATA_TYPE FROM ALL_ARGUMENTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_NAME = '" + conf_procedure_name + "' AND IN_OUT = 'IN' ORDER BY SEQUENCE")
                            for line in rst:
                                list_prc_in_argms.append(line[0])
                                dict_prc_in_argms_and_type[line[0]] = line[1]
                                list_prc_in_argms_for_placeholder.append("")
                            self.log.info("     通过字典查询发现：存储过程 " + conf_schema + '.' + conf_procedure_name + " 有 " + str(int_in_counts) + " 个输入参数: " + str(dict_prc_in_argms_and_type))

                        # 检查存储过程定义的输出参数个数， 有参数则装入字典中保存
                        int_out_counts_rst_set = self.c.execute("SELECT count(*) FROM ALL_ARGUMENTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_NAME = '" + conf_procedure_name + "' AND IN_OUT = 'OUT' ORDER BY SEQUENCE")
                        int_out_counts = int_out_counts_rst_set.fetchone()[0]
                        if int_out_counts == 0:
                            self.log.info("     通过字典查询发现：存储过程 " + conf_schema + '.' + conf_procedure_name + " 无输出参数")
                        else:
                            rst = self.c.execute("SELECT ARGUMENT_NAME, DATA_TYPE FROM ALL_ARGUMENTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_NAME = '" + conf_procedure_name + "' AND IN_OUT = 'OUT' ORDER BY SEQUENCE")
                            for line in rst:
                                list_prc_out_argms.append(line[0])
                                dict_prc_out_argms_and_type[line[0]] = line[1]

                                if line[1] in cx_Oracle_STRING:
                                    list_prc_out_argms_for_py.append(self.c.var(cx_Oracle.STRING))
                                elif line[1] in cx_Oracle_FIXED_CHAR:
                                    list_prc_out_argms_for_py.append(self.c.var(cx_Oracle.FIXED_CHAR))
                                elif line[1] in cx_Oracle_NUMBER:
                                    list_prc_out_argms_for_py.append(self.c.var(cx_Oracle.NUMBER))
                                # elif line[1] in cx_Oracle_CURSOR:
                                #     list_prc_out_argms_for_py.append(self.c.var(cx_Oracle.CURSOR))
                                else:
                                    raise Exception(" 存储过程 " + conf_schema + "." + conf_procedure_name + " 输出参数 " + line[0] + " 类型为 " + line[1] + " 无法处理")

                            self.log.info("     通过字典查询发现：存储过程 " + conf_schema + '.' + conf_procedure_name + " 有 " + str(int_out_counts) + " 个输出参数: " + str(dict_prc_out_argms_and_type))

                        # 判断参数是否为空
                        if conf_arguments == "":
                            # list_argms = []
                            # if len(list_prc_out_argms) != 0: list_argms = list_prc_in_argms_for_placeholder + list_prc_out_argms_for_py
                            if int_in_counts != 0: self.log.warn("  该存储过程有定义输入参数，但用户传入参数为空")
                            list_argms = list_prc_in_argms_for_placeholder + list_prc_out_argms_for_py
                        else:
                            list_argms = conf_arguments.split("|", conf_arguments.count("|"))
                            if int_in_counts == 0:
                                self.log.warn("  该存储过程未定义输入参数，但用户传入了参数")
                                list_argms = []
                            elif int_in_counts != len(list_argms):
                                raise Exception(" 存储过程定义的输入参数个数与用户传入的不匹配，请检查传入参数个数")
                            if len(list_prc_out_argms) != 0: list_argms += list_prc_out_argms_for_py

                        self.log.debug("   " + str(list_argms))

                        # 执行存储过程
                        v_start_time = time.clock()
                        self.c.callproc(conf_schema + '.' + conf_procedure_name, list_argms)
                        v_stop_time = time.clock()

                        list_out_parm = []
                        for out_parm in list_prc_out_argms_for_py: list_out_parm.append(out_parm.getvalue())
                        self.log.info("     返回信息 " + str(list_out_parm))
                        self.log.info("     耗费时间 [" + "%f s" % (v_stop_time - v_start_time) + " / " + "%f m" % ((v_stop_time - v_start_time) / 60) + " / " + "%f h" % ((v_stop_time - v_start_time) / 3600) + "]")

                    # 拉链表记录比对
                    elif conf_opt_type == 'ZIPPER':
                        conf_schema = str(new_line[1]).upper()          # schema 名
                        conf_i_f_flag = str(new_line[2]).upper()        # 增全量标识
                        conf_src_tab = str(new_line[3]).upper()         # 增全量表名，比对使用
                        conf_lalian_tab = str(new_line[4]).upper()      # 拉链表名
                        conf_etl_date = str(new_line[5])                # 数据日期
                        conf_start_date_col = str(new_line[6]).upper()  # 拉链表中开始日期字段
                        conf_end_date_col = str(new_line[7]).upper()    # 拉链表中结束日期字段

                        # 检查用户输入的配置信息是否合法
                        if conf_schema == "": raise Exception("SCHEMA 不可为空")
                        if conf_i_f_flag == "" or (conf_i_f_flag != 'F' and conf_i_f_flag != 'I'): raise Exception("增全量标志不可为空，且必须为I或F")
                        if conf_src_tab == "": raise Exception("预比对的增量全表名 不可为空")
                        if conf_lalian_tab == "": raise Exception("拉链表的表名 不可为空")
                        if conf_etl_date == "": raise Exception("数据日期 不可为空")
                        if conf_start_date_col == "": raise Exception(" 拉链表开始日期字段名 不可为空")
                        if conf_end_date_col == "" and conf_i_f_flag == 'F': raise Exception("比对模式为F，拉链表结束日期字段名 不可为空")

                        # self.log.info("")
                        self.log.debug(" ZIPPER 开始准备执行拉链表比对 : 原表为 - " + conf_src_tab + "   拉链表为 - " + conf_lalian_tab)
                        self.log.debug(" " + conf_schema + ' ' + conf_i_f_flag + ' ' + conf_src_tab + ' ' + conf_lalian_tab + ' ' + conf_etl_date + ' ' + conf_start_date_col + ' ' + conf_end_date_col)

                        # 判断表及开始日期和结束日期字段是否在字典表中存在，不存在则报错退出
                        str_sql_1 = "SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_src_tab + "'"
                        if self.c.execute(str_sql_1).fetchone()[0] == 0: raise Exception("增全量表 " + conf_schema + "." + conf_src_tab + " 在字典中不存在")

                        str_sql_2 = "SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_lalian_tab + "'"
                        if self.c.execute(str_sql_2).fetchone()[0] == 0: raise Exception("拉链表 " + conf_schema + "." + conf_lalian_tab + " 在字典中不存在")

                        str_sql_3 = "SELECT COUNT(*) FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_lalian_tab + "' AND COLUMN_NAME = '" + conf_start_date_col + "'"
                        if self.c.execute(str_sql_3).fetchone()[0] == 0: raise Exception("开始日期字段 " + conf_start_date_col + "在拉链表 " + conf_schema + "." + conf_lalian_tab + " 中不存在")

                        if conf_end_date_col != "" and conf_i_f_flag == 'F':
                            str_sql_4 = "SELECT COUNT(*) FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_lalian_tab + "' AND COLUMN_NAME = '" + conf_end_date_col + "'"
                            if self.c.execute(str_sql_4).fetchone()[0] == 0: raise Exception("结束日期字段 " + conf_end_date_col + "在拉链表 " + conf_schema + "." + conf_lalian_tab + " 中不存在")

                        # 查询开始日期字段的类型及长度
                        rst = self.c.execute("SELECT DATA_TYPE, DATA_LENGTH FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_lalian_tab + "' AND COLUMN_NAME = '" + conf_start_date_col + "'")
                        line = rst.fetchone()
                        col_type = line[0].upper()
                        col_length = line[1]

                        ####
                        self.log.debug(" 开始日期字段" + conf_start_date_col + " : " + col_type + ' ' + str(col_length))
                        # self.log.info("   通过字典查询发现：存储过程 " + conf_schema + '.' + conf_procedure_name + " 有 " + str(int_in_counts) + " 个输入参数: " + str(dict_prc_in_argms_and_type))

                        if conf_i_f_flag == 'I' and col_type in ('CHAR', 'VARCHAR2') and col_length == 8:
                            v_where = " " + conf_start_date_col + " = '" + conf_etl_date + "'"
                        elif conf_i_f_flag == 'I' and col_type in ('CHAR', 'VARCHAR2') and col_length > 8:
                            v_where = " substr(regexp_replace(" + conf_start_date_col + ",'[^0-9]'),0,8) = '" + conf_etl_date + "'"
                        elif conf_i_f_flag == 'I' and col_type == 'DATE':
                            v_where = " to_char(" + conf_start_date_col + ", 'YYYYMMDD') = '" + conf_etl_date + "'"
                        elif conf_i_f_flag == 'F' and col_type in ('CHAR', 'VARCHAR2') and col_length == 8:
                            v_where = " " + conf_start_date_col + " <= '" + conf_etl_date + "' and '" + conf_etl_date + "' < " + conf_end_date_col
                        elif conf_i_f_flag == 'F' and col_type in ('CHAR', 'VARCHAR2') and col_length > 8:
                            v_where = " substr(regexp_replace(" + conf_start_date_col + ",'[^0-9]'),0,8) <= '" + conf_etl_date + "' and '" + conf_etl_date + "' < substr(regexp_replace(" + conf_end_date_col + ",'[^0-9]'),0,8)"
                        elif conf_i_f_flag == 'F' and col_type == 'DATE':
                            v_where = " to_char(" + conf_start_date_col + ", 'YYYYMMDD') <= '" + conf_etl_date + "' and '" + conf_etl_date + "' < to_char(" + conf_end_date_col + ", 'YYYYMMDD')"
                        else:
                            raise Exception("开始日期字段和结束日期字段目前只支持 CHAR VARCHAR2 DATE 类型")

                        self.log.debug(" WHERE 条件为" + v_where)

                        int_tab_count = self.c.execute("SELECT COUNT(*) FROM " + conf_src_tab)
                        src_tab_count = int_tab_count.fetchone()[0]
                        int_tab_count = self.c.execute("SELECT COUNT(*) FROM " + conf_lalian_tab + " WHERE " + v_where)
                        lalian_tab_count = int_tab_count.fetchone()[0]

                        if src_tab_count == lalian_tab_count:
                            right_error_flag = '√'
                        else:
                            right_error_flag = '×'

                        if conf_i_f_flag == 'I':
                            self.log.info("  (" + right_error_flag + ") ZIPPER 拉链表对比, 增量模式(I), 数据日期 - " + conf_etl_date + ", " + conf_src_tab + "(增量表) / " + conf_lalian_tab + "(拉链表)  记录数对比结果为 ： " + str(src_tab_count) + " / " + str(lalian_tab_count))
                        elif conf_i_f_flag == 'F':
                            self.log.info("  (" + right_error_flag + ") ZIPPER 拉链表对比, 全量模式(F), 数据日期 - " + conf_etl_date + ", " + conf_src_tab + "(全量表) / " + conf_lalian_tab + "(拉链表)  记录数对比结果为 ： " + str(src_tab_count) + " / " + str(lalian_tab_count))

                    # 表记录字段比对
                    elif conf_opt_type == 'TAB_RECORD_COL_VS':
                        conf_schema = str(new_line[1]).upper()       # schema 名
                        conf_tab_1 = str(new_line[2]).upper()        # 表1英文名
                        conf_tab_1_where = str(new_line[3])          # 表1where条件
                        conf_tab_2 = str(new_line[4]).upper()        # 表2英文名
                        conf_tab_2_where = str(new_line[5])          # 表2where条件

                        # 检查用户输入的配置信息是否合法
                        if conf_schema == "": raise Exception("SCHEMA 不可为空")
                        if conf_tab_1 == "": raise Exception("表1 英文名 不可为空")
                        if conf_tab_2 == "": raise Exception("表2 英文名 不可为空")

                        # self.log.info("")
                        self.log.debug(" TAB_COUNT_VS 开始准备执行表记录比对 : 表1 - " + conf_tab_1 + "   表2 - " + conf_tab_2)
                        self.log.debug(" " + conf_schema + ' ' + conf_tab_1 + ' ' + conf_tab_1_where + ' ' + conf_tab_2 + ' ' + conf_tab_2_where)

                        # 判断表及开始日期和结束日期字段是否在字典表中存在，不存在则报错退出
                        int_is_exists = self.c.execute("SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_tab_1 + "'")
                        if int_is_exists.fetchone()[0] == 0: raise Exception("表1 " + conf_schema + "." + equal_flag + " 在字典中不存在")

                        int_is_exists = self.c.execute("SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_tab_2 + "'")
                        if int_is_exists.fetchone()[0] == 0: raise Exception("表2 " + conf_schema + "." + conf_tab_2 + " 在字典中不存在")

                        if conf_tab_1_where != "":
                            str_sql_1_count = "SELECT COUNT(*) FROM " + conf_schema + "." + conf_tab_1 + " WHERE " + conf_tab_1_where
                            str_sql_1_all_col = "SELECT * FROM " + conf_schema + "." + conf_tab_1 + " WHERE " + conf_tab_1_where
                        else:
                            str_sql_1_count = "SELECT COUNT(*) FROM " + conf_schema + "." + conf_tab_1
                            str_sql_1_all_col = "SELECT * FROM " + conf_schema + "." + conf_tab_1

                        if conf_tab_2_where != "":
                            str_sql_2_count = "SELECT COUNT(*) FROM " + conf_schema + "." + conf_tab_2 + " WHERE " + conf_tab_2_where
                            str_sql_2_all_col = "SELECT * FROM " + conf_schema + "." + conf_tab_2 + " WHERE " + conf_tab_2_where
                        else:
                            str_sql_2_count = "SELECT COUNT(*) FROM " + conf_schema + "." + conf_tab_2
                            str_sql_2_all_col = "SELECT * FROM " + conf_schema + "." + conf_tab_2

                        str_sql_t1_minus_t2_count = "SELECT COUNT(*) FROM (" + str_sql_1_all_col + " minus " + str_sql_2_all_col + ")"
                        str_sql_t2_minus_t1_count = "SELECT COUNT(*) FROM (" + str_sql_2_all_col + " minus " + str_sql_1_all_col + ")"

                        count1 = self.c.execute(str_sql_1_count).fetchone()[0]
                        count2 = self.c.execute(str_sql_2_count).fetchone()[0]
                        count3 = self.c.execute(str_sql_t1_minus_t2_count).fetchone()[0]
                        count4 = self.c.execute(str_sql_t2_minus_t1_count).fetchone()[0]

                        if count1 == count2:
                            equal_flag = '√'
                        else:
                            equal_flag = '×'

                        self.log.info("  (" + equal_flag + ") TAB_RECORD_COL_VS 表记录对比,  记录数统计  T1:" + conf_tab_1 + "(" + str(count1) + ")  T2:" + conf_tab_2 + "(" + str(count2) + ")  In_T1_Not_In_T2(" + str(count3) + ")  In_T2_Not_In_T1(" + str(count4) + ")")

                    # 日期字段检核
                    elif conf_opt_type == 'CHECK_DATE_COL':
                        conf_schema = str(new_line[1]).upper()                                                        # schema 名
                        conf_tab_name = str(new_line[2]).upper()                                                      # 表名
                        # conf_date_col_list = str(new_line[3]).upper().split("|", str(new_line[3]).count("|"))         # 日期字段列表
                        conf_date_col = str(new_line[3]).upper()

                        # if len(conf_date_col_list) != len(list(set(conf_date_col_list))): raise Exception("日期字段有重复值，请重新检查配置")

                        # conf_date_col_format_list = str(new_line[4]).upper().split("|", str(new_line[4]).count("|"))  # 日期字段格式列表
                        conf_date_col_format = str(new_line[4]).upper()

                        # if len(conf_date_col_list) != len(conf_date_col_format_list): raise Exception("日期字段 与 日期格式 数量不匹配，请重新检查配置")

                        # dict_date_col_format = dict(zip(conf_date_col_list, conf_date_col_format_list))

                        # 检查用户输入的配置信息是否合法
                        if conf_schema == "": raise Exception("SCHEMA 不可为空")
                        if conf_tab_name == "": raise Exception("表名 不可为空")
                        if conf_date_col == "": raise Exception("日期字段 不可为空")
                        if conf_date_col_format == "": raise Exception("日期字段格式 不可为空")

                        int_is_exists = self.c.execute("SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_tab_name + "'")
                        if int_is_exists.fetchone()[0] == 0: raise Exception("表 " + conf_schema + "." + conf_tab_name + " 在字典中不存在")

                        self.log.debug(" CHECK_DATE_COL 开始准备执行日期字段检核 : 表名 - " + conf_schema + "." + conf_tab_name)
                        self.log.debug(" " + conf_schema + ' ' + conf_tab_name + ' ' + str(conf_date_col) + ' ' + str(conf_date_col_format))

                        # for date_col in dict_date_col_format:
                        # date_col_format = dict_date_col_format[date_col]

                        re_date_col_format = conf_date_col_format.replace('YYYY', r'[0-9][0-9][0-9][0-9]', 1)
                        re_date_col_format = re_date_col_format.replace('MM', r'([0][1-9]|[1][0-2])', 1)
                        re_date_col_format = re_date_col_format.replace('DD', r'([0][1-9]|[12][0-9]|[3][1])', 1)
                        re_date_col_format = re_date_col_format.replace('HH', r'([0][0-9]|[1][0-9]|[2][0-3])', 1)
                        re_date_col_format = re_date_col_format.replace('MI', r'[0-5][0-9]', 1)
                        re_date_col_format = re_date_col_format.replace('SS', r'[0-5][0-9]', 1)
                        re_date_col_format = re_date_col_format.replace('FF3', r'[0-9][0-9][0-9]', 1)
                        re_date_col_format = re_date_col_format.replace('FF6', r'[0-9][0-9][0-9][0-9][0-9][0-9]', 1)
                        re_date_col_format = '^' + re_date_col_format + '$'

                        self.log.debug(re_date_col_format)

                        str_sql_count = "SELECT COUNT(*) FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_tab_name + "' AND COLUMN_NAME = '" + conf_date_col + "'"
                        if self.c.execute(str_sql_count).fetchone()[0] == 0: raise Exception("日期字段 " + conf_date_col + "在表 " + conf_schema + "." + conf_tab_name + " 中不存在")

                        # 查询开始日期字段的类型及长度
                        rst = self.c.execute("SELECT DATA_TYPE FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_tab_name + "' AND COLUMN_NAME = '" + conf_date_col + "'")
                        col_type = rst.fetchone()[0][:4]

                        if col_type == 'DATE':
                            self.log.info("  (√) CHECK_DATE_COL 日期字段检查,  表名：" + conf_schema + "." + conf_tab_name + ",  日期字段：" + conf_date_col + "  类型为 DATE , 无需检测")
                        elif col_type == 'TIME':
                            self.log.info("  (√) CHECK_DATE_COL 日期字段检查,  表名：" + conf_schema + "." + conf_tab_name + ",  日期字段：" + conf_date_col + "  类型为 TIMESTAMP , 无需检测")
                        else:
                            str_sql = "SELECT " + conf_date_col + " FROM " + conf_schema + "." + conf_tab_name
                            list_rst_select = map(lambda x: x[0], list(self.c.execute(str_sql).fetchall()))
                            total = str(len(list(copy.deepcopy(list_rst_select))))
                            invalid_count = len(list(filter(lambda x: not(re.match(re_date_col_format, str(x))), list_rst_select)))
                            if invalid_count == 0:
                                v_flag = '√'
                            else:
                                v_flag = '×'
                            self.log.info("  (" + v_flag + ") CHECK_DATE_COL 日期字段检查,  表名：" + conf_schema + "." + conf_tab_name + ",  日期字段：" + conf_date_col + "  日期格式：" + conf_date_col_format + ",  总数量：" + total + " 不合法数量：" + str(invalid_count))

                    # 代码字段检核
                    elif conf_opt_type == 'CHECK_CODE_COL':
                        conf_schema = str(new_line[1]).upper()                                                 # schema 名
                        conf_tab_name = str(new_line[2]).upper()                                               # 表名
                        conf_code_col = str(new_line[3].upper())                                               # 代码字段名
                        conf_code_sql = str(new_line[4])                                                       # 代码枚举查询sql
                        if new_line[5] != "":
                            conf_code_enum = str(new_line[5]).upper().split("|", str(new_line[5]).count("|"))  # 代码枚举值 | 分隔
                        else:
                            conf_code_enum = ""

                        # 检查用户输入的配置信息是否合法
                        if conf_schema == "": raise Exception("SCHEMA 不可为空")
                        if conf_tab_name == "": raise Exception("表名 不可为空")
                        if conf_code_col == "": raise Exception("代码字段名 不可为空")

                        self.log.debug(" CHECK_CODE_COL 开始准备执行代码字段检核 : 表名 - " + conf_schema + "." + conf_tab_name)
                        self.log.debug(" " + conf_schema + ' ' + conf_tab_name + ' ' + conf_code_col + ' ' + conf_code_sql + ' ' + str(conf_code_enum))

                        int_is_exists = self.c.execute("SELECT COUNT(*) FROM ALL_OBJECTS WHERE OWNER = '" + conf_schema + "' AND OBJECT_TYPE = 'TABLE' AND OBJECT_NAME = '" + conf_tab_name + "'")
                        if int_is_exists.fetchone()[0] == 0: raise Exception("表 " + conf_schema + "." + conf_tab_name + " 在字典中不存在")

                        str_sql_count = "SELECT COUNT(*) FROM ALL_TAB_COLS WHERE OWNER = '" + conf_schema + "' and TABLE_NAME = '" + conf_tab_name + "' AND COLUMN_NAME = '" + conf_code_col + "'"
                        if self.c.execute(str_sql_count).fetchone()[0] == 0: raise Exception("代码字段 " + conf_code_col + "在表 " + conf_schema + "." + conf_tab_name + " 中不存在")

                        rst = self.c.execute("SELECT " + conf_code_col + ", COUNT(*) FROM " + conf_schema + "." + conf_tab_name + " GROUP BY " + conf_code_col)
                        select_rst = copy.deepcopy(rst.fetchall())
                        list_code_range = list(sorted(map(lambda x: str(x[0]).upper(), select_rst)))
                        # print(select_rst)
                        # print(str(sum(list(map(lambda x: x[1], select_rst)))))
                        self.log.debug(" list_code_range（代码字段值域范围）：" + str(list_code_range))

                        if conf_code_sql != "":
                            rst = self.c.execute(conf_code_sql)
                            list_code_enum = list(map(lambda x: str(x[0]).upper(), rst.fetchall()))
                            list_invalid_enum = list(sorted(filter(lambda x: x not in list_code_enum, list_code_range)))
                        elif conf_code_enum != "":
                            list_invalid_enum = list(sorted(filter(lambda x: x not in conf_code_enum, list_code_range)))
                        else:
                            list_invalid_enum = []

                        if len(list_invalid_enum) == 0:
                            v_flag = '√'
                        else:
                            v_flag = '×'

                        self.log.info("  (" + v_flag + ") CHECK_CODE_COL 代码字段检查,  表名：" + conf_schema + "." + conf_tab_name + " ,  代码字段：" + conf_code_col)
                        self.log.info("     值域范围 ：" + str(list_code_range))
                        self.log.info("     无效代码 ：" + str(list_invalid_enum))

                    else:
                        self.log.warn("该配置模式（" + conf_opt_type + "）暂时不被支持,请修改配置信息后重新测试")

            # 将dat文件记录装入字典中保存
            control2 = self.control2.strip()
            conf2 = control2.split("\n", control2.count("\n"))
            if conf2[0] != '' and conf2[0][0:2] != '粘贴':

                dict_table_ddl = {}
                names = locals()
                list_owner_tabname = []

                for line in conf2:
                    list_line = line.split('|', line.count('|'))

                    if list_line[0] + "@" + list_line[1] in dict_table_ddl.keys():
                        names[list_line[0] + "@" + list_line[1]].append(list_line)
                    else:
                        names[list_line[0] + "@" + list_line[1]] = []
                        names[list_line[0] + "@" + list_line[1]].append(list_line)

                    dict_table_ddl[list_line[0] + "@" + list_line[1]] = names[list_line[0] + "@" + list_line[1]]

                # 从字典中取出数据，循环操作
                for key in dict_table_ddl.keys():

                    list_owner_tabname = key.split('@', 1)
                    owner = list_owner_tabname[0].upper()
                    tabname = list_owner_tabname[1].upper()

                    v_count_sql = "SELECT COUNT(*) FROM ALL_TAB_COLS C " \
                                          "LEFT JOIN (SELECT A.* FROM ALL_CONS_COLUMNS A, ALL_CONSTRAINTS B WHERE A.CONSTRAINT_NAME = B.CONSTRAINT_NAME " \
                                          "AND B.CONSTRAINT_TYPE = 'P' AND B.TABLE_NAME = '" + tabname + "' ) D " \
                                          "ON C.COLUMN_NAME = D.COLUMN_NAME WHERE C.OWNER = '" + owner + "' and C.TABLE_NAME = '" + tabname + "' ORDER BY C.TABLE_NAME, C.COLUMN_ID"

                    if self.c.execute(v_count_sql).fetchone()[0] == 0:
                        self.log.error(" " + owner + "." + tabname + " 不存在")
                        continue

                    v_select_sql = "SELECT C.OWNER, C.TABLE_NAME, C.COLUMN_NAME, C.COLUMN_ID, C.NULLABLE, " \
                                          "CASE WHEN D.COLUMN_NAME IS NULL THEN 'N' ELSE 'Y' END AS PRIMARY_KEY, C.DATA_TYPE, C.DATA_LENGTH, C.DATA_PRECISION, C.DATA_SCALE FROM ALL_TAB_COLS C " \
                                          "LEFT JOIN (SELECT A.* FROM ALL_CONS_COLUMNS A, ALL_CONSTRAINTS B WHERE A.CONSTRAINT_NAME = B.CONSTRAINT_NAME " \
                                          "AND B.CONSTRAINT_TYPE = 'P' AND B.TABLE_NAME = '" + tabname + "' ) D " \
                                          "ON C.COLUMN_NAME = D.COLUMN_NAME WHERE C.OWNER = '" + owner + "' and C.TABLE_NAME = '" + tabname + "' ORDER BY C.TABLE_NAME, C.COLUMN_ID"

                    list_table_ddl_local = list(map(lambda y: y, self.c.execute(v_select_sql).fetchall()))

                    col_same_count = 0     # 相同字段个数记录
                    list_log_records = []  # 存放日志信息，后面一起输出
                    vs_flag = 0            # 0 一样； 1 不一样
                    pos_flag = 0           # 0 一样； 1 不一样

                    # 比对字段数
                    v_src_tab_col_count = len(dict_table_ddl[key])
                    v_local_tab_col_count = len(list_table_ddl_local)
                    if v_src_tab_col_count != v_local_tab_col_count:
                        vs_flag = 1
                        list_log_records.append("     字段数不一致 ： 相差 " + str(abs(v_src_tab_col_count - v_local_tab_col_count)) + "个")

                    list_src_col_sort = []
                    list_local_col_sort = []
                    for list_src in dict_table_ddl[key]:
                        col_name = list_src[2].upper()
                        v_list_list_index = []
                        for v_list_index in range(max(v_src_tab_col_count, v_local_tab_col_count)):
                            # self.log.warn(list_table_ddl_local)
                            # self.log.warn(v_list_index)
                            # print(list_table_ddl_local)
                            # print(v_list_index)
                            if v_list_index + 1 > len(list_table_ddl_local):
                                list_src_col_sort.append(col_name.ljust(30))
                                list_local_col_sort.append(''.ljust(30))
                                break
                            else:
                                list_local = list_table_ddl_local[v_list_index]

                            if col_name == list_local[2].upper():  # 字段相同的

                                list_src_col_sort.append(col_name.ljust(30))
                                list_local_col_sort.append(col_name.ljust(30))

                                col_same_count += 1

                                # if list_src[3] != list_local[3]: pass  # 字段序号不处理
                                if list_src[4].upper() != list_local[4].upper():   # 是否可空
                                    vs_flag = 1
                                    list_log_records.append("     字段 " + col_name + " 是否可空标志不同：源表标志（" + list_src[4].upper() + "） 本地表标志（" + list_local[4].upper() + "）")
                                if list_src[5].upper() != list_local[5].upper():   # 主键
                                    vs_flag = 1
                                    list_log_records.append("     字段 " + col_name + " 是否主键标志不同：源表标志（" + list_src[5].upper() + "） 本地表标志（" + list_local[5].upper() + "）")
                                if list_src[6].upper() != list_local[6].upper():   # 字段类型
                                    vs_flag = 1
                                    list_log_records.append("     字段 " + col_name + " 字段类型不同：源表类型（" + list_src[6].upper() + "） 本地表类型（" + list_local[6].upper() + "）")
                                if str(list_src[7]) != str(list_local[7]):   # 字段长度
                                    vs_flag = 1
                                    list_log_records.append("     字段 " + col_name + " 字段长度不同：源表长度（" + str(list_src[7]) + "） 本地表长度（" + str(list_local[7]) + "）")
                                if (str(list_src[8]) != '' or str(list_local[8]) != 'None') and str(list_src[8]) != str(list_local[8]):   # Local None
                                    vs_flag = 1
                                    if str(list_local[8]) == 'None':
                                        local_precision = ''
                                    else:
                                        local_precision = str(list_local[8])
                                    list_log_records.append("     字段 " + col_name + " 字段精度不同：源表精度（" + str(list_src[8]) + "） 本地表精度（" + local_precision + "）")
                                if (str(list_src[9]) != '' or str(list_local[9]) != 'None') and str(list_src[9]) != str(list_local[9]):   # Local None
                                    vs_flag = 1
                                    if str(list_local[9]) == 'None':
                                        local_scale = ''
                                    else:
                                        local_scale = str(list_local[9])
                                    list_log_records.append("     字段 " + col_name + " 字段小数位数不同：源表小数位数（" + str(list_src[9]) + "） 本地表小数位数（" + local_scale + "）")

                                v_list_list_index.append(v_list_index)
                                break
                            else:
                                pos_flag = 1
                                list_src_col_sort.append(''.ljust(30))
                                list_local_col_sort.append(str(list_local[2].upper()).ljust(30))
                                v_list_list_index.append(v_list_index)

                        for v_index in v_list_list_index: list_table_ddl_local.pop(0)

                    # print(list_table_ddl_local)
                    for local_other in range(len(list_table_ddl_local)):
                        list_src_col_sort.append(''.ljust(30))
                        list_local_col_sort.append(list_table_ddl_local[local_other][2].ljust(30))

                    # 将比对结果循环输出到日志，可以使用map
                    if vs_flag == 0:
                        self.log.info("  (√) CHECK_TABLE_DDL 表结构比对,  表名：" + owner + "." + tabname + "  源表字段数（" + str(v_src_tab_col_count) + "） 本地表字段数（" + str(v_local_tab_col_count) + "） 相同字段数（" + str(col_same_count) + "）")
                    else:
                        self.log.info("  (×) CHECK_TABLE_DDL 表结构比对,  表名：" + owner + "." + tabname + "  源表字段数（" + str(v_src_tab_col_count) + "） 本地表字段数（" + str(v_local_tab_col_count) + "） 相同字段数（" + str(col_same_count) + "）")

                    for log in list_log_records:
                        self.log.info(log)

                    if pos_flag == 1:

                        for x in range(len(list_src_col_sort)):
                            self.log.info("     " + list_src_col_sort[x] + "     -----     " + list_local_col_sort[x])

        except Exception as e:
            self.conn.rollback()
            self.log.error("  " + str(e))
            traceback.print_exc(e)
        finally:
            self.finish()


# class stdoutBuffer(object):
#     def __init__(self):
#         self.buffer = []
#
#     def write(self, *args, **kwargs):
#         self.buffer.append(args)


########################################################################
class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    """TextEditMixin allows any column to be edited."""

    # ----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)
        self.__canEditList = []  # 可编辑项目列表

    def OpenEditor(self, col, row):
        """ 控制当前项目能否编辑 """
        if self.canEdit(col, row):
            listmix.TextEditMixin.OpenEditor(self, col, row)
        else:
            pass

    def setCanEditList(self, canEditList):
        """ 设置某行某列为可编辑 @param editFlagList: @type list: 单个元素是元组类型,参照 self.__canEditList 的说明 """
        self.__canEditList = canEditList

    def appendCanEditItem(self, col, row):
        """ 将指定的项目添加到可编辑列表中 """
        if (col, row) not in self.__canEditList:
            self.__canEditList.append((col, row))
        else:
            pass

    def removeCanEditItem(self, col, row):
        """ 将指定项目从可编辑列表中移除,使其不可编辑 """
        if (col, row) in self.__canEditList:
            self.__canEditList.remove((col, row))
        else:
            pass

    def removeAllCanEditItem(self):
        self.__canEditList = []

    def canEdit(self, col, row):
        """ 判断当前点击的项目是否可编辑 """
        if (col, row) in self.__canEditList:
            return True
        else:
            return False

    def currentCanEditItem(self):
        """ 返回当前可编辑项目的列表 """
        return self.__canEditList

########################################################################
class MyPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""

        # self.log = InitLog("gui").get_log()

        try:

            # self.start = time.clock()

            # cols = ['A', 'B', 'C']
            # # cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            # # select_sql = "SELECT " + str(cols).replace('[', '').replace(']', '').replace("'", '') + " FROM LISTCTRL"
            # select_sql = "SELECT " + str(cols).replace('[', '').replace(']', '').replace("'", '') + " FROM CODE_TAB"
            # rst = self.c.execute(select_sql)
            # rows = list(map(lambda z: z, rst.fetchall()))
            #

            self.cx = connect("./autotest.db")
            self.sql = self.cx.cursor()

            wx.Panel.__init__(self, parent)
            #
            # self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
            #
            # index = 0
            # for col in cols:
            #     self.list_ctrl.InsertColumn(index, col)
            #     index += 1
            #
            # index = 0
            # for row in rows:
            #     self.list_ctrl.InsertStringItem(index, row[0])
            #     for count in range(1, len(row)):
            #         self.list_ctrl.SetStringItem(index, count, row[count])
            #     index += 1
            # # self.SetBackgroundColour('#4f5049')

            self.control1 = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.HSCROLL)
            self.control2 = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.HSCROLL)
            self.control3 = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)

            self.control1.SetLabelText("粘贴自动化测试配置")
            self.control2.SetLabelText("粘贴表结构对比配置")

            sizer1 = wx.BoxSizer(wx.VERTICAL)
            sizer1.Add(self.control1, 1, wx.EXPAND | wx.ALL, 10)
            sizer1.Add(self.control2, 1, wx.EXPAND | wx.ALL, 10)

            sizer2 = wx.BoxSizer(wx.HORIZONTAL)
            sizer2.Add(sizer1, 1, wx.EXPAND, 0)
            sizer2.Add(self.control3, 1, wx.EXPAND | wx.ALL, 10)

            rst = self.sql.execute("select * from conf_data_source order by type, id").fetchall()
            list_rst = []
            self.dict_rst = {}
            for line in rst:
                key = line[0] + " - " + line[1] + " - " + line[2] + "/" + line[3] + "@" + line[4] + ":" + line[5]
                value = " where id = '" + line[0] + "' and type = '" + line[1] + "'"
                list_rst.append(key)
                self.dict_rst[key] = value

            # print(self.dict_rst)
            # self.st = wx.StaticText(self, -1, "数据源:", (15, 20), style=wx.ALIGN_CENTER | wx.CENTER)
            # self.wc = wx.Choice(self, -1, "选择数据源", (85, 18), choices=list_rst, style=wx.ALIGN_CENTER | wx.CENTER)
            self.wc = wx.ComboBox(self, -1, "选择数据源", (15, 30), size=wx.DefaultSize, choices=list_rst, style=wx.CB_DROPDOWN)

            self.buttonProgramConf = wx.Button(self, wx.ID_ANY, "设置")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonProgramConf, self.buttonProgramConf)

            self.buttonDeleteConfUp = wx.Button(self, wx.ID_ANY, "清空配置(上)")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonDeleteConfUp, self.buttonDeleteConfUp)
            # self.buttonDeleteConfUp.SetDefault()

            self.buttonDeleteConfDown = wx.Button(self, wx.ID_ANY, "清空配置(下)")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonDeleteConfDown, self.buttonDeleteConfDown)
            # self.buttonDeleteConfDown.SetDefault()

            self.buttonDeleteLog = wx.Button(self, wx.ID_ANY, "清空日志")
            self.Bind(wx.EVT_BUTTON, self.OnClickDeleteLog, self.buttonDeleteLog)
            # self.buttonDeleteLog.SetDefault()

            self.buttonExecute = wx.Button(self, wx.ID_ANY, "执行程序")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonExecute, self.buttonExecute)
            # self.buttonExecute.SetDefault()

            sizer3 = wx.BoxSizer(wx.HORIZONTAL)
            # sizer3.Add(self.st, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.wc, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.buttonProgramConf, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.buttonDeleteConfUp, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.buttonDeleteConfDown, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.buttonDeleteLog, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer3.Add(self.buttonExecute, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)

            sizer4 = wx.BoxSizer(wx.VERTICAL)
            sizer4.Add(sizer2, 1, wx.EXPAND | wx.UP, 0)
            sizer4.Add(sizer3, 0, wx.CENTER, 0)
            self.SetSizer(sizer4)

            # 设置全部可编辑，可扩充至方法中，根据类型进行控制
            # for x in range(len(cols)):
            #     for y in range(self.list_ctrl.GetItemCount()):
            #         self.list_ctrl.appendCanEditItem(x, y)

        except Exception as e:
            # self.conn.rollback()
            # self.log.error("  " + str(e))
            traceback.print_exc(e)

        # finally:
        #     self.finish()

    def OnClickButtonProgramConf(self, event):
        MyFrameConf(self)

    def OnClickButtonDeleteConfUp(self, event):
        self.control1.SetLabelText("")

    def OnClickButtonDeleteConfDown(self, event):
        self.control2.SetLabelText("")

    def OnClickDeleteLog(self, event):
        self.control3.SetLabelText("")

    def OnClickButtonExecute(self, event):

        if self.wc.GetCurrentSelection() == -1:
            self.control3.SetLabelText("ERROR : 请先选择数据源")
        else:
            type = self.wc.GetValue().split('-', self.wc.GetValue().count('-'))[1].strip()
            if type == 'ORACLE':

                try:
                    log_name = "./log/auto_test_%s.log" % (datetime.date.today() - datetime.timedelta(days=0))
                    f_log = open(log_name, 'w+', encoding='UTF-8')
                    f_log.truncate()
                    do = DoOracle(self.control1.GetValue(), self.control2.GetValue(), self.dict_rst[str(self.wc.GetValue())])
                    do.execute()
                finally:
                    self.control3.SetLabelText("")
                    self.control3.AppendText(f_log.read())
                    f_log.close()
                    time.sleep(1)

            elif type == 'MYSQL':
                # dm = DoMysql()
                # dm.execute()
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            elif type == 'DB2':
                # dd = DoDb2()
                # dd.execute()
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

    def setDictRst(self, dict_rst):
        self.dict_rst = dict_rst

    def finish(self):
        # self.opt_oracle.close()
        # self.check_table_ddl.close()
        # self.c.close()
        # self.conn.close()
        self.log.info("")
        self.log.info(" ===== All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "] =====")

########################################################################
class MyMenuBar(wx.MenuBar, wx.Menu):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.parent = parent  # frame
        self.parent.CreateStatusBar()

        menubar = wx.MenuBar()
        menufile = wx.Menu()
        menufile2 = wx.Menu()

        mnuabout = menufile.Append(wx.ID_ABOUT, '&About', 'about this shit')
        mnuexit = menufile.Append(wx.ID_EXIT, 'E&xit', 'end program')

        # sampleList = ['zero', 'one', 'two', 'three', 'four', 'five',
        #               'six', 'seven', 'eight']
        # wx.StaticText(self, -1, "Select one:", (15, 20))
        # wx.Choice(self, -1, (85, 18), choices=sampleList)

        menubar.Append(menufile, '&File1')
        menubar.Append(menufile2, '&File2')
        # menubar.Append(menufile, '&File3')

        # 事件绑定
        self.parent.Bind(wx.EVT_MENU, self.onAbout, mnuabout)
        self.parent.Bind(wx.EVT_MENU, self.onExit, mnuexit)

        self.parent.SetMenuBar(menubar)

    '''点击about的事件响应'''
    def onAbout(self, evt):
        dlg = wx.MessageDialog(self.parent, 'This app is a simple text editor', 'About my app', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    '''点击退出'''
    def onExit(self, evt): self.parent.Close(True)

########################################################################
class MyFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, title="Automatic Test v1.0 by xiaoke", size=(880, 600))
        # self.menubar = MyMenuBar(self)
        self.panel = MyPanel(self)
        self.Center()
        self.Show()

class MyPanelConf(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent, superParent):
        """Constructor"""

        self.superParent = superParent

        try:

            wx.Panel.__init__(self, parent)

            self.cx = connect("./autotest.db")
            self.sql = self.cx.cursor()

            # 左侧布局
            rst = self.sql.execute("select * from conf_data_source order by type, id").fetchall()
            list_rst = []
            self.dict_rst = {}
            for line in rst:
                key = line[0] + " - " + line[1] + " - " + line[2] + "/" + line[3] + "@" + line[4] + ":" + line[5]
                value = line[0] + "|" + line[1] + "|" + line[2] + "|" + line[3] + "|" + line[4] + "|" + line[5]
                list_rst.append(key)
                self.dict_rst[key] = value

            # print(self.dict_rst)
            self.st = wx.StaticText(self, -1, "数据源 :")
            # self.wc = wx.Choice(self, -1, "选择数据源", (85, 18), choices=list_rst, style=wx.ALIGN_CENTER | wx.CENTER)
            self.wc = wx.ComboBox(self, -1, "删除、修改 - 请选择", (15, 30), size=wx.DefaultSize, choices=list_rst, style=wx.CB_DROPDOWN)
            self.Bind(wx.EVT_COMBOBOX, self.OnSelectedWC, self.wc)

            self.idLabel = wx.StaticText(self, -1, "数据源名 :")
            self.idText = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.idText.SetInsertionPoint(0)

            self.typeLabel = wx.StaticText(self, -1, "数据源类型 :")
            # self.typeText = wx.TextCtrl(self, -1, "", size=(175, -1))
            # self.typeText.SetInsertionPoint(0)
            self.typecb = wx.ComboBox(self, -1, "ORACLE", (15, 30), size=wx.DefaultSize, choices=['MYSQL', 'DB2', 'ORACLE'], style=wx.CB_DROPDOWN)

            self.usernameLabel = wx.StaticText(self, -1, "用户名 :")
            self.usernameText = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.usernameText.SetInsertionPoint(0)

            self.passwordLabel = wx.StaticText(self, -1, "密码 :")
            self.passwordText = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.passwordText.SetInsertionPoint(0)

            self.ipLabel = wx.StaticText(self, -1, "IP :")
            self.ipText = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.ipText.SetInsertionPoint(0)

            self.servicenameLabel = wx.StaticText(self, -1, "service name :")
            self.servicenameText = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.servicenameText.SetInsertionPoint(0)

            self.buttonSave1 = wx.Button(self, wx.ID_ANY, "保存数据源配置")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonSave1, self.buttonSave1)

            self.buttonDel = wx.Button(self, wx.ID_ANY, "删除数据源配置")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonDel, self.buttonDel)

            self.buttonTest = wx.Button(self, wx.ID_ANY, "测试连接")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonTest, self.buttonTest)

            sizerLeft = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
            sizerLeft.AddMany([wx.StaticText(self, -1, "数据源信息配置"), wx.StaticText(self, -1, ""), self.st, self.wc, self.idLabel, self.idText, self.typeLabel, self.typecb, self.usernameLabel, self.usernameText, self.passwordLabel, self.passwordText, self.ipLabel, self.ipText, self.servicenameLabel, self.servicenameText, self.buttonSave1, self.buttonDel, self.buttonTest])
            # self.SetSizer(sizerLeft)

            # 右侧布局
            rst = self.sql.execute("SELECT * FROM conf_log").fetchone()
            self.logger_logPath_Label = wx.StaticText(self, -1, "日志路径 :")
            self.logger_logPath_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.logger_logPath_Text.SetValue(rst[0])
            self.logger_logPath_Text.SetInsertionPoint(0)

            self.logger_level_Label = wx.StaticText(self, -1, "总日志等级 :")
            self.logger_level_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.logger_level_Text.SetValue(rst[1])
            self.logger_level_Text.SetInsertionPoint(0)

            self.logger_logMaxBytes_Label = wx.StaticText(self, -1, "单日志文件大小 :")
            self.logger_logMaxBytes_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.logger_logMaxBytes_Text.SetValue(rst[2])
            self.logger_logMaxBytes_Text.SetInsertionPoint(0)

            self.logger_logBackupCount_Label = wx.StaticText(self, -1, "日志文件总数 :")
            self.logger_logBackupCount_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.logger_logBackupCount_Text.SetValue(rst[3])
            self.logger_logBackupCount_Text.SetInsertionPoint(0)

            self.handler_fileHandlerLevel_Label = wx.StaticText(self, -1, "文件日志输出等级 :")
            self.handler_fileHandlerLevel_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.handler_fileHandlerLevel_Text.SetValue(rst[4])
            self.handler_fileHandlerLevel_Text.SetInsertionPoint(0)

            self.handler_screenHandlerLevel_Label = wx.StaticText(self, -1, "控制台日志输出等级 :")
            self.handler_screenHandlerLevel_Text = wx.TextCtrl(self, -1, "", size=(175, -1))
            self.handler_screenHandlerLevel_Text.SetValue(rst[5])
            self.handler_screenHandlerLevel_Text.SetInsertionPoint(0)

            self.buttonSave2 = wx.Button(self, wx.ID_ANY, "保存日志配置")
            self.Bind(wx.EVT_BUTTON, self.OnClickButtonSave2, self.buttonSave2)

            sizerRight = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
            sizerRight.AddMany([wx.StaticText(self, -1, "日志信息配置"), wx.StaticText(self, -1, ""), wx.StaticText(self, -1, ""), wx.StaticText(self, -1, ""), self.logger_logPath_Label, self.logger_logPath_Text, self.logger_level_Label, self.logger_level_Text, self.logger_logMaxBytes_Label, self.logger_logMaxBytes_Text, self.logger_logBackupCount_Label, self.logger_logBackupCount_Text, self.handler_fileHandlerLevel_Label, self.handler_fileHandlerLevel_Text, self.handler_screenHandlerLevel_Label, self.handler_screenHandlerLevel_Text, self.buttonSave2])

            sizer = wx.BoxSizer(wx.HORIZONTAL)
            # sizer3.Add(self.st, 0, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer.Add(sizerLeft, 1, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            sizer.Add(sizerRight, 1, wx.ALIGN_RIGHT | wx.RIGHT, 10)
            self.SetSizer(sizer)

        except Exception as e:
            traceback.print_exc(e)

    def updateComBoBox(self, currvar):
        rst = self.sql.execute("select * from conf_data_source order by type, id").fetchall()
        list_rst = []
        self.dict_rst = {}
        for line in rst:
            key = line[0] + " - " + line[1] + " - " + line[2] + "/" + line[3] + "@" + line[4] + ":" + line[5]
            value = line[0] + "|" + line[1] + "|" + line[2] + "|" + line[3] + "|" + line[4] + "|" + line[5]
            list_rst.append(key)
            self.dict_rst[key] = value

        self.wc.SetItems(list_rst)
        self.wc.SetValue(currvar)
        self.idText.SetValue('')
        # self.typecb.SetValue('')
        self.usernameText.SetValue('')
        self.passwordText.SetValue('')
        self.ipText.SetValue('')
        self.servicenameText.SetValue('')

    def updateParentComBoBox(self):
        rst = self.sql.execute("select * from conf_data_source order by type, id").fetchall()
        list_rst = []
        dict_rst = {}
        for line in rst:
            key = line[0] + " - " + line[1] + " - " + line[2] + "/" + line[3] + "@" + line[4] + ":" + line[5]
            value = " where id = '" + line[0] + "' and type = '" + line[1] + "'"
            list_rst.append(key)
            dict_rst[key] = value

        self.superParent.wc.SetItems(list_rst)
        self.superParent.wc.SetValue('选择数据源')
        self.superParent.setDictRst(dict_rst)

    def OnClickButtonTest(self, event):
        if self.wc.GetCurrentSelection() == -1:
            dlg = wx.MessageDialog(self, '请先选择数据源', '提示', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # type = self.wc.GetValue().split('-', self.wc.GetValue().count('-'))[1].strip()
            type = self.typecb.GetValue()
            if type == 'ORACLE':

                username = self.usernameText.GetValue()
                password = self.passwordText.GetValue()
                ip = self.ipText.GetValue()
                service_name = self.servicenameText.GetValue()

                # 链接oracle数据库
                try:
                    conn = cx_Oracle.connect(username + '/' + password + '@' + ip + '/' + service_name)
                    c = conn.cursor()
                    if c.execute("select 1 from dual").fetchone()[0] == 1:
                        dlg = wx.MessageDialog(self, '连接成功', '提示', wx.OK)
                        dlg.ShowModal()
                        dlg.Destroy()
                except Exception as e:
                    dlg = wx.MessageDialog(self, '连接失败!!!  ' + str(e), '提示', wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()
                    traceback.print_exc(e)
                else:
                    c.close()
                    conn.close()

            elif type == 'MYSQL':
                # dm = DoMysql()
                # dm.execute()
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            elif type == 'DB2':
                # dd = DoDb2()
                # dd.execute()
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                dlg = wx.MessageDialog(self, '数据源类型：' + type + ' 暂时不被支持', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

    def OnClickButtonDel(self, event):
        flag = self.wc.GetSelection()
        if flag == -1:
            dlg = wx.MessageDialog(self, '删除前请选择数据源配置', '提示', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:

            sel_sql = "select count(*) from conf_data_source where id = '" + self.idText.GetValue() + "' and type = '" + self.typecb.GetValue() + "'"
            rst = self.sql.execute(sel_sql).fetchone()[0]

            if rst == 0:
                dlg = wx.MessageDialog(self, '该配置不存在', '提示', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

            else:
                # currValue = self.wc.GetSelection()
                wmd = wx.MessageDialog(self, '确认要删除该数据源配置 ？', '提示', wx.YES_NO)
                if wmd.ShowModal() == wx.ID_YES:
                    del_sql = "delete from conf_data_source where id = '" + self.idText.GetValue() + "' and type = '" + self.typecb.GetValue() + "'"
                    self.sql.execute(del_sql)
                    self.cx.commit()

                    self.updateComBoBox('删除、修改 - 请选择')

                    dlg = wx.MessageDialog(self, '删除成功', '提示', wx.OK)
                    dlg.ShowModal()
                    dlg.Destroy()

                self.updateParentComBoBox()
                wmd.Destroy()


    def OnSelectedWC(self, event):
        var = str(self.dict_rst[self.wc.GetValue()])
        list_var = var.split("|", var.count("|"))
        self.idText.SetValue(list_var[0])
        self.typecb.SetValue(list_var[1])
        self.usernameText.SetValue(list_var[2])
        self.passwordText.SetValue(list_var[3])
        self.ipText.SetValue(list_var[4])
        self.servicenameText.SetValue(list_var[5])

    def OnClickButtonSave1(self, event):
        a = self.idText.GetValue().strip().upper()
        b = self.typecb.GetValue().strip().upper()
        c = self.usernameText.GetValue().strip()
        d = self.passwordText.GetValue().strip()
        e = self.ipText.GetValue().strip()
        f = self.servicenameText.GetValue().strip()

        if a == '' or c == '' or d == '' or e == '' or f == '':
            dlg = wx.MessageDialog(self, '数据源配置不可有为空字段', '提示', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            sel_sql = "select count(*) from conf_data_source where id = '" + a + "' and type = '" + b + "'"
            rst = self.sql.execute(sel_sql).fetchone()[0]

            if rst == 0:
                insert_sql = "insert into conf_data_source values('" + a + "','" + b + "','" + c + "','" + d + "','" + e + "','" + f + "')"
                self.sql.execute(insert_sql)
                self.cx.commit()

                dlg = wx.MessageDialog(self, '保存成功', '数据源配置 - 新增', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

                # self.wc.SetValue(a + " - " + b + " - " + c + "/" + d + "@" + e + ":" + f)
                # self.wc.AppendItems(a + " - " + b + " - " + c + "/" + d + "@" + e + ":" + f)

            else:
                update_sql = "UPDATE conf_data_source SET username = '" + c + "', password = '" + d + "', ip = '" + e + "', service_name = '" + f + "' where id = '" + a + "' and type = '" + b + "'"
                self.sql.execute(update_sql)
                self.cx.commit()
                dlg = wx.MessageDialog(self, '保存成功', '数据源配置 - 修改', wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

            self.updateComBoBox('删除、修改 - 请选择')
            self.updateParentComBoBox()


    def OnClickButtonSave2(self, event):
        a = self.logger_logPath_Text.GetValue().strip()
        b = self.logger_level_Text.GetValue().strip()
        c = self.logger_logMaxBytes_Text.GetValue().strip()
        d = self.logger_logBackupCount_Text.GetValue().strip()
        e = self.handler_fileHandlerLevel_Text.GetValue().strip()
        f = self.handler_screenHandlerLevel_Text.GetValue().strip()

        if a == '' or b == '' or c == '' or d == '' or e == '' or f == '':
            dlg = wx.MessageDialog(self, '日志信息配置不可有为空字段', '提示', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            update_sql = "UPDATE conf_log SET logger_logPath = '" + a + "', logger_level = '" + b + "', logger_logMaxBytes = '" + c + "', logger_logBackupCount = '" + d + "', handler_fileHandlerLevel = '" + e + "', handler_screenHandlerLevel = '" + f + "'"
            self.sql.execute(update_sql)
            self.cx.commit()
            dlg = wx.MessageDialog(self, '保存成功', '日志配置 - 修改', wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

class MyFrameConf(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, title="程序配置", size=(880, 600))
        # self.menubar = MyMenuBar(self)
        self.panel = MyPanelConf(self, parent)
        self.Center()
        self.Show()

class InitDB:

    def __init__(self):
        if not os.path.exists(os.getcwd() + '\log'): os.makedirs(os.getcwd() + '\log')
        if not os.path.isfile("./autotest.db"):
            self.cx = connect("./autotest.db")
            self.sql = self.cx.cursor()
            self.sql.execute("PRAGMA auto_vacuum = FULL")
            self.sql.execute("CREATE TABLE[conf_log]([logger_logPath] VARCHAR2, [logger_level] VARCHAR2, [logger_logMaxBytes] VARCHAR2, [logger_logBackupCount] VARCHAR2, [handler_fileHandlerLevel] VARCHAR2, [handler_screenHandlerLevel] VARCHAR2)")
            self.sql.execute("CREATE TABLE [conf_data_source] ([id] VARCHAR2, [type] VARCHAR2, [username] VARCHAR2, [password] VARCHAR2, [ip] VARCHAR2, [service_name] VARCHAR2)")
            ist_conf_1 = "INSERT INTO [conf_log] VALUES('" + os.getcwd() + "\log', 'DEBUG', '10000000', '100', 'INFO', 'INFO')"
            ist_conf_2 = "INSERT INTO [conf_data_source] VALUES('CONN_ORACLE_01', 'ORACLE', 'test', 'test', '22.117.68.132', 'orcl')"
            self.sql.execute(ist_conf_1)
            self.sql.execute(ist_conf_2)
            self.cx.commit()

InitDB()
app = wx.App(False)
frame = MyFrame()
app.MainLoop()
