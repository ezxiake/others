import time

from com.midas.tool.ConnSqlite import ConnSqlite

from com.log import PyLog


class SetOperation:
    # 构造方法
    def __init__(self):
        self.log = PyLog("SetOperation").get_log()
        self.start = time.clock()
        self.cx = ConnSqlite().get_sql()
        self.sql = self.cx.cursor()
        self.log.debug("SetOperation.py 初始化操作，链接Sqlite数据库成功")
        self.sql.execute("select a,b,c,d,e,f from T00_29700")
        self.set_29700 = set(self.sql.fetchall())

    # 结束方法
    def finish(self):
        self.cx.commit()
        self.cx.close()
        self.log.info("All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "]")

    # 可计算 0001 - 0013 静态类型（无需期号）
    def static_type_union_operation(self, optCode, optRange, opt_code):
        optRangeList = optRange.split(",", str(optRange).count(","))
        rstOptRangeSet = set()
        for orl in optRangeList:
            self.sql.execute("select a,b,c,d,e,f from t00_range where id = '" + optCode + "' and v = '" + orl + "'")
            rstOptRangeSet |= set(self.sql.fetchall())

        # 算法 s 为 设定算法； p 为 排除算法
        if opt_code == "s":  # 设定值域算法
            return rstOptRangeSet
        else:  # 排除值域算法
            return self.set_29700 - rstOptRangeSet

    # 可计算 0022（4）、0023 - 0025（5）、0741（6）、0742 - 0746（7）四种动态类型（需要期号、flag为了区分并加快查询速度）
    def dynamic_type_union_operation(self, optPeriodNum, optCode, optRange, flag, opt_code):
        optRangeList = optRange.split(",", str(optRange).count(","))
        rstOptRangeSet = set()
        for orl in optRangeList:
            self.sql.execute("select a,b,c,d,e,f from t00_range_dynamic where period = '" + optPeriodNum + "' and id = '" + optCode + "' and flag = '" + flag + "' and v = '" + orl + "'")
            rstOptRangeSet |= set(self.sql.fetchall())

        # 算法 s 为 设定算法； p 为 排除算法
        if opt_code == "s":  # 设定值域算法
            return rstOptRangeSet
        else:  # 排除值域算法
            return self.set_29700 - rstOptRangeSet

    # 获取内部规律最终集合结果，返回set类型，还要和外部的合并
    def get_inside_final_result(self, optPeriodNum, nextPeriodNum):

        v_tmp = 0
        v_up_count = 29700
        self.sql.execute("select * from t00_29700")
        inside_final_result_set = set(self.sql.fetchall())
        self.sql.execute("select 交易码,分类自己用,算法 from T03_MAPPING where 启用 = 1 order by 交易码")
        for val in self.sql.fetchall():
            v_id = val[0]
            v_flag = val[1]
            v_opt = val[2]  # 算法 s 为 设定算法； p 为 排除算法

            # self.sql.execute("select 设置值域,历史值域,排除值域,手动值域,组别 from T03_RANGE_RESULT where 开奖期号 = " + optPeriodNum + " and 交易码 = '" + v_id + "'")
            # self.sql.execute("select 设置值域,历史值域,排除值域,手动值域,组别 from T03_RANGE_RESULT where 交易码 = '" + v_id + "'")
            self.sql.execute("select 设置值域 from T03_RANGE_RESULT where 交易码 = '" + v_id + "'")
            v_set_range = self.sql.fetchone()[0]
            # v_his_range = v_rst[1]
            # v_pc_range = v_rst[2]
            # v_hand_range = v_rst[3]
            # v_group = v_rst[4]

            # self.sql.execute("select 关注遗传周期,关注边缘周期 from T03_RANGE_MIDDLE where 计算期号 = " + optPeriodNum + " and 组别 = " + str(v_group))
            # v_rst = self.sql.fetchone()
            # v_point_yc_period = v_rst[0]
            # v_point_by_period = v_rst[1]

            v_point_range = v_set_range

            if v_point_range != "":  # 修改下，利用排除值域来计算，之前用设定值域来计算会过滤的太猛    在修改下，用历史值域来试试
                if v_flag == 1 or v_flag == 2:  # 静态元数据
                    if len(inside_final_result_set) == 0:
                        inside_final_result_set = self.static_type_union_operation(v_id, v_point_range, v_opt)
                    else:
                        inside_final_result_set = inside_final_result_set & self.static_type_union_operation(v_id, v_point_range, v_opt)

                else:            # 动态元数据
                    if len(inside_final_result_set) == 0:
                        inside_final_result_set = self.dynamic_type_union_operation(optPeriodNum, v_id, v_point_range, str(v_flag), v_opt)
                    else:
                        inside_final_result_set = inside_final_result_set & self.dynamic_type_union_operation(optPeriodNum, v_id, v_point_range, str(v_flag), v_opt)

            v_after_filted_count = len(inside_final_result_set)
            v_been_filted_count = v_up_count - v_after_filted_count
            v_up_count = v_after_filted_count

            # self.sql.execute("select 红球1, 红球2, 红球3, 红球4, 红球5, 红球6 from T00_DATA_ANALYZE_INSIDE where 开奖期号 = '" + nextPeriodNum + "'")
            # target_numbers = self.sql.fetchone()
            #
            # if target_numbers in inside_final_result_set:
            #     # self.log.debug(v_id + " - " + str(v_flag) + " - 过滤后-干掉：【" + str(v_after_filted_count) + "-" + str(v_been_filted_count) + "】个  组别" + str(v_group) + "  历史值域：" + str(v_his_range) + " 目标尚在 " + str(target_numbers))
            #     self.log.debug(v_id + " - " + str(v_flag) + " - 过滤后-干掉：【" + str(v_after_filted_count) + "-" + str(v_been_filted_count) + "】个 目标尚在 " + str(target_numbers))
            # else:
            #     self.log.debug(v_id + " - " + str(v_flag) + " - 过滤后-干掉：【" + str(v_after_filted_count) + "-" + str(v_been_filted_count) + "】个 目标已出柜")
            #     if v_tmp < 1:
            #         if v_flag == 1 or v_flag == 2:  # 静态
            #             self.sql.execute("select * from T00_RANGE WHERE a='" + target_numbers[0] + "' and b='" + target_numbers[1] + "' and c='" + target_numbers[2] + "' and d='" + target_numbers[3] + "' and e='" + target_numbers[4] + "' and f='" + target_numbers[5] + "' and id='" + v_id + "'")
            #             self.log.debug(self.sql.fetchone())
            #             v_tmp += 1
            #         else:  # 动态
            #             self.sql.execute("select * from T00_RANGE_DYNAMIC WHERE a='" + target_numbers[0] + "' and b='" + target_numbers[1] + "' and c='" + target_numbers[2] + "' and d='" + target_numbers[3] + "' and e='" + target_numbers[4] + "' and f='" + target_numbers[5] + "' and id='" + v_id + "'")
            #             self.log.debug(self.sql.fetchone())
            #             v_tmp += 1
            #
            #         exit()
            #
            # if len(inside_final_result_set) == 0:
            #     self.log.error("计算错误，都干成0了")
            #     exit()
            condition = 0
            killed = str(v_been_filted_count)
            while condition < 6 - len(killed):
                killed += " "
            self.log.debug(v_id + " - " + str(v_flag) + " - 干掉： " + killed + "个，剩余： " + str(v_after_filted_count) + "个")
        self.log.debug("")
        self.log.debug("最终剩余集合数：" + str(len(inside_final_result_set)) + "个")
        self.log.debug("")
        self.log.debug(inside_final_result_set)

        self.sql.execute("SELECT 红球1,红球2,红球3,红球4,红球5,红球6 FROM T00_DATA_ANALYZE_INSIDE")
        his_model_rst = self.sql.fetchall()
        true_final_result = (val for val in inside_final_result_set if val not in his_model_rst)
        self.log.debug(his_model_rst)

        self.log.debug("在次过滤掉历史出现的模型期号后的 最终剩余集合数：" + str(len(list(true_final_result))) + "个")
        self.log.debug(list(true_final_result))



if __name__ == '__main__':
    setOpt = SetOperation()

    # v_num = 0
    # for var in setOpt.static_type_union_operation("0001", "0,1,2,3,4"):  # 测试使用
    #     print(var)
    #     v_num += 1
    # print(str(v_num))

    # v_num = 0
    # for var in setOpt.dynamic_type_union_operation("2014032", "0022", "0,1,2,3,4,5,6,7,8,9,10", "4"):  # 测试遗传总量
    #     print(var)
    #     v_num += 1
    # print(str(v_num))

    # v_num = 0
    # for var in setOpt.dynamic_type_union_operation("2014032", "0023", "0,1,2,3,4,5,6,7,8,9,10", "5"):  # 测试内部遗传比例
    #     print(var)
    #     v_num += 1
    # print(str(v_num))

    # v_num = 0
    # for var in setOpt.dynamic_type_union_operation("2014032", "0741", "0,1,2,3,4,5,6,7,8,9,10", "6"):  # 测试内部遗传比例
    #     print(var)
    #     v_num += 1
    # print(str(v_num))

    # v_num = 0
    # for var in setOpt.dynamic_type_union_operation("2014032", "0742", "0,1,2,3,4,5,6,7,8,9,10", "7"):  # 测试内部遗传比例
    #     print(var)
    #     v_num += 1
    # print(str(v_num))

    setOpt.get_inside_final_result("2014032")

    setOpt.finish()
