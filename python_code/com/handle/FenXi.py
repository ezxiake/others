import time
from urllib import request
from com.tool.ConnSqlite import ConnSqlite
from com.log.PyLog import PyLog


class SourceDataOperation:
    # 构造方法
    def __init__(self):

        self.log = PyLog("FenXi").get_log()
        # self.me = EasyExcel("E:\\101 - Eclipse\\workspace_learn_python\\midas\\data\\fenxi.xlsx")
        self.start = time.clock()
        self.cx = ConnSqlite().get_sql()
        self.sql = self.cx.cursor()
        self.log.debug("FenXi.py 初始化操作，链接Sqlite数据库成功")

    # 获取历届开奖结果元数据
    def get_open_award_source_data(self):
        url = "http://www.17500.cn/getData/ssq.TXT"
        with request.urlopen(url) as web:
            with open("./../../data/ssq.dat", 'wb') as outfile:  # 二进制，防止
                outfile.write(web.read())

        f = open("./../../data/ssq.dat", "r")
        self.sql.execute("delete from t00_open_award")

        for line in f:
            tmp = str(line).replace("\n", "").split(" ", str(line).count(" "))
            ist_sql = "insert into t00_open_award values('"
            for var in tmp: ist_sql = ist_sql + var + "','"
            ist_sql = ist_sql[:len(ist_sql) - 2] + ")"
            self.sql.execute(ist_sql)

        f.close()

    # 结束方法
    def finish(self):
        self.cx.commit()
        self.cx.close()
        # self.me.save()
        # self.me.close()
        self.log.info("All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "]")

    def midas(self):

        # 预使用的list定义
        list_big_num = (17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33)
        list_small_num = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
        range3_1 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
        range3_2 = (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)
        range3_3 = (23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33)
        range4_1 = (1, 2, 3, 4, 5, 6, 7, 8)
        range4_2 = (9, 10, 11, 12, 13, 14, 15, 16)
        range4_3 = (17, 18, 19, 20, 21, 22, 23, 24)
        range4_4 = (25, 26, 27, 28, 29, 30, 31, 32, 33)
        list_prime_number = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31)

        # 分析大势 ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        # 获取100期数据写入midas,出奖号码用代替 √
        self.sql.execute("delete from midas")
        self.sql.execute("select 开奖期号,红号1,红号2,红号3,红号4,红号5,红号6 from t00_open_award order by 开奖期号 desc limit 100")
        open_award = self.sql.fetchall()
        for line in open_award:

            if len(str(int(line[1]))) == 1:
                red1 = " " + str(int(line[1]))
            else:
                red1 = line[1]
            if len(str(int(line[2]))) == 1:
                red2 = " " + str(int(line[2]))
            else:
                red2 = line[2]
            if len(str(int(line[3]))) == 1:
                red3 = " " + str(int(line[3]))
            else:
                red3 = line[3]
            if len(str(int(line[4]))) == 1:
                red4 = " " + str(int(line[4]))
            else:
                red4 = line[4]
            if len(str(int(line[5]))) == 1:
                red5 = " " + str(int(line[5]))
            else:
                red5 = line[5]
            if len(str(int(line[6]))) == 1:
                red6 = " " + str(int(line[6]))
            else:
                red6 = line[6]
            red = red1 + "  " + red2 + "  " + red3 + "  " + red4 + "  " + red5 + "  " + red6

            self.sql.execute("insert into midas (id, win_num) values(" + line[0] + ",'" + red + "')")
            for v_num in range(1, 34):
                self.sql.execute("update midas set \"" + str(v_num) + "\"= '' where id = '" + line[0] + "'")
            for v_num in range(1, 7):
                self.sql.execute("update midas set \"" + str(int(line[v_num])) + "\"= '√' where id = '" + line[0] + "'")

        # 计算遗漏
        self.sql.execute("select id,\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"8\",\"9\",\"10\",\"11\",\"12\",\"13\",\"14\",\"15\",\"16\",\"17\",\"18\",\"19\",\"20\",\"21\",\"22\",\"23\",\"24\",\"25\",\"26\",\"27\",\"28\",\"29\",\"30\",\"31\",\"32\",\"33\" from midas")
        list_id = []
        names = locals()
        for v_num in range(1, 34): names['list_%s' % v_num] = []
        for line in self.sql.fetchall():
            # 获取列存贮在数组中（更合适列的方式处理）
            list_id.append(line[0])
            for v_num in range(1, 34):
                names['list_%s' % v_num].append(line[v_num])

        # 开始一列一列的处理，计算遗漏，共33列
        yilou = 0
        for v_col_num in range(1, 34):
            v_num = 0
            for var in names['list_%s' % v_col_num]:
                if var == "√":

                    # 如果是第一行
                    if v_num == 0:
                        right_flag = "yes"
                    elif v_num == 99:
                        yilou = 0
                    elif right_flag != "yes":
                        self.sql.execute("update midas set \"" + str(v_col_num) + "\"='" + str(yilou) + "' where id = '" + str(list_id[write_num]) + "'")
                        yilou = 0
                        right_flag = 'yes'
                else:
                    # 如果是第一行
                    if v_num == 0:
                        right_flag = "no"
                        write_num = v_num
                        yilou += 1
                    elif v_num == 99:
                        yilou = 0
                    else:
                        if right_flag == "yes":
                            right_flag = "no"
                            yilou += 1
                            write_num = v_num
                        else:
                            yilou += 1
                v_num += 1

        # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
        for line in open_award:
            v_num = 0

            period_num = line[0]
            red1 = int(line[1])
            red2 = int(line[2])
            red3 = int(line[3])
            red4 = int(line[4])
            red5 = int(line[5])
            red6 = int(line[6])

            # 单双号
            if red1 % 2 == 0: v_num += 1
            if red2 % 2 == 0: v_num += 1
            if red3 % 2 == 0: v_num += 1
            if red4 % 2 == 0: v_num += 1
            if red5 % 2 == 0: v_num += 1
            if red6 % 2 == 0: v_num += 1

            self.sql.execute("update midas set single = '" + str(v_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set double = '" + str(6-v_num) + "' where id =" + str(period_num))

            if v_num == 6: self.sql.execute("update midas set \"6s0d\" = '√' where id =" + str(period_num))
            if v_num == 5: self.sql.execute("update midas set \"5s1d\" = '√' where id =" + str(period_num))
            if v_num == 4: self.sql.execute("update midas set \"4s2d\" = '√' where id =" + str(period_num))
            if v_num == 3: self.sql.execute("update midas set \"3s3d\" = '√' where id =" + str(period_num))
            if v_num == 2: self.sql.execute("update midas set \"2s4d\" = '√' where id =" + str(period_num))
            if v_num == 1: self.sql.execute("update midas set \"1s5d\" = '√' where id =" + str(period_num))
            if v_num == 0: self.sql.execute("update midas set \"0s6d\" = '√' where id =" + str(period_num))

            # 大小号
            v_num = 0
            if red1 in list_big_num: v_num += 1
            if red2 in list_big_num: v_num += 1
            if red3 in list_big_num: v_num += 1
            if red4 in list_big_num: v_num += 1
            if red5 in list_big_num: v_num += 1
            if red6 in list_big_num: v_num += 1

            self.sql.execute("update midas set big = '" + str(v_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set small = '" + str(6-v_num) + "' where id =" + str(period_num))

            if v_num == 6: self.sql.execute("update midas set \"6b0s\" = '√' where id =" + str(period_num))
            if v_num == 5: self.sql.execute("update midas set \"5b1s\" = '√' where id =" + str(period_num))
            if v_num == 4: self.sql.execute("update midas set \"4b2s\" = '√' where id =" + str(period_num))
            if v_num == 3: self.sql.execute("update midas set \"3b3s\" = '√' where id =" + str(period_num))
            if v_num == 2: self.sql.execute("update midas set \"2b4s\" = '√' where id =" + str(period_num))
            if v_num == 1: self.sql.execute("update midas set \"1b5s\" = '√' where id =" + str(period_num))
            if v_num == 0: self.sql.execute("update midas set \"0b6s\" = '√' where id =" + str(period_num))

            # 和值
            v_sum = red1 + red2 + red3 + red4 + red5 + red6
            self.sql.execute("update midas set sum = " + str(v_sum) + " where id =" + str(period_num))
            if v_sum - 102 > 0:
                self.sql.execute("update midas set \"deviate102\" = '+" + str(v_sum - 102) + "' where id =" + str(period_num))
            else:
                self.sql.execute("update midas set \"deviate102\" = '" + str(v_sum-102) + "' where id =" + str(period_num))

            # 3分区间
            v_qj_3_1_num = 0
            v_qj_3_2_num = 0
            v_qj_3_3_num = 0

            if red1 in range3_1:
                v_qj_3_1_num += 1
            elif red1 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            if red2 in range3_1:
                v_qj_3_1_num += 1
            elif red2 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            if red3 in range3_1:
                v_qj_3_1_num += 1
            elif red3 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            if red4 in range3_1:
                v_qj_3_1_num += 1
            elif red4 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            if red5 in range3_1:
                v_qj_3_1_num += 1
            elif red5 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            if red6 in range3_1:
                v_qj_3_1_num += 1
            elif red6 in range3_2:
                v_qj_3_2_num += 1
            else:
                v_qj_3_3_num += 1

            self.sql.execute("update midas set \"range3-1\" = '" + str(v_qj_3_1_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"range3-2\" = '" + str(v_qj_3_2_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"range3-3\" = '" + str(v_qj_3_3_num) + "' where id =" + str(period_num))

            # 4分区间
            v_qj_4_1_num = 0
            v_qj_4_2_num = 0
            v_qj_4_3_num = 0
            v_qj_4_4_num = 0

            if red1 in range4_1:
                v_qj_4_1_num += 1
            elif red1 in range4_2:
                v_qj_4_2_num += 1
            elif red1 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            if red2 in range4_1:
                v_qj_4_1_num += 1
            elif red2 in range4_2:
                v_qj_4_2_num += 1
            elif red2 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            if red3 in range4_1:
                v_qj_4_1_num += 1
            elif red3 in range4_2:
                v_qj_4_2_num += 1
            elif red3 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            if red4 in range4_1:
                v_qj_4_1_num += 1
            elif red4 in range4_2:
                v_qj_4_2_num += 1
            elif red4 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            if red5 in range4_1:
                v_qj_4_1_num += 1
            elif red5 in range4_2:
                v_qj_4_2_num += 1
            elif red5 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            if red6 in range4_1:
                v_qj_4_1_num += 1
            elif red6 in range4_2:
                v_qj_4_2_num += 1
            elif red6 in range4_3:
                v_qj_4_3_num += 1
            else:
                v_qj_4_4_num += 1

            self.sql.execute("update midas set \"range4-1\" = '" + str(v_qj_4_1_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"range4-2\" = '" + str(v_qj_4_2_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"range4-3\" = '" + str(v_qj_4_3_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"range4-4\" = '" + str(v_qj_4_4_num) + "' where id =" + str(period_num))

            # 除3余数
            v_rmd_3_1_num = 0
            v_rmd_3_2_num = 0
            v_rmd_3_0_num = 0

            if red1 % 3 == 1: v_rmd_3_1_num += 1
            if red1 % 3 == 2: v_rmd_3_2_num += 1
            if red1 % 3 == 0: v_rmd_3_0_num += 1

            if red2 % 3 == 1: v_rmd_3_1_num += 1
            if red2 % 3 == 2: v_rmd_3_2_num += 1
            if red2 % 3 == 0: v_rmd_3_0_num += 1

            if red3 % 3 == 1: v_rmd_3_1_num += 1
            if red3 % 3 == 2: v_rmd_3_2_num += 1
            if red3 % 3 == 0: v_rmd_3_0_num += 1

            if red4 % 3 == 1: v_rmd_3_1_num += 1
            if red4 % 3 == 2: v_rmd_3_2_num += 1
            if red4 % 3 == 0: v_rmd_3_0_num += 1

            if red5 % 3 == 1: v_rmd_3_1_num += 1
            if red5 % 3 == 2: v_rmd_3_2_num += 1
            if red5 % 3 == 0: v_rmd_3_0_num += 1

            if red6 % 3 == 1: v_rmd_3_1_num += 1
            if red6 % 3 == 2: v_rmd_3_2_num += 1
            if red6 % 3 == 0: v_rmd_3_0_num += 1

            self.sql.execute("update midas set \"remainder3-1\" = '" + str(v_rmd_3_1_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder3-2\" = '" + str(v_rmd_3_2_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder3-0\" = '" + str(v_rmd_3_0_num) + "' where id =" + str(period_num))

            # 除4余数
            v_rmd_4_1_num = 0
            v_rmd_4_2_num = 0
            v_rmd_4_3_num = 0
            v_rmd_4_0_num = 0

            if red1 % 4 == 1: v_rmd_4_1_num += 1
            if red1 % 4 == 2: v_rmd_4_2_num += 1
            if red1 % 4 == 3: v_rmd_4_3_num += 1
            if red1 % 4 == 0: v_rmd_4_0_num += 1

            if red2 % 4 == 1: v_rmd_4_1_num += 1
            if red2 % 4 == 2: v_rmd_4_2_num += 1
            if red2 % 4 == 3: v_rmd_4_3_num += 1
            if red2 % 4 == 0: v_rmd_4_0_num += 1

            if red3 % 4 == 1: v_rmd_4_1_num += 1
            if red3 % 4 == 2: v_rmd_4_2_num += 1
            if red3 % 4 == 3: v_rmd_4_3_num += 1
            if red3 % 4 == 0: v_rmd_4_0_num += 1

            if red4 % 4 == 1: v_rmd_4_1_num += 1
            if red4 % 4 == 2: v_rmd_4_2_num += 1
            if red4 % 4 == 3: v_rmd_4_3_num += 1
            if red4 % 4 == 0: v_rmd_4_0_num += 1

            if red5 % 4 == 1: v_rmd_4_1_num += 1
            if red5 % 4 == 2: v_rmd_4_2_num += 1
            if red5 % 4 == 3: v_rmd_4_3_num += 1
            if red5 % 4 == 0: v_rmd_4_0_num += 1

            if red6 % 4 == 1: v_rmd_4_1_num += 1
            if red6 % 4 == 2: v_rmd_4_2_num += 1
            if red6 % 4 == 3: v_rmd_4_3_num += 1
            if red6 % 4 == 0: v_rmd_4_0_num += 1

            self.sql.execute("update midas set \"remainder4-1\" = '" + str(v_rmd_4_1_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder4-2\" = '" + str(v_rmd_4_2_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder4-3\" = '" + str(v_rmd_4_3_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder4-0\" = '" + str(v_rmd_4_0_num) + "' where id =" + str(period_num))

            # 除6余数
            v_rmd_6_1_num = 0
            v_rmd_6_2_num = 0
            v_rmd_6_3_num = 0
            v_rmd_6_4_num = 0
            v_rmd_6_5_num = 0
            v_rmd_6_0_num = 0

            if red1 % 6 == 1: v_rmd_6_1_num += 1
            if red1 % 6 == 2: v_rmd_6_2_num += 1
            if red1 % 6 == 3: v_rmd_6_3_num += 1
            if red1 % 6 == 4: v_rmd_6_4_num += 1
            if red1 % 6 == 5: v_rmd_6_5_num += 1
            if red1 % 6 == 0: v_rmd_6_0_num += 1

            if red2 % 6 == 1: v_rmd_6_1_num += 1
            if red2 % 6 == 2: v_rmd_6_2_num += 1
            if red2 % 6 == 3: v_rmd_6_3_num += 1
            if red2 % 6 == 4: v_rmd_6_4_num += 1
            if red2 % 6 == 5: v_rmd_6_5_num += 1
            if red2 % 6 == 0: v_rmd_6_0_num += 1

            if red3 % 6 == 1: v_rmd_6_1_num += 1
            if red3 % 6 == 2: v_rmd_6_2_num += 1
            if red3 % 6 == 3: v_rmd_6_3_num += 1
            if red3 % 6 == 4: v_rmd_6_4_num += 1
            if red3 % 6 == 5: v_rmd_6_5_num += 1
            if red3 % 6 == 0: v_rmd_6_0_num += 1

            if red4 % 6 == 1: v_rmd_6_1_num += 1
            if red4 % 6 == 2: v_rmd_6_2_num += 1
            if red4 % 6 == 3: v_rmd_6_3_num += 1
            if red4 % 6 == 4: v_rmd_6_4_num += 1
            if red4 % 6 == 5: v_rmd_6_5_num += 1
            if red4 % 6 == 0: v_rmd_6_0_num += 1

            if red5 % 6 == 1: v_rmd_6_1_num += 1
            if red5 % 6 == 2: v_rmd_6_2_num += 1
            if red5 % 6 == 3: v_rmd_6_3_num += 1
            if red5 % 6 == 4: v_rmd_6_4_num += 1
            if red5 % 6 == 5: v_rmd_6_5_num += 1
            if red5 % 6 == 0: v_rmd_6_0_num += 1

            if red6 % 6 == 1: v_rmd_6_1_num += 1
            if red6 % 6 == 2: v_rmd_6_2_num += 1
            if red6 % 6 == 3: v_rmd_6_3_num += 1
            if red6 % 6 == 4: v_rmd_6_4_num += 1
            if red6 % 6 == 5: v_rmd_6_5_num += 1
            if red6 % 6 == 0: v_rmd_6_0_num += 1

            self.sql.execute("update midas set \"remainder6-1\" = '" + str(v_rmd_6_1_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder6-2\" = '" + str(v_rmd_6_2_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder6-3\" = '" + str(v_rmd_6_3_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder6-4\" = '" + str(v_rmd_6_4_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder6-5\" = '" + str(v_rmd_6_5_num) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"remainder6-0\" = '" + str(v_rmd_6_0_num) + "' where id =" + str(period_num))

            # 尾数
            # print(str(red4) + "  " + str(red4)[-1:])
            v_last_num_0 = 0
            v_last_num_1 = 0
            v_last_num_2 = 0
            v_last_num_3 = 0
            v_last_num_4 = 0
            v_last_num_5 = 0
            v_last_num_6 = 0
            v_last_num_7 = 0
            v_last_num_8 = 0
            v_last_num_9 = 0

            if int(str(red1)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red1)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red1)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red1)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red1)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red1)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red1)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red1)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red1)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red1)[-1:]) == 9: v_last_num_9 += 1

            if int(str(red2)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red2)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red2)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red2)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red2)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red2)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red2)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red2)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red2)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red2)[-1:]) == 9: v_last_num_9 += 1

            if int(str(red3)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red3)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red3)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red3)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red3)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red3)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red3)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red3)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red3)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red3)[-1:]) == 9: v_last_num_9 += 1

            if int(str(red4)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red4)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red4)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red4)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red4)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red4)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red4)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red4)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red4)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red4)[-1:]) == 9: v_last_num_9 += 1

            if int(str(red5)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red5)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red5)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red5)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red5)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red5)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red5)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red5)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red5)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red5)[-1:]) == 9: v_last_num_9 += 1

            if int(str(red6)[-1:]) == 0: v_last_num_0 += 1
            if int(str(red6)[-1:]) == 1: v_last_num_1 += 1
            if int(str(red6)[-1:]) == 2: v_last_num_2 += 1
            if int(str(red6)[-1:]) == 3: v_last_num_3 += 1
            if int(str(red6)[-1:]) == 4: v_last_num_4 += 1
            if int(str(red6)[-1:]) == 5: v_last_num_5 += 1
            if int(str(red6)[-1:]) == 6: v_last_num_6 += 1
            if int(str(red6)[-1:]) == 7: v_last_num_7 += 1
            if int(str(red6)[-1:]) == 8: v_last_num_8 += 1
            if int(str(red6)[-1:]) == 9: v_last_num_9 += 1

            self.sql.execute("update midas set \"last_num0\" = '" + str(v_last_num_0) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num1\" = '" + str(v_last_num_1) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num2\" = '" + str(v_last_num_2) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num3\" = '" + str(v_last_num_3) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num4\" = '" + str(v_last_num_4) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num5\" = '" + str(v_last_num_5) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num6\" = '" + str(v_last_num_6) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num7\" = '" + str(v_last_num_7) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num8\" = '" + str(v_last_num_8) + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"last_num9\" = '" + str(v_last_num_9) + "' where id =" + str(period_num))

            # 质数 list_prime_number
            v_prime_num_count = 0
            v_prime_nums = ""

            if red1 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red1)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red1)

            if red2 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red2)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red2)

            if red3 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red3)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red3)

            if red4 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red4)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red4)

            if red5 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red5)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red5)

            if red6 in list_prime_number:
                v_prime_num_count += 1
                if v_prime_nums == "":
                    v_prime_nums = str(red6)
                else:
                    v_prime_nums = v_prime_nums + "  " + str(red6)

            self.sql.execute("update midas set \"prime_num\" = '" + v_prime_nums + "' where id =" + str(period_num))
            self.sql.execute("update midas set \"prime_num_count\" = '" + str(v_prime_num_count) + "' where id =" + str(period_num))

            # 连号 border_num
            v_vorder_num = ""
            list_vorder_nums = []
            if red1 == red2 - 1:
                list_vorder_nums.append(red1)
                list_vorder_nums.append(red2)
            if red2 == red3 - 1:
                list_vorder_nums.append(red2)
                list_vorder_nums.append(red3)
            if red3 == red4 - 1:
                list_vorder_nums.append(red3)
                list_vorder_nums.append(red4)
            if red4 == red5 - 1:
                list_vorder_nums.append(red4)
                list_vorder_nums.append(red5)
            if red5 == red6 - 1:
                list_vorder_nums.append(red5)
                list_vorder_nums.append(red6)

            self.sql.execute("update midas set \"border_num\" = '" + str(sorted(set(list_vorder_nums))).replace(",", " ").replace("[", "").replace("]", "").replace("set()", "") + "' where id =" + str(period_num))

            # 邻号 neighbor_num
            list_neighbor_num = []
            if red1 == 1:
                list_neighbor_num.append(2)
            else:
                list_neighbor_num.append(red1-1)
                list_neighbor_num.append(red1+1)

            list_neighbor_num.append(red2 - 1)
            list_neighbor_num.append(red2 + 1)
            list_neighbor_num.append(red3 - 1)
            list_neighbor_num.append(red3 + 1)
            list_neighbor_num.append(red4 - 1)
            list_neighbor_num.append(red4 + 1)
            list_neighbor_num.append(red5 - 1)
            list_neighbor_num.append(red5 + 1)

            if red6 == 33:
                list_neighbor_num.append(32)
            else:
                list_neighbor_num.append(red6-1)
                list_neighbor_num.append(red6+1)

            self.sql.execute("update midas set \"neighbor_num\" = '" + str(sorted(set(list_neighbor_num))).replace(",", " ").replace("[", "").replace("]", "").replace("set()", "") + "' where id =" + str(period_num))

        # 邻号命中计算 neighbor_num_bingo ----------------------------------------------------------
        self.sql.execute("select id from midas order by id desc")
        # print(self.sql.fetchall())
        list_p_num = []
        for p_num in self.sql.fetchall():
            list_p_num.append(p_num[0])
        for x, y in enumerate(list_p_num):
            if x == 99: break
            self.sql.execute("select win_num, neighbor_num from midas where id <= " + str(y) + " order by id desc limit 2")
            tmp1 = self.sql.fetchone()[0]
            tmp2 = self.sql.fetchone()[1]
            v_present = tmp1.split("  ", tmp1.count("  "))
            v_up = tmp2.split("  ", tmp2.count("  "))

            rst = sorted(var for var in v_present if var in v_up)
            self.sql.execute("update midas set \"neighbor_num_bingo\" = '" + str(rst).replace("'", "").replace(",", " ").replace("[", "").replace("]", "") + "' where id =" + str(y))

        # 计算热、温、冷号 --------------------------------------------------------------------------
        names = locals()
        for v_num in range(1, 34): names['array%s' % v_num] = []

        for line in open_award:
            names['array%s' % int(line[1])].append(int(line[1]))
            names['array%s' % int(line[2])].append(int(line[2]))
            names['array%s' % int(line[3])].append(int(line[3]))
            names['array%s' % int(line[4])].append(int(line[4]))
            names['array%s' % int(line[5])].append(int(line[5]))
            names['array%s' % int(line[6])].append(int(line[6]))

        # 将长度的类型装入set，达到去重的效果
        set_num_count = set()
        for v_num in range(1, 34):
            set_num_count.add(len(names['array%s' % v_num]))

        # 倒序排序set
        list_num_count = list(sorted(set_num_count))
        list_num_count.reverse()
        # print(list_num_count)

        # 定义list
        for v_num in set_num_count: names['list_num%s' % v_num] = []

        # 装载值
        for v_num in range(1, 34):
            names['list_num%s' % len(names['array%s' % v_num])].append(v_num)

        # 输入到日志（当确认热温冷号的临界点后，手动修改参数打印到日志）
        self.log.info("")
        for v_num in list_num_count: self.log.info(str(v_num) + " - " + str(names['list_num%s' % v_num]))

        # 手动设参，输出热温冷号集合 start
        v_hot_conf = 5
        v_warm_conf = 4
        v_cold_conf = 3

        list_hot = []
        list_warm = []
        list_cold = []

        v_count = 0
        for v_num in list_num_count:
            if 0 <= v_count < v_hot_conf:
                list_hot += names['list_num%s' % v_num]
            elif v_hot_conf <= v_count < v_hot_conf + v_warm_conf:
                list_warm += names['list_num%s' % v_num]
            else:
                list_cold += names['list_num%s' % v_num]
            v_count += 1

        self.log.info("")
        self.log.info("以下热温冷号元素信息需要手动设置参数后，并清除掉注释后方可输出")
        self.log.info(sorted(list_hot))
        self.log.info(sorted(list_warm))
        self.log.info(sorted(list_cold))

        # 根据上面计算出的热温冷号集合来计算统计表中的列
        for line in open_award:

            list_hot_val = []
            list_warm_val = []
            list_cold_val = []

            if int(line[1]) in list_hot: list_hot_val.append(line[1])
            if int(line[2]) in list_hot: list_hot_val.append(line[2])
            if int(line[3]) in list_hot: list_hot_val.append(line[3])
            if int(line[4]) in list_hot: list_hot_val.append(line[4])
            if int(line[5]) in list_hot: list_hot_val.append(line[5])
            if int(line[6]) in list_hot: list_hot_val.append(line[6])

            if int(line[1]) in list_warm: list_warm_val.append(line[1])
            if int(line[2]) in list_warm: list_warm_val.append(line[2])
            if int(line[3]) in list_warm: list_warm_val.append(line[3])
            if int(line[4]) in list_warm: list_warm_val.append(line[4])
            if int(line[5]) in list_warm: list_warm_val.append(line[5])
            if int(line[6]) in list_warm: list_warm_val.append(line[6])

            if int(line[1]) in list_cold: list_cold_val.append(line[1])
            if int(line[2]) in list_cold: list_cold_val.append(line[2])
            if int(line[3]) in list_cold: list_cold_val.append(line[3])
            if int(line[4]) in list_cold: list_cold_val.append(line[4])
            if int(line[5]) in list_cold: list_cold_val.append(line[5])
            if int(line[6]) in list_cold: list_cold_val.append(line[6])

            # self.log.info(list_hot_val)
            # self.log.info(list_warm_val)
            # self.log.info(list_cold_val)

            self.sql.execute("update midas set \"hot\" = '" + str(list_hot_val).replace("'", "").replace(",", " ").replace("[", "").replace("]", "") + "' where id =" + str(line[0]))
            self.sql.execute("update midas set \"hot_count\" = '" + str(len(list_hot_val)) + "' where id =" + str(line[0]))

            self.sql.execute("update midas set \"warm\" = '" + str(list_warm_val).replace("'", "").replace(",", " ").replace("[", "").replace("]", "") + "' where id =" + str(line[0]))
            self.sql.execute("update midas set \"warm_count\" = '" + str(len(list_warm_val)) + "' where id =" + str(line[0]))

            self.sql.execute("update midas set \"cold\" = '" + str(list_cold_val).replace("'", "").replace(",", " ").replace("[", "").replace("]", "") + "' where id =" + str(line[0]))
            self.sql.execute("update midas set \"cold_count\" = '" + str(len(list_cold_val)) + "' where id =" + str(line[0]))

    def rst(self):
        self.sql.execute("select 红号1, 红号2, 红号3, 红号4, 红号5, 红号6 from T00_OPEN_AWARD order by 开奖期号 desc limit 1")
        open_num = self.sql.fetchone()
        self.sql.execute("select id, num from my_buy")
        for line in self.sql.fetchall():
            # list_my_buy = map(int, line[1].split(" ", line[1].count(" ")))
            list_my_buy = line[1].split(" ", line[1].count(" "))
            # print(list_my_buy)
            # print(open_num)
            self.sql.execute("update my_buy set cnt = " + str(len(list((var for var in list_my_buy if var in open_num)))) + " where id =" + str(line[0]))

        # self.sql.execute("select 红号1,红号2,红号3,红号4,红号5,红号6 from T00_OPEN_AWARD")
        # a = self.sql.fetchall()
        self.sql.execute("select * from my_buy")
        b = self.sql.fetchall()
        for var1 in b:
            # print(line[1])
            tmp = var1[1].split(" ", var1[1].count(" "))
            print(tmp)
            # for var2 in a:
            #     # print(tmp)
            #     # print(list(var2))
            #     # print("===============")
            #     if list(var2) in tmp:
            #         print(tmp)





if __name__ == '__main__':
    csr = SourceDataOperation()  # 实例化类对象

    csr.get_open_award_source_data()
    # csr.midas()
    csr.rst()  # 兑奖，先要获取T00_OPEN_AWARD
    csr.finish()
