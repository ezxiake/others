import time
from urllib import request

import com.midas.tool.PublicObject as po
from com.midas.tool.ConnSqlite import ConnSqlite

from com.log import PyLog


class SourceDataOperation:
    # 构造方法
    def __init__(self):
        self.log = PyLog("SourceDataOperation").get_log()
        # self.me = EasyExcel("E:\\101 - Eclipse\\workspace_learn_python\\midas\\data\\ssq.xlsx")
        self.start = time.clock()
        self.cx = ConnSqlite().get_sql()
        self.sql = self.cx.cursor()
        self.log.debug("SourceDataOperation.py 初始化操作，链接Sqlite数据库成功")

    # 集合值域元数据（静态）
    def create_set_range(self):
        # 根据交易码查询集合中的数据 -> setb
        self.sql.execute("select id,v from t00_set where o='1' order by id")
        for seta in self.sql.fetchall():  # ('0001','01 15 18 32')
            trancode = seta[0]  # '0001'
            setb = seta[1].split(' ', seta[1].count(' '))  # ['01','15','18','32']

            # 先删除该交易码对应的已生成的数据，避免数据重复
            self.sql.execute("delete from t00_range where id='" + trancode + "'")

            # 查询出原始模型数据29700条，并以此循环
            self.sql.execute("select * from t00_29700")
            for line in self.sql.fetchall():  # ['01', '02', '12', '17', '23', '24'] 29700个

                # 交集处理得出交集个数，然后将结果和模型值插入元数据库t00_range
                setc = [var for var in setb if var in line]
                self.sql.execute("insert into t00_range values('" + trancode + "','" + str(len(setc)) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

    # 各项数量统计元数据（静态）
    def create_every_count(self):
        # 根据交易码查询集合中的数据 -> setb
        self.sql.execute("select id,v from t00_set where o='2' order by id")
        for seta in self.sql.fetchall():  # ['0009',''0001','0002','0003','0004','0005','0006','0007','0008' 0']
            trancode = seta[0]  # '0009'
            setb = seta[1].split(' ', seta[1].count(' '))  # [''0001','0002','0003','0004','0005','0006','0007','0008'','0']

            # 先删除该交易码对应的已生成的数据，避免数据重复
            self.sql.execute("delete from t00_range where id='" + trancode + "'")

            # 查询出原始模型数据29700条，并以此循环处理
            self.sql.execute("select * from t00_29700")
            for line in self.sql.fetchall():  # ['01', '02', '12', '17', '23', '24'] 29700个

                # 获取各统计原始集合配置
                v_count = 0
                self.sql.execute("select v from t00_set where id in (" + setb[0] + ")")
                for setc in self.sql.fetchall():  # ['01 15 18 32'] 配置几个循环几个，例如001-008的，那么就是8次
                    setd = setc[0].split(' ', setc[0].count(' '))  # ['01','15','18','32']

                    # 交集处理得出交集个数，遇到交集个数符合预期值得，计数器+1
                    sete = [var for var in setd if var in line]
                    if len(sete) == int(setb[1]): v_count += 1
                # 将计数后的结果和模型值插入元数据库 t00_range
                self.sql.execute(
                    "insert into t00_range values('" + trancode + "','" + str(v_count) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

    # 间距与位势、和值、综合常规、集合元数据（静态）
    def create_others(self):
        self.sql.execute("select a,b,c,d,e,f from t00_29700")
        result = self.sql.fetchall()

        for line in result:
            # 位势 0686 - 0691
            self.sql.execute("insert into t00_range values('0686','" + line[0] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0687','" + line[1] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0688','" + line[2] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0689','" + line[3] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0690','" + line[4] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0691','" + line[5] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

            # 间距 0693 - 0698
            # 将红球01-33顺时针排列成圈，然后计算各个相邻号码在这个圈中间隔的号码个数
            # 即相邻号码间距为两相邻号码只差减1，如12与16，间距为16-12-1=3；
            # 33与01视为相连，即间距为0
            # 第6个号码与第一个号码间距称为1，第2个与第3个称为2...
            self.sql.execute("insert into t00_range values('0693','" + str(33 - int(line[5]) + int(line[0]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0694','" + str(int(line[1]) - int(line[0]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0695','" + str(int(line[2]) - int(line[1]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0696','" + str(int(line[3]) - int(line[2]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0697','" + str(int(line[4]) - int(line[3]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0698','" + str(int(line[5]) - int(line[4]) - 1) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

            # 间距的重复项和间距特征 0700 - 0701
            #  计算模型间距，放入list
            modelGap = [str(33 - int(line[5]) + int(line[0]) - 1), str(int(line[1]) - int(line[0]) - 1), str(int(line[2]) - int(line[1]) - 1), str(int(line[3]) - int(line[2]) - 1), str(int(line[4]) - int(line[3]) - 1), str(int(line[5]) - int(line[4]) - 1)]

            setc = list(set(modelGap))  # 排序+去重
            chongfuxiang = []
            jianjutezheng = []
            for setd in setc:  # 遍历排序去重后的list ['0','1','5','8','12']
                v_count = 0
                for sete in modelGap:  # 遍历查询出的list
                    if setd == sete: v_count += 1
                if v_count > 1:
                    chongfuxiang.append(setd)
                    jianjutezheng.append(str(v_count))
            if len(chongfuxiang) == 0: jianjutezheng.append("0")

            setf = list(sorted(set(map(int, chongfuxiang))))
            setg = list(sorted(jianjutezheng))
            seti = ""
            setj = ""
            for seth in range(0, len(setf)):
                if seti != "":
                    seti = seti + "&" + str(setf[seth])
                else:
                    seti = str(setf[seth])
            for setk in range(0, len(setg)):
                if setj != "":
                    setj = setj + "+" + setg[setk]
                else:
                    setj = setg[setk]

            if seti == "": seti = '-'
            if setj == "0": setj = '-'

            self.sql.execute("insert into t00_range values('0700','" + seti + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            self.sql.execute("insert into t00_range values('0701','" + setj + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

            # 和值 0702 - 0720
            #  0702 二区和值
            self.sql.execute("insert into t00_range values('0702','" + str(sum(map(int, (val for val in line if val in po.sectionTwoSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0703 三区和值
            self.sql.execute("insert into t00_range values('0703','" + str(sum(map(int, (val for val in line if val in po.sectionThreeSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0704 小号和值
            self.sql.execute("insert into t00_range values('0704','" + str(sum(map(int, (val for val in line if val not in po.bigNumberSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0705 一区和值
            self.sql.execute("insert into t00_range values('0705','" + str(sum(map(int, (val for val in line if val in po.sectionOneSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0706 邻号间距和
            self.sql.execute("insert into t00_range values('0706','" + str(int(line[5]) - int(line[0])) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0707 大号和值
            self.sql.execute("insert into t00_range values('0707','" + str(sum(map(int, (val for val in line if val in po.bigNumberSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0708 尾号位积和（1*a+2*b+3*c+4*d+5*e+6*f）
            self.sql.execute("insert into t00_range values('0708','" + str(sum((int(line[0][1:]) * 1, int(line[1][1:]) * 2, int(line[2][1:]) * 3, int(line[3][1:]) * 4, int(line[4][1:]) * 5, int(line[5][1:]) * 6))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0709 奇号和值
            self.sql.execute("insert into t00_range values('0709','" + str(sum(map(int, (val for val in line if val in po.oddNumberSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0710 偶号和值
            self.sql.execute("insert into t00_range values('0710','" + str(sum(map(int, (val for val in line if val not in po.oddNumberSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0711 质号和值
            self.sql.execute("insert into t00_range values('0711','" + str(sum(map(int, (val for val in line if val in po.primeNumberSet)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0712 除6余数和
            self.sql.execute("insert into t00_range values('0712','" + str(sum((int(line[0]) % 6, int(line[1]) % 6, int(line[2]) % 6, int(line[3]) % 6, int(line[4]) % 6, int(line[5]) % 6))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0713 除7余数和
            self.sql.execute("insert into t00_range values('0713','" + str(sum((int(line[0]) % 7, int(line[1]) % 7, int(line[2]) % 7, int(line[3]) % 7, int(line[4]) % 7, int(line[5]) % 7))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0714 号码和尾值
            self.sql.execute("insert into t00_range values('0714','" + str(int(line[0]) + int(line[1]) + int(line[2]) + int(line[3]) + int(line[4]) + int(line[5]))[-1:] + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0715 首位和值
            self.sql.execute("insert into t00_range values('0715','" + str(sum(map(int, (val[0:1] for val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0716 除3余数和
            self.sql.execute("insert into t00_range values('0716','" + str(sum((int(line[0]) % 3, int(line[1]) % 3, int(line[2]) % 3, int(line[3]) % 3, int(line[4]) % 3, int(line[5]) % 3))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0717 除4余数和
            self.sql.execute("insert into t00_range values('0717','" + str(sum((int(line[0]) % 4, int(line[1]) % 4, int(line[2]) % 4, int(line[3]) % 4, int(line[4]) % 4, int(line[5]) % 4))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0718 除5余数和
            self.sql.execute("insert into t00_range values('0718','" + str(sum((int(line[0]) % 5, int(line[1]) % 5, int(line[2]) % 5, int(line[3]) % 5, int(line[4]) % 5, int(line[5]) % 5))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0719 除8余数和
            self.sql.execute("insert into t00_range values('0719','" + str(sum((int(line[0]) % 8, int(line[1]) % 8, int(line[2]) % 8, int(line[3]) % 8, int(line[4]) % 8, int(line[5]) % 8))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0720 除9余数和
            self.sql.execute("insert into t00_range values('0720','" + str(sum((int(line[0]) % 9, int(line[1]) % 9, int(line[2]) % 9, int(line[3]) % 9, int(line[4]) % 9, int(line[5]) % 9))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

            # 综合常规统计： 0721 - 0740
            #  0721 AC值
            acValue_0721 = str(len(list({int(line[1]) - int(line[0]), int(line[2]) - int(line[0]), int(line[3]) - int(line[0]), int(line[4]) - int(line[0]), int(line[5]) - int(line[0]), int(line[2]) - int(line[1]), int(line[3]) - int(line[1]), int(line[4]) - int(line[1]), int(line[5]) - int(line[1]), int(line[3]) - int(line[2]), int(line[4]) - int(line[2]), int(line[5]) - int(line[2]), int(line[4]) - int(line[3]), int(line[5]) - int(line[3]), int(line[5]) - int(line[4])})) - 5)
            self.sql.execute("insert into t00_range values('0721','" + acValue_0721 + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0722 最大号码
            self.sql.execute("insert into t00_range values('0722','" + str(line[5]) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0723 极号间距
            self.sql.execute("insert into t00_range values('0723','" + str(int(line[5]) - int(line[0])) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0724 最大邻距
            self.sql.execute("insert into t00_range values('0724','" + str(list(sorted((int(line[5]) - int(line[4]), int(line[4]) - int(line[3]), int(line[3]) - int(line[2]), int(line[2]) - int(line[1]), int(line[1]) - int(line[0]))))[4]) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0725 号码和值
            self.sql.execute("insert into t00_range values('0725','" + str(sum(map(int, line))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0726 尾数和值
            self.sql.execute("insert into t00_range values('0726','" + str(sum(map(int, (val[1:] for val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0727 最小号码
            self.sql.execute("insert into t00_range values('0727','" + str(line[0]) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0728 尾数组数
            self.sql.execute("insert into t00_range values('0728','" + str(len(list({line[0][1], line[1][1], line[2][1], line[3][1], line[4][1], line[5][1]}))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0729 奇号连续
            oddNumContinuousCount = 0
            if int(line[0]) % 2 != 0 and int(line[1]) % 2 != 0: oddNumContinuousCount += 1
            if int(line[1]) % 2 != 0 and int(line[2]) % 2 != 0: oddNumContinuousCount += 1
            if int(line[2]) % 2 != 0 and int(line[3]) % 2 != 0: oddNumContinuousCount += 1
            if int(line[3]) % 2 != 0 and int(line[4]) % 2 != 0: oddNumContinuousCount += 1
            if int(line[4]) % 2 != 0 and int(line[5]) % 2 != 0: oddNumContinuousCount += 1
            self.sql.execute("insert into t00_range values('0729','" + str(oddNumContinuousCount) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0730 偶号连续
            evenNumContinuousCount = 0
            if int(line[0]) % 2 == 0 and int(line[1]) % 2 == 0: evenNumContinuousCount += 1
            if int(line[1]) % 2 == 0 and int(line[2]) % 2 == 0: evenNumContinuousCount += 1
            if int(line[2]) % 2 == 0 and int(line[3]) % 2 == 0: evenNumContinuousCount += 1
            if int(line[3]) % 2 == 0 and int(line[4]) % 2 == 0: evenNumContinuousCount += 1
            if int(line[4]) % 2 == 0 and int(line[5]) % 2 == 0: evenNumContinuousCount += 1
            self.sql.execute("insert into t00_range values('0730','" + str(evenNumContinuousCount) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0731 最小邻距
            self.sql.execute("insert into t00_range values('0731','" + str(list(sorted((int(line[5]) - int(line[4]), int(line[4]) - int(line[3]), int(line[3]) - int(line[2]), int(line[2]) - int(line[1]), int(line[1]) - int(line[0]))))[0]) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0732 质号个数
            self.sql.execute("insert into t00_range values('0732','" + str(len(list(val for val in line if val in po.primeNumberSet))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

            # 0734 质号连续
            primeNumContinuousCount = 0
            if line[0] in po.primeNumberSet and line[1] in po.primeNumberSet: primeNumContinuousCount += 1
            if line[1] in po.primeNumberSet and line[2] in po.primeNumberSet: primeNumContinuousCount += 1
            if line[2] in po.primeNumberSet and line[3] in po.primeNumberSet: primeNumContinuousCount += 1
            if line[3] in po.primeNumberSet and line[4] in po.primeNumberSet: primeNumContinuousCount += 1
            if line[4] in po.primeNumberSet and line[5] in po.primeNumberSet: primeNumContinuousCount += 1
            self.sql.execute("insert into t00_range values('0734','" + str(primeNumContinuousCount) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0735 连号个数
            ContinuousNumCount = 0
            if int(line[0]) + 1 == int(line[1]): ContinuousNumCount += 1
            if int(line[1]) + 1 == int(line[2]): ContinuousNumCount += 1
            if int(line[2]) + 1 == int(line[3]): ContinuousNumCount += 1
            if int(line[3]) + 1 == int(line[4]): ContinuousNumCount += 1
            if int(line[4]) + 1 == int(line[5]): ContinuousNumCount += 1
            self.sql.execute("insert into t00_range values('0735','" + str(ContinuousNumCount) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0736 大奇个数
            self.sql.execute("insert into t00_range values('0736','" + str(len(list((val for val in po.bigOddSet if val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0737 小奇个数
            self.sql.execute("insert into t00_range values('0737','" + str(len(list((val for val in po.smallOddSet if val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0738 大偶个数
            self.sql.execute("insert into t00_range values('0738','" + str(len(list((val for val in po.bigEvenSet if val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0739 小偶个数
            self.sql.execute("insert into t00_range values('0739','" + str(len(list((val for val in po.smallEvenSet if val in line)))) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")
            #  0740 号码散度
            numDvg1 = list(sorted((int(line[1]) - int(line[0]), int(line[2]) - int(line[0]), int(line[3]) - int(line[0]), int(line[4]) - int(line[0]), int(line[5]) - int(line[0]))))[0]
            numDvg2 = list(sorted((int(line[1]) - int(line[0]), int(line[2]) - int(line[1]), int(line[3]) - int(line[1]), int(line[4]) - int(line[1]), int(line[5]) - int(line[1]))))[0]
            numDvg3 = list(sorted((int(line[2]) - int(line[0]), int(line[2]) - int(line[1]), int(line[3]) - int(line[2]), int(line[4]) - int(line[2]), int(line[5]) - int(line[2]))))[0]
            numDvg4 = list(sorted((int(line[3]) - int(line[0]), int(line[3]) - int(line[1]), int(line[3]) - int(line[2]), int(line[4]) - int(line[3]), int(line[5]) - int(line[3]))))[0]
            numDvg5 = list(sorted((int(line[4]) - int(line[0]), int(line[4]) - int(line[1]), int(line[4]) - int(line[2]), int(line[4]) - int(line[3]), int(line[5]) - int(line[4]))))[0]
            numDvg6 = list(sorted((int(line[5]) - int(line[0]), int(line[5]) - int(line[1]), int(line[5]) - int(line[2]), int(line[5]) - int(line[3]), int(line[5]) - int(line[4]))))[0]
            numberDivergence = list(sorted((numDvg1, numDvg2, numDvg3, numDvg4, numDvg5, numDvg6)))[5]
            self.sql.execute("insert into t00_range values('0740','" + str(numberDivergence) + "','" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "')")

    # 遗传总量元数据（动态）
    def create_heredity_total(self, opt_period_num):

        # 负责自动遍历各个开奖周期号部分注释掉，传入哪期动态计算哪期(ps:"create_interior_heredity_proportion"也一样，但是删掉了这里保留一份即可)
        # self.sql.execute("SELECT \"开奖期号\" FROM T00_DATA_ANALYZE_INSIDE")
        # result_period_num = self.sql.fetchall()
        # self.sql.execute("select period from t00_range_dynamic where flag='4' group by period")
        # result_created_period_num = self.sql.fetchall()
        # list_period_num = []
        # list_created_period_num = []
        # for period_num in result_period_num: list_period_num.append(period_num[0])
        # for created_period_num in result_created_period_num: list_created_period_num.append(str(created_period_num[0]))
        # list_result = list((var for var in list_period_num if var not in list_created_period_num))
        #
        # if len(list_result) != 0:
        #     for opt_period_num in list_result:

        #  读取原始模型中的29700条记录循环处理
        self.sql.execute("select * from t00_29700")
        rst_model_data = self.sql.fetchall()  # [('01', '02', '12', '17', '23', '24'), ('01', '02', '12', '17', '23', '26')...] 29700个

        # 开始计算遗传总量（1-3章比较有规律，根据t00_set配置表中 o 为 4 的配置计算；4章后都是手动写死计算，没有多少，从0692开始）
        #  计算1-3章的遗传总量
        self.sql.execute("select id,v from t00_set where o='4' order by id")
        for seta in self.sql.fetchall():  # ['0022'] ['0001','0002','0003','0004','0005','0006','0007','0008' '0014','0015','0016','0017','0018','0019','0020','0021'] 个数根据配置来定
            setb = seta[1].split(" ", seta[1].count(" "))  # ['0001','0002','0003','0004','0005','0006','0007','0008'] ['0014','0015','0016','0017','0018','0019','0020','0021']

            self.log.debug("正在计算" + opt_period_num + "期：" + seta[0])

            # 获取当期开奖结果集合值域 setc
            self.sql.execute("select " + setb[0].replace("'", "\"") + " from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
            for setc in self.sql.fetchall(): pass  # ['1','2','0','1','0','1','2','2'] 一条记录      等待和下面与seth做比较

            # 获取各统计原始集合配置
            self.sql.execute("select v from t00_set where id in (" + setb[0] + ") order by id")
            rst_config_data = self.sql.fetchall()  # [('01 15 18 32'), ('02 14 19 31')...('08 16 17 25')]

            for setd in rst_model_data:  # ['01', '02', '12', '17', '23', '24'] 29700个

                # 统计每条模型记录的集合值域 seth
                seth = []
                for sete in rst_config_data:  # ['01 15 18 32'] 配置几个循环几个，例如001-008的，那么就是8次
                    setf = sete[0].split(" ", sete[0].count(" "))  # ['01','15','18','32']
                    setg = [var for var in setf if var in setd]
                    seth.append(str(len(setg)))  # ['0','0','0','0','2','2','0','1'] 每一个模型的集合值域统计

                # 比较 setc 和 seth,获取对应相等得个数，然后将个数和模型插入动态元数据表
                v_num = 0
                for v_len in range(0, len(setc)):
                    if setc[v_len] == seth[v_len]: v_num += 1
                self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','" + seta[0] + "','" + str(v_num) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','4')")

        self.log.debug("正在计算" + opt_period_num + "期：0692")

        #  计算4章后的 0692 （位势遗传项数）（非对应式匹配，而是集合式匹配，与书中不同；在0692统计计算时也需要采用集合式匹配）
        #   获取当期开奖结果集合值域 setc
        self.sql.execute("select \"0686\",\"0687\",\"0688\",\"0689\",\"0690\",\"0691\" from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
        setc = self.sql.fetchone()
        for setd in rst_model_data:  # ['01', '02', '12', '17', '23', '24'] 29700个
            sete = list((var for var in setc if var in setd))
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0692','" + str(len(sete)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','4')")

        # 计算4章后的 0699 （间距遗传项数）
        #   获取当期开奖结果集合值域 setc
        self.sql.execute("select \"0693\",\"0694\",\"0695\",\"0696\",\"0697\",\"0698\" from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
        setc = self.sql.fetchone()
        for setd in rst_model_data:  # ['01', '02', '12', '17', '23', '24'] 29700个
            # 计算每个模型的间距值，放入list，准备和上面的setc 1 1 对比计算遗传个数（相等的）
            sete = [str(33 - int(setd[5]) + int(setd[0]) - 1), str(int(setd[1]) - int(setd[0]) - 1), str(int(setd[2]) - int(setd[1]) - 1), str(int(setd[3]) - int(setd[2]) - 1), str(int(setd[4]) - int(setd[3]) - 1), str(int(setd[5]) - int(setd[4]) - 1)]
            v_num = 0
            for v_len in range(0, len(setc)):
                if setc[v_len] == sete[v_len]: v_num += 1
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0699','" + str(v_num) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','4')")

        # 计算4章后的 0733 （常规统计遗传项数）
        #   获取当期开奖结果集合值域 setc
        self.sql.execute("select \"0725\",\"0726\",\"0727\",\"0728\",\"0729\",\"0730\",\"0731\",\"0732\" from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
        setc = self.sql.fetchone()
        for setd in rst_model_data:  # ['01', '02', '12', '17', '23', '24'] 29700个

            #  0729 奇号连续计算（不能一条语句计算出）
            oddNumContinuousCount = 0
            if int(setd[0]) % 2 != 0 and int(setd[1]) % 2 != 0: oddNumContinuousCount += 1
            if int(setd[1]) % 2 != 0 and int(setd[2]) % 2 != 0: oddNumContinuousCount += 1
            if int(setd[2]) % 2 != 0 and int(setd[3]) % 2 != 0: oddNumContinuousCount += 1
            if int(setd[3]) % 2 != 0 and int(setd[4]) % 2 != 0: oddNumContinuousCount += 1
            if int(setd[4]) % 2 != 0 and int(setd[5]) % 2 != 0: oddNumContinuousCount += 1

            #  0730 偶号连续计算（不能一条语句计算出）
            evenNumContinuousCount = 0
            if int(setd[0]) % 2 == 0 and int(setd[1]) % 2 == 0: evenNumContinuousCount += 1
            if int(setd[1]) % 2 == 0 and int(setd[2]) % 2 == 0: evenNumContinuousCount += 1
            if int(setd[2]) % 2 == 0 and int(setd[3]) % 2 == 0: evenNumContinuousCount += 1
            if int(setd[3]) % 2 == 0 and int(setd[4]) % 2 == 0: evenNumContinuousCount += 1
            if int(setd[4]) % 2 == 0 and int(setd[5]) % 2 == 0: evenNumContinuousCount += 1

            # 将计算结果整合成list，然后和setc 1 1 对比计算遗传个数（相等的）
            sete = [str(sum(map(int, setd))), str(sum(map(int, (val[1:] for val in setd)))), setd[0], str(len(list({setd[0][1], setd[1][1], setd[2][1], setd[3][1], setd[4][1], setd[5][1]}))), str(oddNumContinuousCount), str(evenNumContinuousCount), str(list(sorted((int(setd[5]) - int(setd[4]), int(setd[4]) - int(setd[3]), int(setd[3]) - int(setd[2]), int(setd[2]) - int(setd[1]), int(setd[1]) - int(setd[0]))))[0]), str(len(list(val for val in setd if val in po.primeNumberSet)))]

            v_num = 0
            for v_len in range(0, len(setc)):
                if setc[v_len] == sete[v_len]: v_num += 1
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0733','" + str(v_num) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','4')")

        # 计算4章后的 (集合)： 0741 - 0747
        # gannHotLineRedBallShowProportion 计算江恩热线红球中出比例
        self.sql.execute("select \"0686\",\"0687\",\"0688\",\"0689\",\"0690\",\"0691\" from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
        priorPeriodNumber = self.sql.fetchone()  # 保存欲计算期号的号码（上期号码）
        self.sql.execute("select \"开奖期号\",\"01\",\"02\",\"03\",\"04\",\"05\",\"06\",\"07\",\"08\",\"09\",\"10\",\"11\",\"12\",\"13\",\"14\",\"15\",\"16\",\"17\",\"18\",\"19\",\"20\",\"21\",\"22\",\"23\",\"24\",\"25\",\"26\",\"27\",\"28\",\"29\",\"30\",\"31\",\"32\",\"33\" from t00_data_analyze_inside where 开奖期号 <= '" + opt_period_num + "' order by 开奖期号")
        modelPeriodNumber = self.sql.fetchall()
        self.sql.execute("select \"0742\",\"0743\",\"0744\",\"0745\",\"0746\" from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
        priorBeOptSet = self.sql.fetchone()  # 保存欲计算期号的集合统计值（上期）
        for setd in rst_model_data:  # 模型期号号码（当前期号）
            # 计算0741 江恩热线红球中出比例
            gannHotLineNumber = []
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn1))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn1
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn2))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn2
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn3))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn3
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn4))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn4
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn5))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn5
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn6))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn6
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow1))) >= 2: gannHotLineNumber += po.gannHotLineSetRow1
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow2))) >= 2: gannHotLineNumber += po.gannHotLineSetRow2
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow3))) >= 2: gannHotLineNumber += po.gannHotLineSetRow3
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow4))) >= 2: gannHotLineNumber += po.gannHotLineSetRow4
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow5))) >= 2: gannHotLineNumber += po.gannHotLineSetRow5
            if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow6))) >= 2: gannHotLineNumber += po.gannHotLineSetRow6
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0741','" + str(len(list((val for val in setd if val in list(set(gannHotLineNumber)))))) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','6')")

            # 计算 0742 - 0746
            beOptPeriodNumber = setd
            arraySsqIssue = []
            names = locals()
            for v_num in range(1, 34): names['array%s' % v_num] = []

            # 行转列存贮在数组中（更合适列的方式处理）
            for setb in modelPeriodNumber:
                arraySsqIssue.append(setb[0])
                for v_num in range(1, 34): names['array%s' % v_num].append(setb[v_num])

            # for beOptNum in range(10, len(arraySsqIssue)):  # 处理第11期开始的期号

            listA = list(priorPeriodNumber)  # 上期号码集合
            listB = []  # 6-10期未出现过的温号集合
            listC = []  # 10期以上都没出现的冷号集合
            listD = []  # B+C温冷号集合
            listE = []  # A+B+C以外的热号集合
            lista = []
            listb = []
            listc = []
            listd = []
            liste = []  # 小集合变量定义 a/A b/B c/C d/D e/E

            for listValNameNum in range(1, 34):  # 动态拿到1-33个存储列号码的数组变量名

                flagB_1_5 = 0  # 从操作期号开始往上数 beOptNum
                flagB_6_10 = 0  # 从操作期号开始往上数 beOptNum
                flagC = 0

                # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12  len = 12
                # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,  10, 11  下标
                for totalNum in range(len(arraySsqIssue) - 10, len(arraySsqIssue)):  # 每列取后10个出来计算

                    # ready B
                    if totalNum >= len(arraySsqIssue) - 5:
                        if names['array%s' % listValNameNum][totalNum] != "": flagB_1_5 = 1
                    else:
                        if names['array%s' % listValNameNum][totalNum] != "": flagB_6_10 = 1

                    # ready C 每列中有一个值不为空就标注出来，都为空则还是默认的0，即为冷号
                    if names['array%s' % listValNameNum][totalNum] != "": flagC = 1

                # create list B
                if flagB_1_5 == 0 and flagB_6_10 == 1:  # 符合条件（上期为空，1-5为空，6-10有不为空的），则加入B集合
                    if len(str(listValNameNum)) == 1:  # 处理listValNameNum是数字，有1位的情况，前面拼接"0"
                        listB.append("0" + str(listValNameNum))
                    else:
                        listB.append(str(listValNameNum))

                # create list C
                if flagC == 0:  # 10期都是空，则加入C集合
                    if len(str(listValNameNum)) == 1:  # 处理listValNameNum是数字，有1位的情况，前面拼接"0"
                        listC.append("0" + str(listValNameNum))
                    else:
                        listC.append(str(listValNameNum))

                # create list D
                listD = list(sorted(set(listB + listC)))

                # create list E
                listE = list((val for val in po.totalNumberSet if val not in sorted(set(listA + listB + listC))))

            lista = list((val for val in beOptPeriodNumber if val in listA))
            listb = list((val for val in beOptPeriodNumber if val in listB))
            listc = list((val for val in beOptPeriodNumber if val in listC))
            listd = list((val for val in beOptPeriodNumber if val in listD))
            liste = list((val for val in beOptPeriodNumber if val in listE))

            self.log.debug(opt_period_num + "beOptPeriodNumber:" + str(beOptPeriodNumber))
            self.log.debug(opt_period_num + "  A:" + str(listA) + "  a:" + str(lista) + "  a/A:" + str(len(lista)) + "/" + str(len(listA)))
            self.log.debug(opt_period_num + "  B:" + str(listB) + "  b:" + str(lista) + "  b/B:" + str(len(listb)) + "/" + str(len(listB)))
            self.log.debug(opt_period_num + "  C:" + str(listC) + "  c:" + str(lista) + "  c/C:" + str(len(listc)) + "/" + str(len(listC)))
            self.log.debug(opt_period_num + "  D:" + str(listD) + "  d:" + str(lista) + "  d/D:" + str(len(listd)) + "/" + str(len(listD)))
            self.log.debug(opt_period_num + "  E:" + str(listE) + "  e:" + str(lista) + "  e/E:" + str(len(liste)) + "/" + str(len(listE)))

            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0742','" + str(len(lista)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','7')")
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0743','" + str(len(listb)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','7')")
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0744','" + str(len(listc)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','7')")
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0745','" + str(len(listd)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','7')")
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0746','" + str(len(liste)) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','7')")

            # 计算 0747
            twoPeriodSetEqualCount = 0
            currentBeOptSet = [str(len(lista)), str(len(listb)), str(len(listc)), str(len(listd)), str(len(liste))]
            if priorBeOptSet[0][0:1] == currentBeOptSet[0]: twoPeriodSetEqualCount += 1
            if priorBeOptSet[1][0:1] == currentBeOptSet[1]: twoPeriodSetEqualCount += 1
            if priorBeOptSet[2][0:1] == currentBeOptSet[2]: twoPeriodSetEqualCount += 1
            if priorBeOptSet[3][0:1] == currentBeOptSet[3]: twoPeriodSetEqualCount += 1
            if priorBeOptSet[4][0:1] == currentBeOptSet[4]: twoPeriodSetEqualCount += 1
            self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','0747','" + str(twoPeriodSetEqualCount) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','4')")

        self.log.info("第" + opt_period_num + "期-遗传总量元数据全部生成完毕")

        # 此部分注释与方法前面对应
        #     self.log.info("遗传总量元数据生成完毕")
        # else:
        #     self.log.info("遗传总量元数据无需生成")

    # 内部遗传比例元数据（动态）
    def create_interior_heredity_proportion(self, opt_period_num):
        self.log.debug("获取各统计原始集合配置")

        # 读取原始模型中的29700条记录循环处理
        self.sql.execute("select * from t00_29700")
        rst_model_data = self.sql.fetchall()  # [('01', '02', '12', '17', '23', '24'), ('01', '02', '12', '17', '23', '26')...]   29700个

        # 获取"内部遗传比例"配置信息
        self.sql.execute("select id,v from t00_set where o='5' order by id")
        for seta in self.sql.fetchall():  # ['0023'] ['0001','0002','0003','0004','0005','0006','0007','0008' '0014','0015','0016','0017','0018','0019','0020','0021' 0] 个数根据配置来定
            setb = seta[1].split(" ", seta[1].count(" "))  # ['0001','0002','0003','0004','0005','0006','0007','0008'] ['0014','0015','0016','0017','0018','0019','0020','0021'] ['0']

            self.log.debug("正在计算" + opt_period_num + "期：" + seta[0])

            # 获取当期开奖结果集合值域 setc
            self.sql.execute("select " + setb[0].replace("'", "\"") + " from t00_data_analyze_inside where 开奖期号 = '" + opt_period_num + "'")
            for setc in self.sql.fetchall(): pass  # ('1','2','0','1','1','0','0','0') 一条记录      等待和下面与seth做比较

            # 获取各统计原始集合配置
            self.sql.execute("select v from t00_set where id in (" + setb[0] + ") order by id")
            rst_config_data = self.sql.fetchall()  # [('01 15 18 32'), ('02 14 19 31')...('08 16 17 25')]

            for setd in rst_model_data:  # ['01', '02', '12', '17', '23', '24'] 29700个循环
                # 统计每条模型记录的集合值域 seth
                seth = []
                for sete in rst_config_data:  # ['01 15 18 32'] 配置几个循环几个，例如001-008的，那么就是8次
                    setf = sete[0].split(" ", sete[0].count(" "))  # ['01','15','18','32']
                    setg = [var for var in setf if var in setd]
                    seth.append(str(len(setg)))  # ['0','0','0','0','2','2','0','1'] 每一个模型的集合值域统计

                # 比较 setc 和 seth,获取对应相等且等于统计目标值得个数，然后将个数和模型插入动态元数据表
                v_num = 0
                for v_len in range(0, len(setc)):
                    if setc[v_len] == seth[v_len] and setc[v_len] == setb[2]: v_num += 1
                self.sql.execute("insert into t00_range_dynamic values('" + opt_period_num + "','" + seta[0] + "','" + str(v_num) + "','" + setd[0] + "','" + setd[1] + "','" + setd[2] + "','" + setd[3] + "','" + setd[4] + "','" + setd[5] + "','5')")

        self.log.info("第" + opt_period_num + "期-内部遗传比例元数据全部生成完毕")

    # 获取历届开奖结果元数据
    def get_open_award_source_data(self):
        url = "http://www.17500.cn/getData/ssq.TXT"
        with request.urlopen(url) as web:
            with open("./../../../data/ssq.dat", 'wb') as outfile:  # 二进制，防止
                outfile.write(web.read())

        f = open("./../../../data/ssq.dat", "r")
        self.sql.execute("delete from t00_open_award")

        for line in f:
            tmp = str(line).replace("\n", "").split(" ", str(line).count(" "))
            ist_sql = "insert into t00_open_award values('"
            for var in tmp: ist_sql = ist_sql + var + "','"
            ist_sql = ist_sql[:len(ist_sql) - 2] + ")"
            self.sql.execute(ist_sql)

        f.close()

    def get_model_set(self):  # T00_DATA_ANALYZE_INSIDE
        self.sql.execute("delete from t00_data_analyze_inside")
        self.sql.execute("select 开奖期号,红号1,红号2,红号3,红号4,红号5,红号6 from t00_open_award")
        for line in self.sql.fetchall():
            v_arr_uneven = [var1 for var1 in po.oddNumberSet if var1 in line]
            v_arr_bignum = [var2 for var2 in po.bigNumberSet if var2 in line]
            v_arr_1_area = [var3 for var3 in po.sectionOneSet if var3 in line]
            v_arr_2_area = [var4 for var4 in po.sectionTwoSet if var4 in line]
            if len(v_arr_uneven) == 3 and len(v_arr_bignum) == 3 and len(v_arr_1_area) == 2 and len(v_arr_2_area) == 2:
                self.sql.execute("insert into t00_data_analyze_inside (开奖期号,红球1,红球2,红球3,红球4,红球5,红球6) values ('" + line[0] + "','" + line[1] + "','" + line[2] + "','" + line[3] + "','" + line[4] + "','" + line[5] + "','" + line[6] + "')")

    # 获取统计值
    def get_statistics_value(self):
        self.sql.execute("select 开奖期号,红球1,红球2,红球3,红球4,红球5,红球6 from t00_data_analyze_inside order by 开奖期号")
        resultModelIdRedBall_1_6 = self.sql.fetchall()
        self.sql.execute("select 开奖期号  from t00_data_analyze_inside order by 开奖期号")
        resultModelId = self.sql.fetchall()

        # 计算 01 - 33
        # 清空01-33列
        v_column = ""
        for v_num in range(1, 34):
            if len(str(v_num)) == 1:
                v_column = "0" + str(v_num)
            else:
                v_column = str(v_num)
            self.sql.execute("update t00_data_analyze_inside set \"" + v_column + "\"=\"\"")

        # 开始计算
        for seta in resultModelIdRedBall_1_6:  # ('2003005', '04', '06', '15', '17', '30', '31')
            for v_num in range(1, 7):
                self.sql.execute("update t00_data_analyze_inside set \"" + seta[v_num] + "\"='" + seta[v_num] + "' where 开奖期号='" + str(seta[0]) + "'")

        # 一二三、高级统计-计算“值域统计” 0001 - 0008 o=1
        # 获取历届模型基础数据
        for seta in resultModelIdRedBall_1_6:
            self.sql.execute("select id,v from t00_set where o='1' order by id")
            for setb in self.sql.fetchall():
                setc = setb[1].split(" ", setb[1].count(" "))
                rst = [var for var in seta if var in setc]
                self.sql.execute("update t00_data_analyze_inside set \"" + setb[0] + "\"='" + str(len(rst)) + "' where 开奖期号='" + str(seta[0]) + "'")

        # 一二三、高级统计-计算“各项数量统计” 0009 - 0013 o=2
        # 获取历届模型基础数据
        for seta in resultModelIdRedBall_1_6:
            self.sql.execute("select id,v from t00_set where o='2' order by id")
            for setb in self.sql.fetchall():  # ['0009']['0001','0002','0003','0004','0005','0006','0007','0008' 0]
                setc = setb[1].split(" ", setb[1].count(" "))
                self.sql.execute("select 开奖期号," + setc[0].replace("'", "\"") + " from t00_data_analyze_inside where 开奖期号='" + str(seta[0]) + "'")
                for setd in self.sql.fetchall():  # setd:('2016117', '0', '1', '1', '0', '1', '1', '0', '1')
                    v_count = 0
                    for var in setd:
                        if setc[1] == var: v_count += 1
                self.sql.execute("update t00_data_analyze_inside set \"" + setb[0] + "\"='" + str(v_count) + "' where 开奖期号='" + str(seta[0]) + "'")

        # 一二三、高级统计-计算“遗传统计” 0014 - 0021 o=3
        self.sql.execute("select id,v from t00_set where o='3' order by id")
        for seta in self.sql.fetchall():  # ['0014'] ['0001']
            self.sql.execute("select 开奖期号,\"" + seta[1] + "\" from t00_data_analyze_inside order by 开奖期号")
            for setb in self.sql.fetchall():  # ['2003005'] ['1']
                self.sql.execute("select count(1) from t00_data_analyze_inside where 开奖期号<='" + str(setb[0]) + "' order by 开奖期号 ")
                for setc in self.sql.fetchall():  # count ['2']
                    if setc[0] > 1:
                        self.sql.execute("select \"" + seta[1] + "\" from t00_data_analyze_inside where 开奖期号<='" + str(setb[0]) + "' order by 开奖期号  desc  limit 2")
                        setd = self.sql.fetchone()  # 当前记录 ['2']
                        sete = self.sql.fetchone()  # 上一记录 ['2']
                        if setd[0] == sete[0]:
                            self.sql.execute("update t00_data_analyze_inside set \"" + seta[0] + "\"='" + setd[0] + "' where 开奖期号='" + str(setb[0]) + "'")
                        else:
                            self.sql.execute("update t00_data_analyze_inside set \"" + seta[0] + "\"=\"\" where 开奖期号='" + str(setb[0]) + "'")
                    else:
                        self.sql.execute("update t00_data_analyze_inside set \"" + seta[0] + "\"=\"\" where 开奖期号='" + str(setb[0]) + "'")

        # 一二三、高级统计-计算“遗传总量统计” 0022 o=4
        self.sql.execute("select id,v from t00_set where o='4' order by id")
        for seta in self.sql.fetchall():  # ['022'] ['0001','0002','0003','0004','0005','0006','0007','0008' '0014','0015','0016','0017','0018','0019','0020','0021']
            setc = seta[1].split(" ", seta[1].count(" "))
            self.sql.execute("select 开奖期号," + setc[1].replace("'", "\"") + " from t00_data_analyze_inside order by 开奖期号")
            for setb in self.sql.fetchall():  # ['2003005','1','','','1','','']
                v_rst = 0
                v_num = 1
                for var in setb:
                    if v_num == 1:
                        pass
                    else:
                        if var == "":
                            pass
                        else:
                            v_rst += 1
                    v_num += 1
                if str(setb[0]) == "2003005":
                    self.sql.execute("update t00_data_analyze_inside set \"" + seta[0] + "\"=\"\" where 开奖期号='" + str(setb[0]) + "'")
                else:
                    self.sql.execute("update t00_data_analyze_inside set \"" + seta[0] + "\"='" + str(v_rst) + "' where 开奖期号='" + str(setb[0]) + "'")

        # 一二三、高级统计-计算“内部遗传比例” 0023 - 0025 o=5
        self.sql.execute("select id,v from t00_set where o='5' order by id")
        for seta in self.sql.fetchall():  # ['0023'] ['0001','0002','0003','0004','0005','0006','0007','0008' '0014','0015','0016','0017','0018','0019','0020','0021' '0']

            setb = seta[1].split(" ", seta[1].count(" "))  # ['0001','0002','0003','0004','0005','0006','0007','0008'] ['0014','0015','0016','0017','0018','0019','0020','0021'] ['0']

            for setc in resultModelId:  # ['2003005']
                self.sql.execute("select count(1) from t00_data_analyze_inside where 开奖期号<='" + str(setc[0]) + "' order by 开奖期号 ")
                for setd in self.sql.fetchall():  # count ['2']
                    if setd[0] > 1:
                        self.sql.execute("select " + setb[0].replace("'", "\"") + " from t00_data_analyze_inside where 开奖期号<='" + str(setc[0]) + "' order by 开奖期号  desc limit 2")
                        sete = self.sql.fetchone()  # 当前记录  [1','1','0','1','2','1']
                        sete = self.sql.fetchone()  # 上一记录  [1','1','0','0','0','1'] 只要上一记录

                        self.sql.execute("select " + setb[1].replace("'", "\"") + " from t00_data_analyze_inside where 开奖期号<='" + str(setc[0]) + "' order by 开奖期号  desc limit 2")
                        setf = self.sql.fetchone()  # 当前记录  [1','1','0','1','2','1'] 只要当前记录
                        # setf=self.sql.fetchone() #  上一记录  [1','1','0','0','0','1']

                        v_present = 0
                        # v_up = 0
                        #
                        # for var in sete:
                        #     if setb[2] == var: v_up += 1
                        for var in setf:
                            if setb[2] == var: v_present += 1

                        # if v_present == 0:
                        #     self.sql.execute("update t00_data_analyze_inside set \"" + str(seta[0]) + "\"='" + str(v_present) + "' where 开奖期号='" + setc[0] + "'")
                        # else:
                        #     self.sql.execute("update t00_data_analyze_inside set \"" + str(seta[0]) + "\"='" + str(v_present) + "/" + str(v_up) + "' where 开奖期号='" + setc[0] + "'")
                        self.sql.execute("update t00_data_analyze_inside set \"" + str(seta[0]) + "\"='" + str(v_present) + "' where 开奖期号='" + str(setc[0]) + "'")
                    else:
                        self.sql.execute("update t00_data_analyze_inside set \"" + str(seta[0]) + "\"=\"\" where 开奖期号='" + str(setc[0]) + "'")

        # 四、高级统计-计算“位势” 0686 - 0691
        self.sql.execute("update t00_data_analyze_inside set \"0686\"=红球1,\"0687\"=红球2,\"0688\"=红球3,\"0689\"=红球4,\"0690\"=红球5,\"0691\"=红球6")

        # 四、高级统计-计算“位势遗传项数” 0692 （非对应式匹配，而是集合式匹配，与书中不同；在0692值域排除时也需要采用集合式匹配）
        for seta in resultModelId:  # ['2003005']
            if str(seta[0]) == "2003005":
                self.sql.execute("update t00_data_analyze_inside set \"0692\"=\"\" where 开奖期号='" + str(seta[0]) + "'")
            else:
                self.sql.execute("select \"0686\",\"0687\",\"0688\",\"0689\",\"0690\",\"0691\" from t00_data_analyze_inside where 开奖期号<='" + str(seta[0]) + "' order by 开奖期号  desc limit 2")
                setb = self.sql.fetchone()  # 当前记录  ['01,'07','14','20','27','30']
                setc = self.sql.fetchone()  # 上一记录  ['04,'06','15','17','30','31']
                setd = [var for var in setb if var in setc]
                self.sql.execute("update t00_data_analyze_inside set \"0692\"='" + str(len(setd)) + "' where 开奖期号='" + str(seta[0]) + "'")

        # 四、高级统计-计算“间距值” 0693 - 0698
        # 将红球01-33顺时针排列成圈，然后计算各个相邻号码在这个圈中间隔的号码个数
        # 即相邻号码间距为两相邻号码只差减1，如12与16，间距为16-12-1=3；
        # 33与01视为相连，即间距为0
        # 第6个号码与第一个号码间距称为1，第2个与第3个称为2...
        self.sql.execute("select 开奖期号,\"0686\",\"0687\",\"0688\",\"0689\",\"0690\",\"0691\" from t00_data_analyze_inside order by 开奖期号 ")
        for seta in self.sql.fetchall():  # ['2003005','04','06','15','17','30','31']
            # 计算间距1(首尾)
            self.sql.execute("update t00_data_analyze_inside set \"0693\"='" + str(33 - int(seta[6]) + int(seta[1]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")
            # 计算间距2
            self.sql.execute("update t00_data_analyze_inside set \"0694\"='" + str(int(seta[2]) - int(seta[1]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")
            # 计算间距3
            self.sql.execute("update t00_data_analyze_inside set \"0695\"='" + str(int(seta[3]) - int(seta[2]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")
            # 计算间距4
            self.sql.execute("update t00_data_analyze_inside set \"0696\"='" + str(int(seta[4]) - int(seta[3]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")
            # 计算间距5
            self.sql.execute("update t00_data_analyze_inside set \"0697\"='" + str(int(seta[5]) - int(seta[4]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")
            # 计算间距6
            self.sql.execute("update t00_data_analyze_inside set \"0698\"='" + str(int(seta[6]) - int(seta[5]) - 1) + "' where 开奖期号='" + str(seta[0]) + "'")

        # 四、高级统计-计算“间距遗传项数” 0699
        for seta in resultModelId:  # ['2003005']
            if str(seta[0]) == "2003005":
                self.sql.execute("update t00_data_analyze_inside set \"0699\"=\"\" where 开奖期号='" + str(seta[0]) + "'")
            else:
                self.sql.execute("select \"0693\",\"0694\",\"0695\",\"0696\",\"0697\",\"0698\" from t00_data_analyze_inside where 开奖期号<='" + str(seta[0]) + "' order by 开奖期号  desc limit 2")
                setb = self.sql.fetchone()  # 当前记录  ['01,'07','14','20','27','30']
                setc = self.sql.fetchone()  # 上一记录  ['04,'06','15','17','30','31']
                v_num = 0
                for setd in range(0, 6):
                    if setb[setd] == setc[setd]: v_num += 1
                self.sql.execute("update t00_data_analyze_inside set \"0699\"='" + str(v_num) + "' where 开奖期号='" + str(seta[0]) + "'")

        # 四、高级统计-计算“间距-重复项、间距特征” 0700、0701
        self.sql.execute("select 开奖期号,\"0693\",\"0694\",\"0695\",\"0696\",\"0697\",\"0698\" from t00_data_analyze_inside order by 开奖期号")
        for seta in self.sql.fetchall():  # ['2003005','5','1','8','1','12','0'] 间距
            setb = [seta[1], seta[2], seta[3], seta[4], seta[5], seta[6]]
            setc = list(set(setb))  # 排序+去重
            chongfuxiang = []
            jianjutezheng = []
            for setd in setc:  # 遍历排序去重后的list ['0','1','5','8','12']
                v_count = 0
                for sete in seta:  # 遍历查询出的list
                    if setd == sete: v_count += 1
                if v_count > 1:
                    chongfuxiang.append(setd)
                    jianjutezheng.append(str(v_count))
            if len(chongfuxiang) == 0: jianjutezheng.append("0")

            setf = list(sorted(set(map(int, chongfuxiang))))
            setg = list(sorted(jianjutezheng))
            seti = ""
            setj = ""
            for seth in range(0, len(setf)):
                if seti != "":
                    seti = seti + "&" + str(setf[seth])
                else:
                    seti = str(setf[seth])
            for setk in range(0, len(setg)):
                if setj != "":
                    setj = setj + "+" + setg[setk]
                else:
                    setj = setg[setk]

            if seti == "": seti = '-'
            if setj == "0": setj = '-'

            self.sql.execute("update t00_data_analyze_inside set \"0700\"='" + seti + "',\"0701\"='" + setj + "' where 开奖期号='" + str(seta[0]) + "'")

        # 五、高级统计：-计算“和值” 0702 - 0720
        for setf in resultModelIdRedBall_1_6:  # ('2016117', '04', '06', '15', '17', '30', '31')
            setg = (setf[1], setf[2], setf[3], setf[4], setf[5], setf[6])  # ('04', '06', '15', '17', '30', '31')
            #  0702 二区和值
            self.sql.execute("update t00_data_analyze_inside set \"0702\"='" + str(sum(map(int, (val for val in setg if val in po.sectionTwoSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0703 三区和值
            self.sql.execute("update t00_data_analyze_inside set \"0703\"='" + str(sum(map(int, (val for val in setg if val in po.sectionThreeSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0704 小号和值
            self.sql.execute("update t00_data_analyze_inside set \"0704\"='" + str(sum(map(int, (val for val in setg if val not in po.bigNumberSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0705 一区和值
            self.sql.execute("update t00_data_analyze_inside set \"0705\"='" + str(sum(map(int, (val for val in setg if val in po.sectionOneSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0706 邻号间距和
            self.sql.execute("select \"0691\"-\"0686\" from t00_data_analyze_inside where 开奖期号='" + str(setf[0]) + "'")
            for val in self.sql.fetchone(): pass
            self.sql.execute("update t00_data_analyze_inside set \"0706\"='" + str(val) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0707 大号和值
            self.sql.execute("update t00_data_analyze_inside set \"0707\"='" + str(sum(map(int, (val for val in setg if val in po.bigNumberSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0708 尾号位积和（1*a+2*b+3*c+4*d+5*e+6*f）
            self.sql.execute("update t00_data_analyze_inside set \"0708\"='" + str(sum((int(setf[1][1:]) * 1, int(setf[2][1:]) * 2, int(setf[3][1:]) * 3, int(setf[4][1:]) * 4, int(setf[5][1:]) * 5, int(setf[6][1:]) * 6))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0709 奇号和值
            self.sql.execute("update t00_data_analyze_inside set \"0709\"='" + str(sum(map(int, (val for val in setg if val in po.oddNumberSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0710 偶号和值
            self.sql.execute("update t00_data_analyze_inside set \"0710\"='" + str(sum(map(int, (val for val in setg if val not in po.oddNumberSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0711 质号和值
            self.sql.execute("update t00_data_analyze_inside set \"0711\"='" + str(sum(map(int, (val for val in setg if val in po.primeNumberSet)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0712 除6余数和
            self.sql.execute("update t00_data_analyze_inside set \"0712\"='" + str(sum((int(setf[1]) % 6, int(setf[2]) % 6, int(setf[3]) % 6, int(setf[4]) % 6, int(setf[5]) % 6, int(setf[6]) % 6))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0713 除7余数和
            self.sql.execute("update t00_data_analyze_inside set \"0713\"='" + str(sum((int(setf[1]) % 7, int(setf[2]) % 7, int(setf[3]) % 7, int(setf[4]) % 7, int(setf[5]) % 7, int(setf[6]) % 7))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0714 号码和尾值
            self.sql.execute("update t00_data_analyze_inside set \"0714\"='" + str(int(setf[1]) + int(setf[2]) + int(setf[3]) + int(setf[4]) + int(setf[5]) + int(setf[6]))[-1:] + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0715 首位和值
            self.sql.execute("update t00_data_analyze_inside set \"0715\"='" + str(sum(map(int, (val[0:1] for val in setg)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0716 除3余数和
            self.sql.execute("update t00_data_analyze_inside set \"0716\"='" + str(sum((int(setf[1]) % 3, int(setf[2]) % 3, int(setf[3]) % 3, int(setf[4]) % 3, int(setf[5]) % 3, int(setf[6]) % 3))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0717 除4余数和
            self.sql.execute("update t00_data_analyze_inside set \"0717\"='" + str(sum((int(setf[1]) % 4, int(setf[2]) % 4, int(setf[3]) % 4, int(setf[4]) % 4, int(setf[5]) % 4, int(setf[6]) % 4))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0718 除5余数和
            self.sql.execute("update t00_data_analyze_inside set \"0718\"='" + str(sum((int(setf[1]) % 5, int(setf[2]) % 5, int(setf[3]) % 5, int(setf[4]) % 5, int(setf[5]) % 5, int(setf[6]) % 5))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0719 除8余数和
            self.sql.execute("update t00_data_analyze_inside set \"0719\"='" + str(sum((int(setf[1]) % 8, int(setf[2]) % 8, int(setf[3]) % 8, int(setf[4]) % 8, int(setf[5]) % 8, int(setf[6]) % 8))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0720 除9余数和
            self.sql.execute("update t00_data_analyze_inside set \"0720\"='" + str(sum((int(setf[1]) % 9, int(setf[2]) % 9, int(setf[3]) % 9, int(setf[4]) % 9, int(setf[5]) % 9, int(setf[6]) % 9))) + "' where 开奖期号='" + str(setf[0]) + "'")

            # 六、综合常规统计： 0721 - 0740
            #  0721 AC值
            acValue_0721 = str(len(list({int(setf[2]) - int(setf[1]), int(setf[3]) - int(setf[1]), int(setf[4]) - int(setf[1]), int(setf[5]) - int(setf[1]), int(setf[6]) - int(setf[1]), int(setf[3]) - int(setf[2]), int(setf[4]) - int(setf[2]), int(setf[5]) - int(setf[2]), int(setf[6]) - int(setf[2]), int(setf[4]) - int(setf[3]), int(setf[5]) - int(setf[3]), int(setf[6]) - int(setf[3]), int(setf[5]) - int(setf[4]), int(setf[6]) - int(setf[4]), int(setf[6]) - int(setf[5])})) - 5)
            self.sql.execute("update t00_data_analyze_inside set \"0721\"='" + acValue_0721 + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0722 最大号码
            self.sql.execute("update t00_data_analyze_inside set \"0722\"='" + str(list(sorted(setg))[5]) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0723 极号间距
            self.sql.execute("update t00_data_analyze_inside set \"0723\"='" + str(int(setf[6]) - int(setf[1])) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0724 最大邻距
            self.sql.execute("update t00_data_analyze_inside set \"0724\"='" + str(list(sorted((int(setf[6]) - int(setf[5]), int(setf[5]) - int(setf[4]), int(setf[4]) - int(setf[3]), int(setf[3]) - int(setf[2]), int(setf[2]) - int(setf[1]))))[4]) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0725 号码和值
            self.sql.execute("update t00_data_analyze_inside set \"0725\"='" + str(sum(map(int, setg))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0726 尾数和值
            self.sql.execute("update t00_data_analyze_inside set \"0726\"='" + str(sum(map(int, (val[1:] for val in setg)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0727 最小号码
            self.sql.execute("update t00_data_analyze_inside set \"0727\"='" + str(list(sorted(setg))[0]) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0728 尾数组数
            self.sql.execute("update t00_data_analyze_inside set \"0728\"='" + str(len(list({setf[1][1], setf[2][1], setf[3][1], setf[4][1], setf[5][1], setf[6][1]}))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0729 奇号连续
            oddNumContinuousCount = 0
            if int(setf[1]) % 2 != 0 and int(setf[2]) % 2 != 0: oddNumContinuousCount += 1
            if int(setf[2]) % 2 != 0 and int(setf[3]) % 2 != 0: oddNumContinuousCount += 1
            if int(setf[3]) % 2 != 0 and int(setf[4]) % 2 != 0: oddNumContinuousCount += 1
            if int(setf[4]) % 2 != 0 and int(setf[5]) % 2 != 0: oddNumContinuousCount += 1
            if int(setf[5]) % 2 != 0 and int(setf[6]) % 2 != 0: oddNumContinuousCount += 1
            self.sql.execute("update t00_data_analyze_inside set \"0729\"='" + str(oddNumContinuousCount) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0730 偶号连续
            evenNumContinuousCount = 0
            if int(setf[1]) % 2 == 0 and int(setf[2]) % 2 == 0: evenNumContinuousCount += 1
            if int(setf[2]) % 2 == 0 and int(setf[3]) % 2 == 0: evenNumContinuousCount += 1
            if int(setf[3]) % 2 == 0 and int(setf[4]) % 2 == 0: evenNumContinuousCount += 1
            if int(setf[4]) % 2 == 0 and int(setf[5]) % 2 == 0: evenNumContinuousCount += 1
            if int(setf[5]) % 2 == 0 and int(setf[6]) % 2 == 0: evenNumContinuousCount += 1
            self.sql.execute("update t00_data_analyze_inside set \"0730\"='" + str(evenNumContinuousCount) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0731 最小邻距
            self.sql.execute("update t00_data_analyze_inside set \"0731\"='" + str(list(sorted((int(setf[6]) - int(setf[5]), int(setf[5]) - int(setf[4]), int(setf[4]) - int(setf[3]), int(setf[3]) - int(setf[2]), int(setf[2]) - int(setf[1]))))[0]) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0732 质号个数
            self.sql.execute("update t00_data_analyze_inside set \"0732\"='" + str(len(list(val for val in setg if val in po.primeNumberSet))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0733 遗传项数
            heredityCount_0733 = 0
            if str(setf[0]) == "2003005":
                self.sql.execute("update t00_data_analyze_inside set \"0733\"='' where 开奖期号='2003005'")
            else:
                self.sql.execute("select \"0725\",\"0726\",\"0727\",\"0728\",\"0729\",\"0730\",\"0731\",\"0732\" from t00_data_analyze_inside where 开奖期号<='" + str(setf[0]) + "' order by 开奖期号  desc limit 2")
                currentRecord = self.sql.fetchone()  # 当前记录
                previousRecord = self.sql.fetchone()  # 上一记录
                if currentRecord[0] == previousRecord[0]: heredityCount_0733 += 1
                if currentRecord[1] == previousRecord[1]: heredityCount_0733 += 1
                if currentRecord[2] == previousRecord[2]: heredityCount_0733 += 1
                if currentRecord[3] == previousRecord[3]: heredityCount_0733 += 1
                if currentRecord[4] == previousRecord[4]: heredityCount_0733 += 1
                if currentRecord[5] == previousRecord[5]: heredityCount_0733 += 1
                if currentRecord[6] == previousRecord[6]: heredityCount_0733 += 1
                if currentRecord[7] == previousRecord[7]: heredityCount_0733 += 1
                self.sql.execute("update t00_data_analyze_inside set \"0733\"='" + str(heredityCount_0733) + "' where 开奖期号='" + str(setf[0]) + "'")
            # 0734 质号连续
            primeNumContinuousCount = 0
            if setf[1] in po.primeNumberSet and setf[2] in po.primeNumberSet: primeNumContinuousCount += 1
            if setf[2] in po.primeNumberSet and setf[3] in po.primeNumberSet: primeNumContinuousCount += 1
            if setf[3] in po.primeNumberSet and setf[4] in po.primeNumberSet: primeNumContinuousCount += 1
            if setf[4] in po.primeNumberSet and setf[5] in po.primeNumberSet: primeNumContinuousCount += 1
            if setf[5] in po.primeNumberSet and setf[6] in po.primeNumberSet: primeNumContinuousCount += 1
            self.sql.execute("update t00_data_analyze_inside set \"0734\"='" + str(primeNumContinuousCount) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0735 连号个数
            ContinuousNumCount = 0
            if int(setf[1]) + 1 == int(setf[2]): ContinuousNumCount += 1
            if int(setf[2]) + 1 == int(setf[3]): ContinuousNumCount += 1
            if int(setf[3]) + 1 == int(setf[4]): ContinuousNumCount += 1
            if int(setf[4]) + 1 == int(setf[5]): ContinuousNumCount += 1
            if int(setf[5]) + 1 == int(setf[6]): ContinuousNumCount += 1
            self.sql.execute("update t00_data_analyze_inside set \"0735\"='" + str(ContinuousNumCount) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0736 大奇个数
            self.sql.execute("update t00_data_analyze_inside set \"0736\"='" + str(len(list((val for val in po.bigOddSet if val in setf)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0737 小奇个数
            self.sql.execute("update t00_data_analyze_inside set \"0737\"='" + str(len(list((val for val in po.smallOddSet if val in setf)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0738 大偶个数
            self.sql.execute("update t00_data_analyze_inside set \"0738\"='" + str(len(list((val for val in po.bigEvenSet if val in setf)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0739 小偶个数
            self.sql.execute("update t00_data_analyze_inside set \"0739\"='" + str(len(list((val for val in po.smallEvenSet if val in setf)))) + "' where 开奖期号='" + str(setf[0]) + "'")
            #  0740 号码散度
            numDvg1 = list(sorted((int(setf[2]) - int(setf[1]), int(setf[3]) - int(setf[1]), int(setf[4]) - int(setf[1]), int(setf[5]) - int(setf[1]), int(setf[6]) - int(setf[1]))))[0]
            numDvg2 = list(sorted((int(setf[2]) - int(setf[1]), int(setf[3]) - int(setf[2]), int(setf[4]) - int(setf[2]), int(setf[5]) - int(setf[2]), int(setf[6]) - int(setf[2]))))[0]
            numDvg3 = list(sorted((int(setf[3]) - int(setf[1]), int(setf[3]) - int(setf[2]), int(setf[4]) - int(setf[3]), int(setf[5]) - int(setf[3]), int(setf[6]) - int(setf[3]))))[0]
            numDvg4 = list(sorted((int(setf[4]) - int(setf[1]), int(setf[4]) - int(setf[2]), int(setf[4]) - int(setf[3]), int(setf[5]) - int(setf[4]), int(setf[6]) - int(setf[4]))))[0]
            numDvg5 = list(sorted((int(setf[5]) - int(setf[1]), int(setf[5]) - int(setf[2]), int(setf[5]) - int(setf[3]), int(setf[5]) - int(setf[4]), int(setf[6]) - int(setf[5]))))[0]
            numDvg6 = list(sorted((int(setf[6]) - int(setf[1]), int(setf[6]) - int(setf[2]), int(setf[6]) - int(setf[3]), int(setf[6]) - int(setf[4]), int(setf[6]) - int(setf[5]))))[0]
            numberDivergence = list(sorted((numDvg1, numDvg2, numDvg3, numDvg4, numDvg5, numDvg6)))[5]
            self.sql.execute("update t00_data_analyze_inside set \"0740\"='" + str(numberDivergence) + "' where 开奖期号='" + str(setf[0]) + "'")

        # 七、号码分布：集合： 0741 - 0747
        # gannHotLineRedBallShowProportion 计算江恩热线红球中出比例
        for seta in resultModelIdRedBall_1_6:
            gannHotLineNumber = []
            if str(seta[0]) == "2003005":  # 排除第一期
                self.sql.execute("update t00_data_analyze_inside set \"0741\"=\"\" where 开奖期号='" + str(seta[0]) + "'")
                self.sql.execute("update t00_data_analyze_inside set \"0742\"=\"\" where 开奖期号='" + str(seta[0]) + "'")
                priorPeriodNumber = [seta[1], seta[2], seta[3], seta[4], seta[5], seta[6]]  # 保存第一期为上期号码
            else:
                currentPeriodNumber = [seta[1], seta[2], seta[3], seta[4], seta[5], seta[6]]  # 当期号码
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn1))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn1
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn2))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn2
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn3))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn3
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn4))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn4
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn5))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn5
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetColumn6))) >= 2: gannHotLineNumber += po.gannHotLineSetColumn6
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow1))) >= 2: gannHotLineNumber += po.gannHotLineSetRow1
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow2))) >= 2: gannHotLineNumber += po.gannHotLineSetRow2
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow3))) >= 2: gannHotLineNumber += po.gannHotLineSetRow3
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow4))) >= 2: gannHotLineNumber += po.gannHotLineSetRow4
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow5))) >= 2: gannHotLineNumber += po.gannHotLineSetRow5
                if len(list((val for val in priorPeriodNumber if val in po.gannHotLineSetRow6))) >= 2: gannHotLineNumber += po.gannHotLineSetRow6
                # self.sql.execute("update t00_data_analyze_inside set \"0741\"='" + str(len(list((val for val in currentPeriodNumber if val in list(set(gannHotLineNumber)))))) + "/" + str(len(list(set(gannHotLineNumber)))) + "' where 开奖期号='" + str(seta[0]) + "'")
                self.sql.execute("update t00_data_analyze_inside set \"0741\"='" + str(len(list((val for val in currentPeriodNumber if val in list(set(gannHotLineNumber)))))) + "' where 开奖期号='" + str(seta[0]) + "'")
                priorPeriodNumber = [seta[1], seta[2], seta[3], seta[4], seta[5], seta[6]]  # 保存除第一期以外的为上期号码

        self.sql.execute("update t00_data_analyze_inside set \"0742\"='',\"0743\"='',\"0744\"='',\"0745\"='',\"0746\"='',\"0747\"=''")
        arraySsqIssue = []
        names = locals()
        for v_num in range(1, 34): names['array%s' % v_num] = []

        self.sql.execute("select \"开奖期号\",\"01\",\"02\",\"03\",\"04\",\"05\",\"06\",\"07\",\"08\",\"09\",\"10\",\"11\",\"12\",\"13\",\"14\",\"15\",\"16\",\"17\",\"18\",\"19\",\"20\",\"21\",\"22\",\"23\",\"24\",\"25\",\"26\",\"27\",\"28\",\"29\",\"30\",\"31\",\"32\",\"33\" from t00_data_analyze_inside order by 开奖期号")

        # 行转列存贮在数组中（更合适列的方式处理）
        for setb in self.sql.fetchall():
            arraySsqIssue.append(setb[0])
            for v_num in range(1, 34): names['array%s' % v_num].append(setb[v_num])

        for beOptNum in range(10, len(arraySsqIssue)):  # 处理第11期开始的期号

            listA = []  # 上期号码集合
            listB = []  # 6-10期未出现过的温号集合
            listC = []  # 10期以上都没出现的冷号集合
            listD = []  # B+C温冷号集合
            listE = []  # A+B+C以外的热号集合
            lista = []
            listb = []
            listc = []
            listd = []
            liste = []  # 小集合变量定义 a/A b/B c/C d/D e/E
            beOptPeriodNumber = []  # 获取预操作期的号码集合

            for listValNameNum in range(1, 34):  # 动态拿到1-33个存储列号码的数组变量名

                flagB_1_5 = 0  # 从操作期号开始往上数 beOptNum
                flagB_6_10 = 0  # 从操作期号开始往上数 beOptNum
                flagC = 0

                # create list nextPeriodNumber
                if names['array%s' % listValNameNum][beOptNum] != "": beOptPeriodNumber.append(names['array%s' % listValNameNum][beOptNum])

                for totalNum in range(0, len(arraySsqIssue)):  # 循环遍历列数组元素进行相关操作

                    #  create list A
                    if totalNum == beOptNum - 1:
                        if names['array%s' % listValNameNum][totalNum] != "": listA.append(names['array%s' % listValNameNum][totalNum])

                    # ready B
                    if beOptNum - 10 <= totalNum <= beOptNum - 1:
                        if totalNum == beOptNum - 1:
                            if names['array%s' % listValNameNum][totalNum] != "": flagB_1_5 = 1
                        if beOptNum - 5 <= totalNum < beOptNum - 1:
                            if names['array%s' % listValNameNum][totalNum] != "": flagB_1_5 = 1
                        if beOptNum - 10 <= totalNum <= beOptNum - 6:
                            if names['array%s' % listValNameNum][totalNum] != "": flagB_6_10 = 1

                    # ready C
                    if beOptNum - 10 <= totalNum <= beOptNum - 1:
                        if names['array%s' % listValNameNum][totalNum] != "": flagC = 1

                # create list B
                if flagB_1_5 == 0 and flagB_6_10 == 1:  # 符合条件（上期为空，1-5为空，6-10有不为空的），则加入B集合
                    if len(str(listValNameNum)) == 1:  # 处理listValNameNum是数字，有1位的情况，前面拼接"0"
                        listB.append("0" + str(listValNameNum))
                    else:
                        listB.append(str(listValNameNum))

                # create list C
                if flagC == 0:  # 10期都是空，则加入C集合
                    if len(str(listValNameNum)) == 1:  # 处理listValNameNum是数字，有1位的情况，前面拼接"0"
                        listC.append("0" + str(listValNameNum))
                    else:
                        listC.append(str(listValNameNum))

                # create list D
                listD = list(sorted(set(listB + listC)))

                # create list E
                listE = list((val for val in po.totalNumberSet if val not in sorted(set(listA + listB + listC))))

            lista = list((val for val in beOptPeriodNumber if val in listA))
            listb = list((val for val in beOptPeriodNumber if val in listB))
            listc = list((val for val in beOptPeriodNumber if val in listC))
            listd = list((val for val in beOptPeriodNumber if val in listD))
            liste = list((val for val in beOptPeriodNumber if val in listE))

            print(str(arraySsqIssue[beOptNum]) + "beOptPeriodNumber:" + str(beOptPeriodNumber))
            print(str(arraySsqIssue[beOptNum]) + "  A:" + str(listA) + "  a:" + str(lista) + "  a/A:" + str(len(lista)) + "/" + str(len(listA)))
            print(str(arraySsqIssue[beOptNum]) + "  B:" + str(listB) + "  b:" + str(lista) + "  b/B:" + str(len(listb)) + "/" + str(len(listB)))
            print(str(arraySsqIssue[beOptNum]) + "  C:" + str(listC) + "  c:" + str(lista) + "  c/C:" + str(len(listc)) + "/" + str(len(listC)))
            print(str(arraySsqIssue[beOptNum]) + "  D:" + str(listD) + "  d:" + str(lista) + "  d/D:" + str(len(listd)) + "/" + str(len(listD)))
            print(str(arraySsqIssue[beOptNum]) + "  E:" + str(listE) + "  e:" + str(lista) + "  e/E:" + str(len(liste)) + "/" + str(len(listE)))

            # self.sql.execute("update t00_data_analyze_inside set \"0742\"='" + str(len(lista)) + "/" + str(len(listA)) + "' where 开奖期号='" + arraySsqIssue[beOptNum] + "'")
            # self.sql.execute("update t00_data_analyze_inside set \"0743\"='" + str(len(listb)) + "/" + str(len(listB)) + "' where 开奖期号='" + arraySsqIssue[beOptNum] + "'")
            # self.sql.execute("update t00_data_analyze_inside set \"0744\"='" + str(len(listc)) + "/" + str(len(listC)) + "' where 开奖期号='" + arraySsqIssue[beOptNum] + "'")
            # self.sql.execute("update t00_data_analyze_inside set \"0745\"='" + str(len(listd)) + "/" + str(len(listD)) + "' where 开奖期号='" + arraySsqIssue[beOptNum] + "'")
            # self.sql.execute("update t00_data_analyze_inside set \"0746\"='" + str(len(liste)) + "/" + str(len(listE)) + "' where 开奖期号='" + arraySsqIssue[beOptNum] + "'")
            self.sql.execute("update t00_data_analyze_inside set \"0742\"='" + str(len(lista)) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")
            self.sql.execute("update t00_data_analyze_inside set \"0743\"='" + str(len(listb)) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")
            self.sql.execute("update t00_data_analyze_inside set \"0744\"='" + str(len(listc)) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")
            self.sql.execute("update t00_data_analyze_inside set \"0745\"='" + str(len(listd)) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")
            self.sql.execute("update t00_data_analyze_inside set \"0746\"='" + str(len(liste)) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")

            twoPeriodSetEqualCount = 0
            if str(arraySsqIssue[beOptNum]) == "2005129":
                priorBeOptSet = [str(len(lista)), str(len(listb)), str(len(listc)), str(len(listd)), str(len(liste))]
            else:
                currentBeOptSet = [str(len(lista)), str(len(listb)), str(len(listc)), str(len(listd)), str(len(liste))]
                if priorBeOptSet[0] == currentBeOptSet[0]: twoPeriodSetEqualCount += 1
                if priorBeOptSet[1] == currentBeOptSet[1]: twoPeriodSetEqualCount += 1
                if priorBeOptSet[2] == currentBeOptSet[2]: twoPeriodSetEqualCount += 1
                if priorBeOptSet[3] == currentBeOptSet[3]: twoPeriodSetEqualCount += 1
                if priorBeOptSet[4] == currentBeOptSet[4]: twoPeriodSetEqualCount += 1
                self.sql.execute("update t00_data_analyze_inside set \"0747\"='" + str(twoPeriodSetEqualCount) + "' where 开奖期号='" + str(arraySsqIssue[beOptNum]) + "'")
                priorBeOptSet = currentBeOptSet

    # 清空动态元数据表(# 判断T00_RANGE_DYNAMIC是否存在，存在则drop后创建，否则直接创建)
    def init_range_dynamic_table(self):
        self.sql.execute("select count(*) from sqlite_master where type = 'table' and tbl_name = 'T00_RANGE_DYNAMIC'")
        if 0 not in self.sql.fetchone():
            self.sql.execute("DROP TABLE  [T00_RANGE_DYNAMIC]")
        self.sql.execute("CREATE TABLE [T00_RANGE_DYNAMIC] ([period] INT(7), [id] CHAR(4), [v] INT(2), [a] CHAR(2), [b] CHAR(2), [c] CHAR(2), [d] CHAR(2), [e] CHAR(2), [f] CHAR(2), [flag] INT(1))")
        self.sql.execute("CREATE INDEX [INDEX_T00_RANGE_DYNAMIC_FLAG] ON [T00_RANGE_DYNAMIC] ([flag])")
        self.sql.execute("CREATE INDEX [INDEX_T00_RANGE_DYNAMIC_PERIOD_ID_FLAG_V] ON [T00_RANGE_DYNAMIC] ([period], [id], [flag], [v])")
        self.log.info("清空'动态元数据表'(t00_range_dynamic)成功")

    # 清空值域中间表(# 判断 T03_RANGE_MIDDLE、T03_RANGE_MIDDLE_DETAIL 是否存在，存在则drop后创建，否则直接创建)
    def init_t03_range_middle_and_detail(self):
        self.sql.execute("select count(*) from sqlite_master where type = 'table' and tbl_name = 'T03_RANGE_MIDDLE'")
        if 0 not in self.sql.fetchone():
            self.sql.execute("DROP TABLE  [T03_RANGE_MIDDLE]")

        self.sql.execute("select count(*) from sqlite_master where type = 'table' and tbl_name = 'T03_RANGE_MIDDLE_DETAIL'")
        if 0 not in self.sql.fetchone():
            self.sql.execute("DROP TABLE  [T03_RANGE_MIDDLE_DETAIL]")

        self.sql.execute("CREATE TABLE [T03_RANGE_MIDDLE] ([计算期号] INT(7), [组别] INT(3), [记录数] INT(2), [历史值域] VARCHAR2, [遗传值域] VARCHAR2, [边缘值域] VARCHAR2, [关注遗传周期] VARCHAR2, [关注边缘周期] VARCHAR2, [遗传周期] VARCHAR2, [边缘周期] VARCHAR2)")
        self.sql.execute("CREATE TABLE [T03_RANGE_MIDDLE_DETAIL] ([计算期号] INT(7), [交易码] CHAR(4), [组别] INT(3), [历史值域] VARCHAR2, [遗传值域] VARCHAR2, [边缘值域] VARCHAR2)")

        self.log.info("清空'值域中间表'(T03_RANGE_MIDDLE、T03_RANGE_MIDDLE_DETAIL)成功")

    # 清空值域结果配置表(# 判断 T03_RANGE_RESULT 是否存在，存在则drop后创建，否则直接创建)
    def init_t03_range_result_table(self):
        self.sql.execute("select count(*) from sqlite_master where type = 'table' and tbl_name = 'T03_RANGE_RESULT'")
        if 0 not in self.sql.fetchone():
            self.sql.execute("DROP TABLE  [T03_RANGE_RESULT]")

        self.sql.execute("CREATE TABLE [T03_RANGE_RESULT] ([开奖期号] INT(7), [交易码] CHAR(4), [组别] INT(3), [历史值域] VARCHAR2, [排除值域] VARCHAR2, [设置值域] VARCHAR2)")

        self.log.info("清空'值域结果配置表'(T03_RANGE_RESULT)成功")

    # 结束方法
    def finish(self):
        self.cx.commit()
        self.cx.close()
        # self.me.save()
        # self.me.close()
        self.log.info("All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "]")

    # 将T00_SET中o=1的记录中v的值中带有单位数字的补0变成双数，不然集合交集匹配不到，临时使用
    def tmp_replace_single_number(self):  # 将T00_SET中o=1的记录中v的值中带有单位数字的补0变成双数，不然集合交集匹配不到，临时使用
        self.sql.execute("select id,v from t00_set where o='1'")
        for seta in self.sql.fetchall():  # ('0478', '6 12 18 24 30')
            var = ""
            setb = seta[1].split(" ", seta[1].count(" "))  # ['2', '8', '14', '20', '26', '32', '13', '15', '16', '17', '18']
            print(str(setb))
            print(str(len(setb)))
            for setc in range(0, len(setb)):
                if len(setb[setc]) == 1:
                    if var != "":
                        var = var + " " + "0" + setb[setc]
                    else:
                        var = "0" + setb[setc]
                else:
                    if var != "":
                        var = var + " " + setb[setc]
                    else:
                        var = setb[setc]
            self.sql.execute("update t00_set set v='" + var + "' where id='" + seta[0] + "'")

    # 校验 T00_DATA_ANALYZE_INSIDE 表与备份表中的数据前后是否一致
    def data_checkout(self):  # 校验 T00_DATA_ANALYZE_INSIDE 表与备份表中的数据前后是否一致
        self.sql.execute("select sql from sqlite_master where name = 'T00_DATA_ANALYZE_INSIDE'")
        for val in self.sql.fetchall(): pass
        dcColumn = int(str(val).count("\\r\\n"))
        self.sql.execute("select count(*) from T00_DATA_ANALYZE_INSIDE")
        for val in self.sql.fetchall(): pass
        dcRow = int(str(val[0]))

        self.sql.execute("select * from T00_DATA_ANALYZE_INSIDE")
        dcNew = self.sql.fetchall()
        self.sql.execute("select * from T00_DATA_ANALYZE_INSIDE_BK")
        dcBackup = self.sql.fetchall()

        flag = 0
        for dcr in range(0, dcRow):  # 一行一行的比对
            for dcc in range(0, dcColumn):
                if dcNew[dcr][dcc] != dcBackup[dcr][dcc]:
                    self.log.error(str(dcr + 1) + "-开奖期号：" + str(dcNew[dcr][0]) + ",列号：" + "0" + str(dcc - 39) + "；数据不同")
                    flag = 1
        if flag == 0: self.log.info("check is ok ,no have data is different.")

    # def test_set(self):  # 测试集合操作运算
    #     self.sql.execute("select * from a")
    #     rst_a = self.sql.fetchall()
    #     self.sql.execute("select * from b")
    #     rst_b = self.sql.fetchall()
    #     self.log.info("")
    #     self.log.info("集合a    " + str(rst_a))
    #     self.log.info("集合a    " + str(rst_b))
    #     self.log.info("")
    #     self.log.info("交集     " + str(set(rst_a) & set(rst_b)))
    #     self.log.info("并集     " + str(set(rst_a) | set(rst_b)))
    #     self.log.info("差集a-b  " + str(set(rst_a) - set(rst_b)))
    #     self.log.info("差集b-a  " + str(set(rst_b) - set(rst_a)))
    #     self.log.info("")
    #     self.log.info("测试对运算后的结果进行遍历处理：")
    #
    #     for val in set(rst_a) & set(rst_b):
    #         self.log.info(val)
    #         self.log.info(val[5])

    # 将统计数据插入excel
    def easy_excel_impl(self):
        self.sql.execute("select count(*) from t00_data_analyze_inside")
        total_row_count = self.sql.fetchone()[0]
        self.sql.execute("select * from t00_data_analyze_inside")
        v_num = 1  # 记录填充的行数
        v_row = 5  # 从第5行开始填充
        for record in self.sql.fetchall():
            self.log.debug("insert into excel,共" + str(total_row_count) + "行，正在写入第" + str(v_num) + "行")
            for col_num in range(1, len(record) - 5):  # excel列数（比数据库表中列少6个）
                if col_num == 1:
                    self.me.setCell("Sheet1", v_row, col_num, str(v_num))  # 写入该行行号
                elif col_num == 2:
                    self.me.setCell("Sheet1", v_row, col_num, record[0])  # 写入该行期号
                else:
                    self.me.setCell("Sheet1", v_row, col_num, record[col_num + 4])
            v_num += 1  # 记录填充的行数+1
            v_row += 1  # 行游标下移一个

    # 创建排除规则，结果装入 T03_RANGE_MIDDLE + T03_RANGE_MIDDLE_DETAIL 两张表
    def create_exclude_rule(self, period_num):
        # insert into T03_RANGE_MIDDLE values(period_num, mapping[1], self.sql.fetchone()[0], 'str(sorted(yc_union)))', 'str(sorted(his_union ^ yc_union))', 'v_yc_result', 'v_by_result', '关注遗传周期', '关注边缘周期')
        # insert into T03_RANGE_MIDDLE_DETAIL values(period_num, 'mapping[0]', mapping[1], 'str(sorted(his_union))', 'str(sorted(yc_union))', 'str(sorted(his_union ^ yc_union))')
        before_mapping_1 = "1"  # 初始化保留上一组别的变量
        his_union = {}  # 历史值域集合
        yc_union = {}  # 遗传值域集合
        by_map = {}  # 边缘算法字典
        yc_map = {}  # 遗传算法字典
        v_by_result = ""  # 边缘算法结果，为入库准备
        v_yc_result = ""  # 遗传算法结果，为入库准备
        self.sql.execute("select 交易码,组别 from t03_mapping")
        trancode_flag_rst = self.sql.fetchall()
        for v_count, mapping in enumerate(trancode_flag_rst):  # 一列一列的处理

            # 换组别后统一执行一次汇总操作（动这里下面就也要一起动，两个是一样的）
            if before_mapping_1 != str(mapping[1]):
                self.log.debug("")
                self.log.debug("历史值域并集：" + str(sorted(his_union)))
                self.log.debug("遗传值域并集：" + str(sorted(yc_union)))
                self.log.debug("最终边缘值域：" + str(sorted(his_union ^ yc_union)))
                self.log.debug("全部边缘算法获取下标 - 字典：" + str(by_map))
                self.log.debug("遗传值算法获取下标 - 字典：" + str(yc_map))
                self.log.debug("")

                # 获取当前组别对应的交易码
                self.sql.execute("select 交易码 from t03_mapping where 组别 = '" + before_mapping_1 + "'")
                flag_rst = self.sql.fetchall()
                for his_val in sorted(his_union):  # 用所有历史值域作为大循环的基础
                    opt_by_keys = []
                    for v_trancode in flag_rst:  # 每个历史值域值对应一遍当前组别的所有交易码进行循环处理
                        if v_trancode[0] + "-" + his_val in by_map.keys(): opt_by_keys.append(v_trancode[0] + "-" + his_val)

                    self.log.debug(opt_by_keys)

                    # 边缘（by）内部最小周期
                    by_list_all = []
                    for by_key in opt_by_keys:
                        v_num = 0
                        up_by_value = 0
                        by_list_one = []

                        if len(by_map[by_key]) != 1:
                            for by_value in by_map[by_key]:
                                if v_num != 0:
                                    by_list_one.append(by_value - up_by_value - 1)
                                v_num += 1
                                up_by_value = by_value
                            by_list_all.append(sorted(by_list_one)[0])
                    if len(by_list_all) == 0:
                        self.log.info(his_val + "的边缘最小内部周期为：@")
                        if v_by_result == "":
                            v_by_result = his_val + ":@"
                        else:
                            v_by_result = v_by_result + his_val + ":@"
                    else:
                        self.log.info(his_val + "的边缘最小内部周期为：" + str(sorted(by_list_all)[0]))
                        if v_by_result == "":
                            v_by_result = his_val + ":" + str(sorted(by_list_all)[0])
                        else:
                            v_by_result = v_by_result + his_val + ":" + str(sorted(by_list_all)[0])

                    # 边缘（by）外部最小周期
                    opt_ed_keys = []  # 已处理过的key
                    by_out_list_all = []
                    end_flag = 0  # 循环结束标志
                    for by_all_key in opt_by_keys:  # 大循环-主循环列-所有都循环一遍
                        opt_ed_keys.append(by_all_key)  # 保存正在处理和已经处理过的列
                        for by_cur_value in by_map[by_all_key]:  # 当前正在处理的列值
                            for by_mid_key in set(opt_by_keys) ^ set(opt_ed_keys):  # 中间key，需要排除当前和已处理过的列
                                for by_mid_value in by_map[by_mid_key]:  # 中间列值
                                    if by_cur_value - by_mid_value != 0:  # 同一行的就忽略掉，否则计算绝对值
                                        if abs(by_cur_value - by_mid_value) == 1:  # 如果外部最小周期有为1的，保存后，直接退出循环
                                            by_out_list_all.append(abs(by_cur_value - by_mid_value) - 1)
                                            end_flag = 1
                                            break
                                        else:  # 否则保存绝对值后继续循环处理
                                            by_out_list_all.append(abs(by_cur_value - by_mid_value) - 1)
                                if end_flag == 1: break
                            if end_flag == 1: break
                        if end_flag == 1: break
                    if len(by_out_list_all) == 0:
                        self.log.info(his_val + "的边缘最小外部周期为：@")
                        if v_by_result != "":
                            v_by_result += "|@;"
                    else:
                        self.log.info(his_val + "的边缘最小外部周期为：" + str(sorted(by_out_list_all)[0]))
                        if v_by_result != "":
                            v_by_result = v_by_result + "|" + str(sorted(by_out_list_all)[0]) + ";"

                self.log.debug("")

                for yc_val in sorted(yc_union):  # 用所有遗传值域作为大循环的基础
                    opt_yc_keys = []
                    for v_trancode in flag_rst:  # 每个历史值域值对应一遍当前组别的所有交易码进行循环处理
                        if v_trancode[0] + "-" + yc_val in yc_map.keys(): opt_yc_keys.append(v_trancode[0] + "-" + yc_val)

                    self.log.debug(opt_yc_keys)

                    # 遗传（yc）内部最小周期
                    yc_list_all = []
                    for yc_key in opt_yc_keys:
                        v_num = 0
                        up_yc_value = 0
                        yc_list_one = []

                        if len(yc_map[yc_key]) != 1:
                            for yc_value in yc_map[yc_key]:
                                if v_num != 0:
                                    yc_list_one.append(yc_value - up_yc_value - 1)
                                v_num += 1
                                up_yc_value = yc_value
                            yc_list_all.append(sorted(yc_list_one)[0])
                    if len(yc_list_all) == 0:
                        self.log.info(yc_val + "的遗传最小内部周期为：@")
                        if v_yc_result == "":
                            v_yc_result = yc_val + ":@"
                        else:
                            v_yc_result = v_yc_result + yc_val + ":@"
                    else:
                        self.log.info(yc_val + "的遗传最小内部周期为：" + str(sorted(yc_list_all)[0]))
                        if v_yc_result == "":
                            v_yc_result = yc_val + ":" + str(sorted(yc_list_all)[0])
                        else:
                            v_yc_result = v_yc_result + yc_val + ":" + str(sorted(yc_list_all)[0])

                    # 遗传（yc）外部最小周期
                    opt_ed_keys = []  # 已处理过的key
                    yc_out_list_all = []
                    end_flag = 0  # 循环结束标志
                    for yc_all_key in opt_yc_keys:  # 大循环-主循环列-所有都循环一遍
                        opt_ed_keys.append(yc_all_key)  # 保存正在处理和已经处理过的列
                        for yc_cur_value in yc_map[yc_all_key]:  # 当前正在处理的列值
                            for yc_mid_key in set(opt_yc_keys) ^ set(opt_ed_keys):  # 中间key，需要排除当前和已处理过的列
                                for yc_mid_value in yc_map[yc_mid_key]:  # 中间列值
                                    if yc_cur_value - yc_mid_value != 0:  # 同一行的就忽略掉，否则计算绝对值
                                        if abs(yc_cur_value - yc_mid_value) == 1:  # 如果外部最小周期有为0的，保存后，直接退出循环
                                            yc_out_list_all.append(abs(yc_cur_value - yc_mid_value) - 1)
                                            end_flag = 1
                                            break
                                        else:  # 否则保存绝对值后继续循环处理
                                            yc_out_list_all.append(abs(yc_cur_value - yc_mid_value) - 1)
                                if end_flag == 1: break
                            if end_flag == 1: break
                        if end_flag == 1: break
                    if len(yc_out_list_all) == 0:
                        self.log.info(yc_val + "的遗传最小外部周期为：@")
                        if v_yc_result != "":
                            v_yc_result += "|@;"
                    else:
                        self.log.info(yc_val + "的遗传最小外部周期为：" + str(sorted(yc_out_list_all)[0]))
                        if v_yc_result != "":
                            v_yc_result = v_yc_result + "|" + str(sorted(yc_out_list_all)[0]) + ";"

                self.log.debug("")
                self.log.debug("边缘算法结果：" + v_by_result)
                self.log.debug("遗传算法结果：" + v_yc_result)

                v_opt_yc_result = ""
                v_opt_by_result = ""
                self.sql.execute("select count(*) from t03_mapping where 组别 = '" + before_mapping_1 + "'")
                v_record_num = self.sql.fetchone()[0]

                if v_record_num == 1:
                    v_yc_result = v_yc_result.replace("|@", "")
                    v_by_result = v_by_result.replace("|@", "")
                    v_yc_1 = v_yc_result[0:-1].split(";", v_yc_result.count(";"))
                    v_by_1 = v_by_result[0:-1].split(";", v_by_result.count(";"))
                    if v_yc_result != "":
                        for v_yc_2 in v_yc_1:
                            if v_yc_2.split(":", 1)[1] != "0":
                                if v_opt_yc_result == "":
                                    v_opt_yc_result = v_yc_2 + ";"
                                else:
                                    v_opt_yc_result = v_opt_yc_result + v_yc_2 + ";"

                    if v_by_result != "":
                        for v_by_2 in v_by_1:
                            if v_by_2.split(":", 1)[1] != "0":
                                if v_opt_by_result == "":
                                    v_opt_by_result = v_by_2 + ";"
                                else:
                                    v_opt_by_result = v_opt_by_result + v_by_2 + ";"
                else:
                    v_yc_1 = v_yc_result[0:-1].split(";", v_yc_result.count(";"))
                    v_by_1 = v_by_result[0:-1].split(";", v_by_result.count(";"))
                    if v_yc_result != "":
                        for v_yc_2 in v_yc_1:
                            if v_yc_2.split(":", 1)[1].split("|", 1)[0] != "0" or v_yc_2.split(":", 1)[1].split("|", 1)[1] != "0":
                                if v_opt_yc_result == "":
                                    v_opt_yc_result = v_yc_2 + ";"
                                else:
                                    v_opt_yc_result = v_opt_yc_result + v_yc_2 + ";"

                    if v_by_result != "":
                        for v_by_2 in v_by_1:
                            if v_by_2.split(":", 1)[1].split("|", 1)[0] != "0" or v_by_2.split(":", 1)[1].split("|", 1)[1] != "0":
                                if v_opt_by_result == "":
                                    v_opt_by_result = v_by_2 + ";"
                                else:
                                    v_opt_by_result = v_opt_by_result + v_by_2 + ";"

                self.sql.execute("insert into T03_RANGE_MIDDLE values(" + period_num + "," + before_mapping_1 + "," + str(v_record_num) + ",'" + str(sorted(his_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(yc_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(his_union ^ yc_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + v_opt_yc_result + "', '" + v_opt_by_result + "', '" + v_yc_result + "','" + v_by_result + "')")

                self.log.debug("-----------------------------------------------------------------------------------------------------")
                his_union = {}
                yc_union = {}
                by_map = {}
                yc_map = {}
                v_by_result = ""
                v_yc_result = ""
            else:
                self.log.debug("")

            # 获取列的值，并把列的值装入数组，为后续统计计算做准备
            col_array = []  # 原始列数组
            self.sql.execute("select \"" + mapping[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= '" + period_num + "'")
            for value in self.sql.fetchall():  # 把一列的值装入数组
                if value[0] != "":
                    col_array.append(value[0])

            self.log.debug(mapping[0] + " - " + str(mapping[1]) + " - 原始列值 - " + str(col_array))
            self.log.debug(mapping[0] + " - " + str(mapping[1]) + " - 历史值域 - " + str(sorted(set(col_array))))

            # 统计元素个数
            for var in sorted(set(col_array)):
                self.log.info(mapping[0] + " - " + str(mapping[1]) + " - 个数统计 - " + var + "有" + str(col_array.count(var)) + "个")

            # 获取单列遗传值
            list_yc = []
            v_up = ""
            v_num = 0
            for var in col_array:
                if v_num != 0:
                    if v_up == var:
                        list_yc.append(var)
                v_num += 1
                v_up = var
            self.log.debug(mapping[0] + " - " + str(mapping[1]) + " - 遗传值域 - " + str(sorted(set(list_yc))))

            # 获取单列准边缘值
            list_zby = set(list_yc) ^ set(col_array)
            self.log.debug(mapping[0] + " - " + str(mapping[1]) + " - 准边缘值 - " + str(sorted(list_zby)))

            # 记录每列的详细值域信息
            # self.log.debug("insert into T03_RANGE_MIDDLE_DETAIL values(" + period_num + ",'" + str(mapping[0]) + "'," + str(mapping[1]) + ",'" + str(sorted(set(col_array))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(set(list_yc))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(list_zby)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "')")
            self.sql.execute("insert into T03_RANGE_MIDDLE_DETAIL values(" + period_num + ",'" + str(mapping[0]) + "'," + str(mapping[1]) + ",'" + str(sorted(set(col_array))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(set(list_yc))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(list_zby)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "')")

            # 全部边缘算法获取下标
            for var in sorted(set(col_array)):
                all_by_position = [x for x, y in enumerate(col_array) if y == var]
                self.log.debug(str(mapping[0] + "-" + var) + " - 全部边缘算法获取下标 - " + str(all_by_position))
                by_map[mapping[0] + "-" + var] = all_by_position

            # 遗传值算法获取下标
            for var in set(list_yc):  # 遍历该列的遗传值进行循环处理
                v_num = 0
                v_up_val = 0
                v_tmp_list = []
                # self.log.debug(by_map[mapping[0] + "-" + var])
                for v_cur_val in by_map[mapping[0] + "-" + var]:  # 从字典中取出该遗传值对应的"全部边缘算法下标"，并转换遗传值算法下标装入新字典中保存
                    if v_num != 0 and v_cur_val == v_up_val + 1: v_tmp_list.append(v_cur_val)
                    v_up_val = v_cur_val
                    v_num += 1
                yc_map[mapping[0] + "-" + var] = v_tmp_list

            # 获取历史值域并集
            if len(his_union) != 0:
                his_union |= set(col_array)
            else:
                his_union = set(col_array)

            # 获取遗传值域并集
            if len(yc_union) != 0:
                yc_union |= set(list_yc)
            else:
                yc_union = set(list_yc)

            if len(trancode_flag_rst) == v_count + 1:  # 最后一次循环的时候执行
                self.log.debug("")
                self.log.debug("历史值域并集：" + str(sorted(his_union)))
                self.log.debug("遗传值域并集：" + str(sorted(yc_union)))
                self.log.debug("最终边缘值域：" + str(sorted(his_union ^ yc_union)))
                self.log.debug("全部边缘算法获取下标 - 字典：" + str(by_map))
                self.log.debug("遗传值算法获取下标 - 字典：" + str(yc_map))
                self.log.debug("")

                # 获取当前组别对应的交易码
                self.sql.execute("select 交易码 from t03_mapping where 组别 = '" + str(mapping[1]) + "'")
                flag_rst = self.sql.fetchall()
                for his_val in sorted(his_union):  # 用所有历史值域作为大循环的基础
                    opt_by_keys = []
                    for v_trancode in flag_rst:  # 每个历史值域值对应一遍当前组别的所有交易码进行循环处理
                        if v_trancode[0] + "-" + his_val in by_map.keys(): opt_by_keys.append(v_trancode[0] + "-" + his_val)

                    self.log.debug(opt_by_keys)

                    # 边缘（by）内部最小周期
                    by_list_all = []
                    for by_key in opt_by_keys:
                        v_num = 0
                        up_by_value = 0
                        by_list_one = []

                        if len(by_map[by_key]) != 1:
                            for by_value in by_map[by_key]:
                                if v_num != 0:
                                    by_list_one.append(by_value - up_by_value - 1)
                                v_num += 1
                                up_by_value = by_value
                            by_list_all.append(sorted(by_list_one)[0])
                    if len(by_list_all) == 0:
                        self.log.info(his_val + "的边缘最小内部周期为：@")
                        if v_by_result == "":
                            v_by_result = his_val + ":@"
                        else:
                            v_by_result = v_by_result + his_val + ":@"
                    else:
                        self.log.info(his_val + "的边缘最小内部周期为：" + str(sorted(by_list_all)[0]))
                        if v_by_result == "":
                            v_by_result = his_val + ":" + str(sorted(by_list_all)[0])
                        else:
                            v_by_result = v_by_result + his_val + ":" + str(sorted(by_list_all)[0])

                    # 边缘（by）外部最小周期
                    opt_ed_keys = []  # 已处理过的key
                    by_out_list_all = []
                    end_flag = 0  # 循环结束标志
                    for by_all_key in opt_by_keys:  # 大循环-主循环列-所有都循环一遍
                        opt_ed_keys.append(by_all_key)  # 保存正在处理和已经处理过的列
                        for by_cur_value in by_map[by_all_key]:  # 当前正在处理的列值
                            for by_mid_key in set(opt_by_keys) ^ set(opt_ed_keys):  # 中间key，需要排除当前和已处理过的列
                                for by_mid_value in by_map[by_mid_key]:  # 中间列值
                                    if by_cur_value - by_mid_value != 0:  # 同一行的就忽略掉，否则计算绝对值
                                        if abs(by_cur_value - by_mid_value) == 1:  # 如果外部最小周期有为1的，保存后，直接退出循环
                                            by_out_list_all.append(abs(by_cur_value - by_mid_value) - 1)
                                            end_flag = 1
                                            break
                                        else:  # 否则保存绝对值后继续循环处理
                                            by_out_list_all.append(abs(by_cur_value - by_mid_value) - 1)
                                if end_flag == 1: break
                            if end_flag == 1: break
                        if end_flag == 1: break
                    if len(by_out_list_all) == 0:
                        self.log.info(his_val + "的边缘最小外部周期为：@")
                        if v_by_result != "":
                            v_by_result += "|@;"
                    else:
                        self.log.info(his_val + "的边缘最小外部周期为：" + str(sorted(by_out_list_all)[0]))
                        if v_by_result != "":
                            v_by_result = v_by_result + "|" + str(sorted(by_out_list_all)[0]) + ";"

                self.log.debug("")

                for yc_val in sorted(yc_union):  # 用所有遗传值域作为大循环的基础
                    opt_yc_keys = []
                    for v_trancode in flag_rst:  # 每个历史值域值对应一遍当前组别的所有交易码进行循环处理
                        if v_trancode[0] + "-" + yc_val in yc_map.keys(): opt_yc_keys.append(v_trancode[0] + "-" + yc_val)

                    self.log.debug(opt_yc_keys)

                    # 遗传（yc）内部最小周期
                    yc_list_all = []
                    for yc_key in opt_yc_keys:
                        v_num = 0
                        up_yc_value = 0
                        yc_list_one = []

                        if len(yc_map[yc_key]) != 1:
                            for yc_value in yc_map[yc_key]:
                                if v_num != 0:
                                    yc_list_one.append(yc_value - up_yc_value - 1)
                                v_num += 1
                                up_yc_value = yc_value
                            yc_list_all.append(sorted(yc_list_one)[0])
                    if len(yc_list_all) == 0:
                        self.log.info(yc_val + "的遗传最小内部周期为：@")
                        if v_yc_result == "":
                            v_yc_result = yc_val + ":@"
                        else:
                            v_yc_result = v_yc_result + yc_val + ":@"
                    else:
                        self.log.info(yc_val + "的遗传最小内部周期为：" + str(sorted(yc_list_all)[0]))
                        if v_yc_result == "":
                            v_yc_result = yc_val + ":" + str(sorted(yc_list_all)[0])
                        else:
                            v_yc_result = v_yc_result + yc_val + ":" + str(sorted(yc_list_all)[0])

                    # 遗传（yc）外部最小周期
                    opt_ed_keys = []  # 已处理过的key
                    yc_out_list_all = []
                    end_flag = 0  # 循环结束标志
                    for yc_all_key in opt_yc_keys:  # 大循环-主循环列-所有都循环一遍
                        opt_ed_keys.append(yc_all_key)  # 保存正在处理和已经处理过的列
                        for yc_cur_value in yc_map[yc_all_key]:  # 当前正在处理的列值
                            for yc_mid_key in set(opt_yc_keys) ^ set(opt_ed_keys):  # 中间key，需要排除当前和已处理过的列
                                for yc_mid_value in yc_map[yc_mid_key]:  # 中间列值
                                    if yc_cur_value - yc_mid_value != 0:  # 同一行的就忽略掉，否则计算绝对值
                                        if abs(yc_cur_value - yc_mid_value) == 1:  # 如果外部最小周期有为0的，保存后，直接退出循环
                                            yc_out_list_all.append(abs(yc_cur_value - yc_mid_value) - 1)
                                            end_flag = 1
                                            break
                                        else:  # 否则保存绝对值后继续循环处理
                                            yc_out_list_all.append(abs(yc_cur_value - yc_mid_value) - 1)
                                if end_flag == 1: break
                            if end_flag == 1: break
                        if end_flag == 1: break
                    if len(yc_out_list_all) == 0:
                        self.log.info(yc_val + "的遗传最小外部周期为：@")
                        if v_yc_result != "":
                            v_yc_result += "|@;"
                    else:
                        self.log.info(yc_val + "的遗传最小外部周期为：" + str(sorted(yc_out_list_all)[0]))
                        if v_yc_result != "":
                            v_yc_result = v_yc_result + "|" + str(sorted(yc_out_list_all)[0]) + ";"

                self.log.debug("")
                self.log.debug("边缘算法结果：" + v_by_result)
                self.log.debug("遗传算法结果：" + v_yc_result)

                v_opt_yc_result = ""
                v_opt_by_result = ""
                self.sql.execute("select count(*) from t03_mapping where 组别 = '" + str(mapping[1]) + "'")
                v_record_num = self.sql.fetchone()[0]

                if v_record_num == 1:
                    v_yc_result = v_yc_result.replace("|@", "")
                    v_by_result = v_by_result.replace("|@", "")
                    v_yc_1 = v_yc_result[0:-1].split(";", v_yc_result.count(";"))
                    v_by_1 = v_by_result[0:-1].split(";", v_by_result.count(";"))
                    if v_yc_result != "":
                        for v_yc_2 in v_yc_1:
                            if v_yc_2.split(":", 1)[1] != "0":
                                if v_opt_yc_result == "":
                                    v_opt_yc_result = v_yc_2 + ";"
                                else:
                                    v_opt_yc_result = v_opt_yc_result + v_yc_2 + ";"

                    if v_by_result != "":
                        for v_by_2 in v_by_1:
                            if v_by_2.split(":", 1)[1] != "0":
                                if v_opt_by_result == "":
                                    v_opt_by_result = v_by_2 + ";"
                                else:
                                    v_opt_by_result = v_opt_by_result + v_by_2 + ";"
                else:
                    v_yc_1 = v_yc_result[0:-1].split(";", v_yc_result.count(";"))
                    v_by_1 = v_by_result[0:-1].split(";", v_by_result.count(";"))
                    if v_yc_result != "":
                        for v_yc_2 in v_yc_1:
                            if v_yc_2.split(":", 1)[1].split("|", 1)[0] != "0" or v_yc_2.split(":", 1)[1].split("|", 1)[1] != "0":
                                if v_opt_yc_result == "":
                                    v_opt_yc_result = v_yc_2 + ";"
                                else:
                                    v_opt_yc_result = v_opt_yc_result + v_yc_2 + ";"

                    if v_by_result != "":
                        for v_by_2 in v_by_1:
                            if v_by_2.split(":", 1)[1].split("|", 1)[0] != "0" or v_by_2.split(":", 1)[1].split("|", 1)[1] != "0":
                                if v_opt_by_result == "":
                                    v_opt_by_result = v_by_2 + ";"
                                else:
                                    v_opt_by_result = v_opt_by_result + v_by_2 + ";"

                self.sql.execute("insert into T03_RANGE_MIDDLE values(" + period_num + "," + str(mapping[1]) + "," + str(v_record_num) + ",'" + str(sorted(his_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(yc_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + str(sorted(his_union ^ yc_union)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "") + "','" + v_opt_yc_result + "', '" + v_opt_by_result + "', '" + v_yc_result + "','" + v_by_result + "')")

                self.log.debug("-----------------------------------------------------------------------------------------------------")

            # 保存当前操作的组别为上一组别
            before_mapping_1 = str(mapping[1])

    # 根据排除规则生成设定值域，为排除计算提供配置，结果装入 T03_RANGE_RESULT 一张表
    def create_exclude_config_for_result(self, period_num):

        self.sql.execute("select 组别,记录数,关注遗传周期,关注边缘周期 from T03_RANGE_MIDDLE where 计算期号 = " + period_num + " order by 组别")

        # 用排除规则表中的记录进行循环处理
        for rule_record in self.sql.fetchall():

            self.log.debug("-----------------------------------------------------------------------------------------------------")

            # 变量准备
            v_group = rule_record[0]  # 组别
            v_record_count = rule_record[1]  # 记录数
            v_point_yc_period = rule_record[2][0:-1]  # 关注遗传周期(去掉末尾分号)
            v_point_by_period = rule_record[3][0:-1]  # 关注边缘周期(去掉末尾分号)

            # 查出该配置对应的交易码，有多条、有一条（两种情况）
            self.sql.execute("select 交易码,遗传误差,边缘误差,遗传正无穷启用,边缘正无穷启用 from t03_mapping where 组别 =" + str(v_group))
            tran_code_result = self.sql.fetchall()

            # 处理单列的情况
            if v_record_count == 1:

                for v_tran_code in tran_code_result:

                    # 获取该列的历史值域
                    self.sql.execute("select 历史值域 from T03_RANGE_MIDDLE_DETAIL where 计算期号 =" + period_num + " and 交易码 = '" + v_tran_code[0] + "'")
                    v_his_range = self.sql.fetchone()[0]

                    # 单列 - 遗传值处理
                    tmp_single_inside_yc_result = []
                    if v_point_yc_period != "":
                        for v_rule in v_point_yc_period.split(";", v_point_yc_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                            v_key = v_rule.split(":", 1)[0]
                            v_value = v_rule.split(":", 1)[1]

                            # 单列 - 遗传值 - "正无穷" 类 处理
                            # 正无穷的情况，当期该列正好是遗传数值时，则过滤该值，否则 pass 不做任何处理
                            if v_value == "@":
                                if v_tran_code[3] != 0:
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 = " + period_num)
                                    if self.sql.fetchone()[0] == v_key:
                                        tmp_single_inside_yc_result.append(v_key)

                            # 单列 - 遗传值 - "数值" 类 处理
                            # 数值类遗传周期情况，假设遗传周期为5，那么要取出该列的后6条记录出来操作，如果最后一条记录正好是遗传数值时，要判断其他5条记录中是否有连续的该遗传值数出现（遗传现象），有则过滤该值，否则 pass 不做任何处理
                            else:
                                if int(v_value) + 1 - v_tran_code[1] < 0:
                                    v_limit = 0
                                else:
                                    v_limit = int(v_value) + 1 - v_tran_code[1]

                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                if self.sql.fetchone()[0] == v_key:
                                    v_tmp_up = ""
                                    v_tmp_num = 0
                                    v_tmp_flag = 0
                                    for val in self.sql.fetchall():
                                        if v_tmp_num != 0:
                                            if v_tmp_up == val[0] and v_tmp_up == v_key:
                                                v_tmp_flag = 1
                                        v_tmp_num += 1
                                        v_tmp_up = val[0]
                                    if v_tmp_flag == 1:
                                        tmp_single_inside_yc_result.append(v_key)

                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 单列遗传排除值域 - " + str(sorted(tmp_single_inside_yc_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))

                    # 单列 - 边缘值处理
                    tmp_single_inside_by_result = []
                    if v_point_by_period != "":
                        for v_rule in v_point_by_period.split(";", v_point_by_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                            v_key = v_rule.split(":", 1)[0]
                            v_value = v_rule.split(":", 1)[1]

                            # 单列 - 边缘值 - "正无穷" 类 处理，直接过滤该key的边缘值
                            if v_value == "@":
                                if v_tran_code[4] != 0:
                                    tmp_single_inside_by_result.append(v_key)

                            # 单列 - 边缘值 - "数值" 类 处理
                            # 数值类边缘周期情况，假设边缘周期为5，那么要取出该列的后5条记录出来操作，如果这5条记录中存在该边缘值，则过滤该值，否则 pass 不做任何处理
                            else:
                                if int(v_value) - v_tran_code[2] < 0:
                                    v_limit = 0
                                else:
                                    v_limit = int(v_value) - v_tran_code[2]

                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                for val in self.sql.fetchall():
                                    if v_key == val[0]:
                                        tmp_single_inside_by_result.append(v_key)
                                        break

                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 单列边缘排除值域 - " + str(sorted(tmp_single_inside_by_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))

                    # 以下为单列模式的处理汇总（遗传 + 边缘），需要汇总单列遗传值处理的结果
                    v_exclude_range = str(sorted(tmp_single_inside_yc_result + tmp_single_inside_by_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

                    self.log.debug("")
                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 单列历史值域 - " + v_his_range)
                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 单列总排除值域 - " + v_exclude_range)
                    if v_exclude_range == "":  # 排除值域为空则将历史值域赋值给设定值域
                        v_define_range = v_his_range
                    else:  # 排除值域不为空则将历史值域和排除值域去反差集
                        v_define_range = str(list(set(v_his_range.split(",", v_his_range.count(","))) ^ set(v_exclude_range.split(",", v_exclude_range.count(","))))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 单列设定值域 - " + v_define_range)

                    # 结果入库
                    self.sql.execute("insert into T03_RANGE_RESULT values(" + period_num + ",'" + v_tran_code[0] + "'," + str(v_group) + ",'" + v_his_range + "','" + v_exclude_range + "','" + v_define_range + "')")

            # 处理多列（块）的情况，采取分别处理，各个击破，最后汇总的策略进行计算
            else:

                # 初始化计算结果集map
                final_result_map = {}
                for v_tran_code in tran_code_result: final_result_map[v_tran_code[0]] = []

                self.log.debug("组别：" + str(v_group) + " 交易码个数：" + str(v_record_count) + " 初始化计算结果集map :" + str(final_result_map))
                self.log.debug("")

                # 处理多列内部（遗传+边缘），保存在map中 {0001:[排除值数组],0002：[排除值数组]...}
                for v_tran_code in tran_code_result:

                    # 多列 - 内部遗传值处理
                    tmp_many_inside_yc_result = []
                    if v_point_yc_period != "":
                        for v_rule in v_point_yc_period.split(";", v_point_yc_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                            v_key = v_rule.split(":", 1)[0]
                            v_value = v_rule.split(":", 1)[1].split("|", 1)[0]  # 取出遗传值内部周期

                            # 单列 - 遗传值 - "正无穷" 类 处理
                            # 正无穷的情况，当期该列正好是遗传数值时，则过滤该值，否则 pass 不做任何处理
                            if v_value == "@":
                                if v_tran_code[3] != 0:
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 = " + period_num)
                                    if self.sql.fetchone()[0] == v_key:
                                        self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc")
                                        v_tmp_up = ""
                                        v_tmp_num = 0
                                        v_tmp_flag = 0
                                        for val in self.sql.fetchall():
                                            if v_tmp_num != 0:
                                                if v_tmp_up == val[0] and v_tmp_up == v_key:
                                                    v_tmp_flag = 1
                                                    break
                                            v_tmp_num += 1
                                            v_tmp_up = val[0]
                                        if v_tmp_flag == 1:
                                            final_result_map[v_tran_code[0]].append(v_key)
                                            tmp_many_inside_yc_result.append(v_key)

                            # 单列 - 遗传值 - "数值" 类 处理
                            # 数值类遗传周期情况，假设遗传周期为5，那么要取出该列的后6条记录出来操作，如果最后一条记录正好是遗传数值时，要判断其他5条记录中是否有连续的该遗传值数出现（遗传现象），有则过滤该值，否则 pass 不做任何处理
                            else:
                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 = " + period_num)
                                if self.sql.fetchone()[0] == v_key:
                                    if int(v_value) + 1 - v_tran_code[1] < 0:
                                        v_limit = 0
                                    else:
                                        v_limit = int(v_value) + 1 - v_tran_code[1]

                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                    v_tmp_up = ""
                                    v_tmp_num = 0
                                    v_tmp_flag = 0
                                    for val in self.sql.fetchall():
                                        if v_tmp_num != 0:
                                            if v_tmp_up == val[0] and v_tmp_up == v_key:
                                                v_tmp_flag = 1
                                                break
                                        v_tmp_num += 1
                                        v_tmp_up = val[0]
                                    if v_tmp_flag == 1:
                                        final_result_map[v_tran_code[0]].append(v_key)
                                        tmp_many_inside_yc_result.append(v_key)

                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列内部遗传排除值域 - " + str(sorted(tmp_many_inside_yc_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))
                    # self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列内部遗传排除值域 - " + str(tmp_dl_yc_result))

                    # 多列 - 内部边缘值处理
                    tmp_many_inside_by_result = []
                    if v_point_by_period != "":
                        for v_rule in v_point_by_period.split(";", v_point_by_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                            v_key = v_rule.split(":", 1)[0]
                            v_value = v_rule.split(":", 1)[1].split("|", 1)[0]  # 取出边缘值内部周期

                            # 单列 - 边缘值 - "正无穷" 类 处理，直接过滤该key的边缘值
                            if v_value == "@":
                                if v_tran_code[4] != 0:
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc")
                                    for val in self.sql.fetchall():
                                        if v_key == val[0]:
                                            final_result_map[v_tran_code[0]].append(v_key)
                                            tmp_many_inside_by_result.append(v_key)
                                            break

                            # 单列 - 边缘值 - "数值" 类 处理
                            # 数值类边缘周期情况，假设边缘周期为5，那么要取出该列的后5条记录出来操作，如果这5条记录中存在该边缘值，则过滤该值，否则 pass 不做任何处理
                            else:
                                if int(v_value) - v_tran_code[2] < 0:
                                    v_limit = 0
                                else:
                                    v_limit = int(v_value) - v_tran_code[2]

                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                for val in self.sql.fetchall():
                                    if v_key == val[0]:
                                        final_result_map[v_tran_code[0]].append(v_key)
                                        tmp_many_inside_by_result.append(v_key)
                                        break

                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列内部边缘排除值域 - " + str(sorted(tmp_many_inside_by_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))
                    # 结果临时保存在 v_tmp_exclude_range_list 中，list类型

                self.log.debug("")
                self.log.debug("多列内部（遗传+边缘）排序算法计算完毕：" + str(final_result_map))
                self.log.debug("")

                # 处理多列外部（遗传+边缘），保存在追加到内部排除的map中 {0001:[排除值数组].append(xxx),0002：[排除值数组].append(xxx)...}
                # for v_tran_code in tran_code_result:

                # 多列 - 外部遗传值处理
                tmp_many_outside_yc_result = []
                if v_point_yc_period != "":

                    for v_rule in v_point_yc_period.split(";", v_point_yc_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                        v_key = v_rule.split(":", 1)[0]
                        v_value = v_rule.split(":", 1)[1].split("|", 1)[1]  # 取出遗传值外部周期

                        v_list_except = []   # 例外的交易码，即：存在遗传现象本身的列，需要排除掉
                        v_list_contain = []  # 末行出现遗传数值的列（与v_list_except有交集的时候不算，属于内部遗传情况范畴了，不是外部）
                        for v_tran_code in tran_code_result:

                            # 多列 - 遗传值 - "正无穷" 类 处理
                            # 正无穷的情况，当期该列正好是遗传数值时，则过滤该值，否则 pass 不做任何处理
                            if v_value == "@":
                                if v_tran_code[3] != 0:
                                    # 先判断末行
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 = " + period_num)  # 查该列末行
                                    if self.sql.fetchone()[0] == v_key: v_list_contain.append(v_tran_code[0])  # 末行是遗传数值说明此列需要关注是否排除该值，加入包含数组中保存

                                    # 再判断整列是否包含遗传情况
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc")
                                    v_tmp_up = ""
                                    v_tmp_num = 0
                                    v_tmp_flag = 0
                                    for val in self.sql.fetchall():
                                        if v_tmp_num != 0:
                                            if v_tmp_up == val[0] and v_tmp_up == v_key:
                                                v_tmp_flag = 1
                                                break
                                        v_tmp_num += 1
                                        v_tmp_up = val[0]

                                    if v_tmp_flag == 1: v_list_except.append(v_tran_code[0])  # 说明该列包含遗传现象，该列不在排除范围值内

                            # 多列 - 遗传值 - "数值" 类 处理
                            # 数值类遗传周期情况，假设遗传周期为5，那么要取出该列的后6条记录出来操作，如果最后一条记录正好是遗传数值时，要判断其他5条记录中是否有连续的该遗传值数出现（遗传现象），有则过滤该值，否则 pass 不做任何处理
                            else:

                                # 先判断末行
                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 = " + period_num)
                                if self.sql.fetchone()[0] == v_key: v_list_contain.append(v_tran_code[0])  # 末行是遗传数值说明此列需要关注是否排除该值，加入包含数组中保存

                                # 再判断整列是否包含遗传情况
                                if int(v_value) + 1 - v_tran_code[1] < 0:
                                    v_limit = 0
                                else:
                                    v_limit = int(v_value) + 1 - v_tran_code[1]

                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                v_tmp_up = ""
                                v_tmp_num = 0
                                v_tmp_flag = 0
                                for val in self.sql.fetchall():
                                    if v_tmp_num != 0:
                                        if v_tmp_up == val[0] and v_tmp_up == v_key:
                                            v_tmp_flag = 1
                                            break
                                    v_tmp_num += 1
                                    v_tmp_up = val[0]

                                if v_tmp_flag == 1: v_list_except.append(v_tran_code[0])  # 说明该列包含遗传现象，该列不在排除范围值内

                        if not v_list_contain == []:  # 如果存在末列是遗传数值的情况则需要处理，否则不做任何处理
                            for rst in [val for val in v_list_contain if val not in v_list_except]:
                                final_result_map[rst].append(v_key)
                                tmp_many_outside_yc_result.append(v_key)

                self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列外部遗传排除值域 - " + str(sorted(tmp_many_outside_yc_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))
                # self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列外部遗传排除值域 - " + str(tmp_dl_yc_result))

                # 多列 - 外部边缘值处理
                tmp_many_outside_by_result = []
                if v_point_by_period != "":

                    for v_rule in v_point_by_period.split(";", v_point_by_period.count(";")):  # 处理每一个规则，排除的结果塞入临时数组保存，最后去重排序后转成字符串保存到数据库结果表中

                        v_key = v_rule.split(":", 1)[0]
                        v_value = v_rule.split(":", 1)[1].split("|", 1)[1]  # 取出边缘值外部周期

                        v_list_except = []  # 例外的交易码，即：存在边缘值的列，需要排除掉
                        for v_tran_code in tran_code_result:

                            # 多列 - 边缘值 - "正无穷" 类 处理，直接过滤该key的边缘值
                            if v_value == "@":
                                if v_tran_code[4] != 0:
                                    self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc")
                                    v_tmp_flag = 0
                                    for val in self.sql.fetchall():
                                        if v_key == val[0]:  # 如果遗传值在该列中存在，则排除该列，装入v_list_except保存(块中所有交易码都循环检查一遍，存在则加入数组)
                                            v_tmp_flag = 1
                                            break

                                    if v_tmp_flag == 1: v_list_except.append(v_tran_code[0])  # 加入数组保存

                            # 多列 - 边缘值 - "数值" 类 处理
                            # 数值类边缘周期情况，假设边缘周期为5，那么要取出该列的后5条记录出来操作，如果这5条记录中存在该边缘值，则过滤该值，否则 pass 不做任何处理
                            else:
                                if int(v_value) - v_tran_code[2] < 0:
                                    v_limit = 0
                                else:
                                    v_limit = int(v_value) - v_tran_code[2]

                                self.sql.execute("select \"" + v_tran_code[0] + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号 <= " + period_num + " order by 开奖期号 desc limit " + str(v_limit))
                                v_tmp_flag = 0
                                for val in self.sql.fetchall():
                                    if v_key == val[0]:  # 如果遗传值在该列中存在，则排除该列，装入v_list_except保存(块中所有交易码都循环检查一遍，存在则加入数组)
                                        v_tmp_flag = 1
                                        break

                                if v_tmp_flag == 1: v_list_except.append(v_tran_code[0])  # 加入数组保存

                        if not v_list_except == []:
                            for v_tran_code in tran_code_result:
                                if v_tran_code[0] not in v_list_except:
                                    final_result_map[v_tran_code[0]].append(v_key)
                                    tmp_many_outside_by_result.append(v_key)

                self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列外部边缘排除值域 - " + str(sorted(tmp_many_outside_by_result)).replace("'", "").replace("[", "").replace("]", "").replace(" ", ""))
                # 结果临时保存在 v_tmp_exclude_range_list 中，list类型

                # 处理多列排数结果汇总，把结果从map中取出，将数组去重、排序后，按交易码区分，插入T03_RANGE_RESULT表
                for v_tran_code in tran_code_result:

                    # 获取该列的历史值域
                    self.sql.execute("select 历史值域 from T03_RANGE_MIDDLE_DETAIL where 计算期号 =" + period_num + " and 交易码 = '" + v_tran_code[0] + "'")
                    v_his_range = self.sql.fetchone()[0]

                    # v_exclude_range = str(sorted(final_result_map[v_tran_code[0]])).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
                    v_exclude_range = str(sorted(set([val for val in final_result_map[v_tran_code[0]] if val in v_his_range]))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列历史值域 - " + v_his_range)
                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列总排除值域 - " + v_exclude_range)
                    if v_exclude_range == "":  # 排除值域为空则将历史值域赋值给设定值域
                        v_define_range = v_his_range
                    else:  # 排除值域不为空则将历史值域和排除值域去反差集
                        v_define_range = str(list(set(v_his_range.split(",", v_his_range.count(","))) ^ set(v_exclude_range.split(",", v_exclude_range.count(","))))).replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
                    self.log.debug(v_tran_code[0] + " - " + str(v_group) + " - 多列设定值域 - " + v_define_range)

                    # 结果入库
                    self.sql.execute("insert into T03_RANGE_RESULT values(" + period_num + ",'" + v_tran_code[0] + "'," + str(v_group) + ",'" + v_his_range + "','" + v_exclude_range + "','" + v_define_range + "')")

    def xxx(self, exclude_rule=None):
        # self.sql.execute("select id,v,count(*) from t00_range group by id,v")
        # v_rst = self.sql.fetchall()
        # v_up_trancode = "0001"
        # v_num = 0
        # v_value = ""
        # v_value_count = ""
        # for v_count, val in enumerate(v_rst):
        #
        #     if v_up_trancode != val[0]:
        #         print(v_up_trancode + " - " + v_value + " - " + v_value_count)
        #         v_value = ""
        #         v_value_count = ""
        #
        #     if v_value == "":
        #         v_value = str(val[1])
        #     else:
        #         v_value = v_value + "," + str(val[1])
        #
        #     if v_value_count == "":
        #         v_value_count = str(val[1]) + ":" + str(val[2])
        #     else:
        #         v_value_count = v_value_count + " " + str(val[1]) + ":" + str(val[2])
        #
        #     if len(v_rst) == v_count + 1:
        #         print(v_up_trancode + " - " + v_value + " - " + v_value_count)
        #
        #     v_num += 1
        #     v_up_trancode = str(val[0])

        # self.sql.execute("select a,b,c from x")
        # for val in self.sql.fetchall():
        #     trancode = val[0]
        #     l_pc = val[1].split(",", val[1].count(","))
        #     l_his = val[2].split(",", val[2].count(","))
        #
        #     l_rst = str(list((tmp for tmp in l_his if tmp not in l_pc))).replace("[", "").replace("]", "").replace(" ", "").replace("'", "")
        #     print(str(l_pc) + " - " + str(l_his) + " - " + str(l_rst))
        #
        #     self.sql.execute("update t03_range_result set 历史值域 = '" + str(l_rst) + "' where 交易码 = '" + trancode + "'")

        self.sql.execute("DROP TABLE [T03_RANGE_RESULT]")
        self.sql.execute("CREATE TABLE [T03_RANGE_RESULT] ([交易码] CHAR(4), [设置值域] VARCHAR2)")

        _v_num = 0
        list_all_exclude_period = []  # 总被过滤掉的周期号
        list_all_period = []
        dict_exclude_period_tran_code = {}
        self.sql.execute("SELECT 开奖期号 FROM T00_DATA_ANALYZE_INSIDE")
        for val in self.sql.fetchall():
            dict_exclude_period_tran_code[val[0]] = []
            list_all_period.append(val[0])
        self.sql.execute("select 交易码 from T03_MAPPING where 启用 = 1 order by 交易码")
        for val in self.sql.fetchall():
            result = []
            tran_code = val[0]

            # 获得当期之前（包括当期）范围值域 - persend_range_set
            # persend_range_set = []
            # self.sql.execute("SELECT \"" + tran_code + "\" FROM T00_DATA_ANALYZE_INSIDE WHERE 开奖期号 <= '" + period_num + "'")
            # for val in self.sql.fetchall():
            #     if val[0] != "":
            #         persend_range_set.append(val[0])
            # persend_range_set = list(set(persend_range_set))
            # self.log.debug("【" + tran_code + "】当期之前范围值域为： " + str(persend_range_set))

            # 获得所有期范围值域 - all_range_set
            all_range = []
            self.sql.execute("SELECT \"" + tran_code + "\",开奖期号 FROM T00_DATA_ANALYZE_INSIDE")
            range_rst = self.sql.fetchall()
            for val in range_rst:
                if val[0] != "":
                    all_range.append(val[0])
            all_range_set = list(set(all_range))
            self.log.debug("【" + tran_code + "】所有期范围值域为： " + str(all_range_set))

            # 获得排除值 - exclude_range
            if exclude_rule:  # 如果排除规则不为空
                exclude_rule_list = exclude_rule.split(",", exclude_rule.count(","))
                exclude_range = []
                range_count = {}
                for erl in exclude_rule_list:
                    for val in all_range_set:
                        range_count[val[0]] = all_range.count(val[0])
                        if erl == str(all_range.count(val[0])):
                            exclude_range.append(val[0])
                    self.log.debug("【" + tran_code + "】排除规则为： " + erl + " 排除值域为： " + str(exclude_range))
                self.log.debug("【" + tran_code + "】值域值数量统计 - " + str(range_count))
            else:
                self.log.debug("【" + tran_code + "】传入排除规则为空，默认设定为历史值域")

            if exclude_rule and exclude_range != []:
                result = list(sorted((val for val in all_range_set if val not in exclude_range)))
                self.log.debug("【" + tran_code + "】 ====ｐｃ==== 最终设置值域为： " + str(result))

                # 额外添加，获取排除的期号信息
                list_tmp_exclude_period = []  # 当前交易码过滤掉的周期号
                for val in exclude_range:
                    for value_periodnum in range_rst:
                        if val == value_periodnum[0]:
                            list_tmp_exclude_period.append(value_periodnum[1])
                            dict_exclude_period_tran_code[value_periodnum[1]].append(tran_code)
                self.log.debug("【" + tran_code + "】过滤掉的周期为： " + str(list_tmp_exclude_period))
                list_all_exclude_period += list_tmp_exclude_period


            else:
                result = list(sorted(all_range_set))
                self.log.debug("【" + tran_code + "】最终设置值域为： " + str(result))

            self.sql.execute("insert into T03_RANGE_RESULT values('" + tran_code + "','" + str(result).replace("[", "").replace("]", "").replace("'", "").replace(" ", "") + "')")

            _v_num += 1
            self.log.debug("----------------------------------------------------------------------------------------------------------------------------")

        self.log.debug("")
        self.log.debug("过滤周期个数 / 总周期个数：" + str(len(set(list_all_exclude_period))) + "/" + str(len(set(list_all_period))) + "     剩余周期个数：" + str(len(set(list_all_period))-len(set(list_all_exclude_period))))
        self.log.debug("总过滤掉的周期为： " + str(sorted(set(list_all_exclude_period))))
        self.log.debug("余下周期为： " + str(sorted(val for val in set(list_all_period) if val not in set(list_all_exclude_period))))
        self.log.debug("共计算:" + str(_v_num) + "个设置值域")

        for val in sorted(set(list_all_exclude_period)):
            self.log.debug("被过滤周期个数统计：" + str(val) + " - " + str(list_all_exclude_period.count(val)) + "  被谁过滤的: " + str(dict_exclude_period_tran_code[val]))

    def yyy(self):
        self.sql.execute("select 开奖期号 from T00_DATA_ANALYZE_INSIDE")
        rst = self.sql.fetchall()
        v_num = 0
        v_up = ""
        for val in rst:
            if v_num == 0:
                v_up = val[0]

            print(str(val[0])[4:])

            v_num += 1

    def write_range(self, period_num):
        self.sql.execute("delete from T00_DATA_ANALYZE_INSIDE where 开奖期号='9999999'")
        self.sql.execute("insert into T00_DATA_ANALYZE_INSIDE (开奖期号) values ('9999999')")
        self.sql.execute("select 交易码, 设置值域 from t03_range_result")
        rst1 = self.sql.fetchall()
        for var in rst1:
            v_code = var[0]
            v_value = var[1]
            self.sql.execute("update T00_DATA_ANALYZE_INSIDE set \"" + v_code + "\"='" + v_value + "' where 开奖期号='9999999'")

        for var in rst1:
            v_code = var[0]
            v_value = var[1]
            self.sql.execute("select \"" + v_code + "\" from T00_DATA_ANALYZE_INSIDE where 开奖期号='" + period_num + "'")
            rst2 = self.sql.fetchone()[0]
            v_list = v_value.split(",", v_value.count(","))
            if rst2 not in v_list:
                print(v_code)


if __name__ == '__main__':
    csr = SourceDataOperation()  # 实例化类对象

    # csr.tmp_replace_single_number()                  # 将T00_SET中o=1的记录中v的值中带有单位数字的补0变成双数，不然集合交集匹配不到，临时使用

    # csr.get_open_award_source_data()                 # 获取"历届开奖结果"元数据(依赖于Internet)
    # csr.get_model_set()                              # 获取"模型集合"(依赖开奖结果元数据:大号三个[17-33]，偶数三个[偶16奇17]，区间2-2-2[1-11][12-22][23-33],共计29700条记录)
    # csr.get_statistics_value()                       # 获取"统计值"(依赖配置表t00_set)

    # csr.create_set_range()                           # 创建"集合值域"元数据(依赖配置表t00_set)    03:39
    # csr.create_every_count()                         # 创建"各项数量统计"元数据(依赖配置表t00_set)
    # csr.create_others()                              # 间距与位势、和值、综合常规、集合元数据（静态）

    # csr.init_range_dynamic_table()                   # 清空动态元数据表(# 判断T00_RANGE_DYNAMIC是否存在，存在则drop后创建，否则直接创建)
    # csr.create_heredity_total()                      # 获取"遗传总量"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成
    # csr.create_interior_heredity_proportion()        # 获取"内部遗传比例"元数据(即时性)(依赖配置表t00_set)，依赖上期期号，需每次重新生成

    # csr.data_checkout()                              # 校验 T00_DATA_ANALYZE_INSIDE 表与备份表中的数据前后是否一致

    # csr.create_exclude_rule("2014032")               # 创建排除规则，结果装入 T03_RANGE_MIDDLE + T03_RANGE_MIDDLE_DETAIL 两张表
    # csr.create_exclude_config_for_result("2014032")  # 根据排除规则生成设定值域，为排除计算提供配置，结果装入 T03_RANGE_RESULT 一张表

    # csr.xxx("1,2")
    csr.yyy()

    # csr.test_set()
    csr.finish()
