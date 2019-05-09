from com.handle import SetOperation
from com.handle import SourceDataOperation

srcDataOpt = SourceDataOperation()  # 实例化类对象

# srcDataOpt.tmp_replace_single_number()                  # 将T00_SET中o=1的记录中v的值中带有单位数字的补0变成双数，不然集合交集匹配不到，临时使用

srcDataOpt.get_open_award_source_data()                 # 获取"历届开奖结果"元数据(依赖于Internet)
srcDataOpt.get_model_set()                              # 获取"模型集合"(依赖开奖结果元数据:大号三个[17-33]，偶数三个[偶16奇17]，区间2-2-2[1-11][12-22][23-33],共计29700条记录)
srcDataOpt.get_statistics_value()                       # 获取"统计值"(依赖配置表t00_set)
# srcDataOpt.write_range("2017026")

# srcDataOpt.create_set_range()                           # 创建"集合值域"元数据(依赖配置表t00_set)           有删除语句
# srcDataOpt.create_every_count()                         # 创建"各项数量统计"元数据(依赖配置表t00_set)        有删除语句
# srcDataOpt.create_others()                              # 间距与位势、和值、综合常规、集合元数据(静态)        无删除语句

# srcDataOpt.init_range_dynamic_table()                   # 清空动态元数据表(# 判断T00_RANGE_DYNAMIC是否存在，存在则drop后创建，否则直接创建)
# srcDataOpt.create_heredity_total("2014146")             # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_interior_heredity_proportion("2014146")  # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成

# srcDataOpt.create_heredity_total("2007071")             # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_interior_heredity_proportion("2007071")  # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_heredity_total("2011021")             # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_interior_heredity_proportion("2011021")  # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_heredity_total("2014127")             # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_interior_heredity_proportion("2014127")  # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_heredity_total("2017016")             # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
# srcDataOpt.create_interior_heredity_proportion("2017016")  # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成

# srcDataOpt.data_checkout()                              # 校验 T00_DATA_ANALYZE_INSIDE 表与备份表中的数据前后是否一致
# srcDataOpt.xxx()
# srcDataOpt.test_set()
# srcDataOpt.easy_excel_impl()                            # 将统计数据插入excel

# srcDataOpt.init_t03_range_middle_and_detail()           # 清空值域中间表(# 判断 T03_RANGE_MIDDLE、T03_RANGE_MIDDLE_DETAIL 是否存在，存在则drop后创建，否则直接创建)
# srcDataOpt.init_t03_range_result_table()                # 清空值域结果配置表(# 判断 T03_RANGE_RESULT 是否存在，存在则drop后创建，否则直接创建)

# srcDataOpt.create_exclude_rule("2017001")               # 创建排除规则，结果装入 T03_RANGE_MIDDLE + T03_RANGE_MIDDLE_DETAIL 两张表

# srcDataOpt.create_exclude_config_for_result("2014032")  # 根据排除规则生成设定值域，为排除计算提供配置，结果装入 T03_RANGE_RESULT 一张表
# srcDataOpt.create_exclude_config_for_result("2013153")

srcDataOpt.finish()

#################################################################################################################################################

setOpt = SetOperation()                                 # 实例化类对象
# setOpt.get_inside_final_result("2013153", "2014032")               # 获取内部规律最终集合结果，返回set类型，还要和外部的合并

# setOpt.get_inside_final_result("2013153", "2014032")    # 40 - 41 - 66


# setOpt.get_inside_final_result("2014146", "2015024")    # 46 - 47 - 89
# setOpt.get_inside_final_result("2015024", "2015037")    # 47 - 48 - 60
# setOpt.get_inside_final_result("2015037", "2016021")    # 48 - 49 - 38
# setOpt.get_inside_final_result("2016021", "2016028")    # 49 - 50 - 98
# setOpt.get_inside_final_result("2016028", "2016052")    # 50 - 51 - 70
# setOpt.get_inside_final_result("2016052", "2016106")    # 51 - 52 - 32
# setOpt.get_inside_final_result("2016106", "2016117")    # 52 - 53 - 43
# setOpt.get_inside_final_result("2016117", "2017001")    # 53 - 54 ： 665 /

# setOpt.get_inside_final_result("2007071", "2007086")
# setOpt.get_inside_final_result("2011021", "2011104")
# setOpt.get_inside_final_result("2014127", "2014146")
# setOpt.get_inside_final_result("2017016", "")

# setOpt.sql.execute("SELECT 开奖期号 FROM T00_DATA_ANALYZE_INSIDE ORDER BY 开奖期号")
# print(setOpt.sql.fetchall())


setOpt.finish()
