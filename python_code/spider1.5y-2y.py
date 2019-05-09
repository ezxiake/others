# coding=utf-8
import os, win32crypt, sqlite3, time, requests, traceback, cx_Oracle, grequests, io, sys
import random

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from parse import *


class spider:
    ''''''

    def __init__(self):
        self.key_list = []
        self.total_dict = {}
        # self.cookies = {}
        # cookies_dict = {}

        # 导入字符串cookie
        # str_cookies = ''
        # list_cookies = str_cookies.split("; ", str_cookies.count("; "))
        #
        # # 转换为字典型cookie
        # for item in list_cookies:
        #     list_item = item.split("=", item.count("="))
        #     cookies_dict[list_item[0]] = list_item[1]

        # 将字典cookies转为CookieJar类型
        # self.cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
        self.cookies = self.get_cookies()

        # 伪装成火狐浏览器请求
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; rv:35.0) Gecko/20100101 Firefox/35.0',
                        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        'Accept-Encoding':'gzip, deflate',
                        'Connection':'keep-alive',
                        'Cache-Control':'max-age=0',
                        'Host':'www.jiayuan.com',
                        'Referer':'http://search.jiayuan.com/v2/'}

        # self.rs = requests.session()
        # self.rs.cookies = cookies

        self.start = time.clock()

        # self.cx = connect("./jiayuan.db")
        # self.sql = self.cx.cursor()
        self.cx = cx_Oracle.connect('jiayuan/jiayuan@192.168.1.38/orcl')
        self.sql = self.cx.cursor()

    def get_cookies(self):
        conn = sqlite3.connect('C:\\Users\\xiaoke\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies')
        cursor = conn.cursor()

        rst = cursor.execute("SELECT host_key, name, path, value, encrypted_value FROM cookies where host_key = '.jiayuan.com'")
        ret_dict = {}
        for line in rst.fetchall():
            # print(line)
            ret = win32crypt.CryptUnprotectData(line[4], None, None, None, 0)
            ret_dict[line[1]] = ret[1].decode()

        cursor.close()
        conn.close()
        # print(ret_dict)
        return requests.utils.cookiejar_from_dict(ret_dict, cookiejar=None, overwrite=True)

    def execute(self, end_pos):

        # try:

        # 测试使用
        # self.sql.execute('delete from get_id')

        # v_sql_id = 'select id + 1 from  get_id where id < ' + str(end_pos) + ' order by id desc limit 1'
        v_sql_id = 'select id from (select id + 1 as id from get_id_4 order by id desc)  where rownum = 1'
        start_pos = self.sql.execute(v_sql_id).fetchone()[0]
        # start_pos = 150000000  # 1y

        id_list = []
        url_list = []
        while 1 == 1:

            try:

                for count in range(10):
                    if start_pos == end_pos: break
                    id_list.append(str(start_pos))
                    url_list.append('http://www.jiayuan.com/%s' % str(start_pos))
                    start_pos += 1

                v_proxy = self.get_proxy()

                # response = requests.get(get_url)
                # response = requests.get(get_url, cookies=self.cookies, headers=self.headers)
                # response = self.rs.get(get_url, headers=self.headers)
                gg = (grequests.get(url, cookies=self.cookies, headers=self.headers, proxies=self.get_proxy()) for url in url_list)
                # gg = (grequests.get(url, cookies=self.cookies, headers=self.headers) for url in url_list)
                response_dict = dict(zip(id_list, grequests.map(gg)))

                self.parse(response_dict)

                id_list = []
                url_list = []
                if start_pos == end_pos: exit(0)
                # exit(2)
            except AttributeError:
                print("AttributeError: 'NoneType' object has no attribute 'text' and now from " + str(id_list[0]) + " re-start ...")
                self.cx.rollback()
                self.key_list = []
                self.total_dict = {}
                # traceback.print_exc(e)
                start_pos = int(id_list[0])
                id_list = []
                url_list = []
                continue
            # except ValueError:
            #     print("ValueError: the query contains a null character and now from " + str(id_list[0]) + " re-start ...")
            #     self.cx.rollback()
            #     self.key_list = []
            #     self.total_dict = {}
            #     start_pos = int(id_list[0])
            #     id_list = []
            #     url_list = []
            #     continue
            except Exception as e:
                print(self.v_sql)
                traceback.print_exc(e)

            # except Exception as e:
            #     self.cx.rollback()
            #     self.key_list = []
            #     self.total_dict = {}
            #     self.sql.close()
            #     self.cx.close()
            #     traceback.print_exc(e)

            # exit(2)

        # except Exception as e:
        #     self.cx.rollback()
        #     self.key_list = []
        #     self.total_dict = {}
        #     traceback.print_exc(e)
        #     self.execute(id_list[0])
        # finally:
            # self.cx.commit()
            # self.sql.close()
            # self.cx.close()
            # print(" ===== All finish and spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "] =====")

    def parse(self, response_dict):

        for id, response in response_dict.items():

            self.key_list.append('ID')
            self.total_dict['ID'] = id
            # print(response.text)
            check_id = response.text.count("您查找的用户ID有误或不存在")
            check_black = response.text.count("该会员已被加黑")
            check_close1 = response.text.count("征友资料关闭")
            check_close2 = response.text.count("该用户资料已经关闭")
            check_login = response.text.count("登录后可见")
            check_other1 = response.text.count("此用户暂未通过审核")
            check_other2 = response.text.count("正在审核")

            if check_id > 0:
                str_sql = 'insert into get_id_4 values(' + str(id) + ', 0)'
                self.sql.execute(str_sql)
                print("您查找的用户ID有误或不存在 ：" + str(id))
            elif check_black > 0:
                str_sql = 'insert into get_id_4 values(' + str(id) + ', 1)'
                self.sql.execute(str_sql)
                print("该会员已被加黑 ：" + str(id))
            elif check_close1 > 0 or check_close2 > 0 or check_other1 > 0 or check_other2 > 0:
                str_sql = 'insert into get_id_4 values(' + str(id) + ', 2)'
                self.sql.execute(str_sql)
                print("资料关闭或未通过审核 ：" + str(id))
            elif check_login > 0:
                print("需要重新登录")
                self.cookies = self.get_cookies()
                raise AttributeError
                # exit(1)
            else:
                str_sql = 'insert into get_id_4 values(' + str(id) + ', 9)'
                self.sql.execute(str_sql)

                print("------- ：" + str(id))

                self.key_list, self.total_dict = get_nickname(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_last_login_time(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_care(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_charm_value(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_member_sf(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_honesty_level(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_age_marry_from(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_member_info_map(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_mdjlp_status(response, self.key_list, self.total_dict)
                v_self_intro = get_self_intro(response)
                self.key_list, self.total_dict = get_claims(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_habbits(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_economic_power(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_work_study(response, self.key_list, self.total_dict)
                self.key_list, self.total_dict = get_marriage_concept(response, self.key_list, self.total_dict)

                # hash_value = get_care_hash(response)
                # care_page = 'http://fate.jiayuan.com/ajax/get_fate_user.php?hash=' + hash_value
                # rs = requests.get(care_page)
                # pattern1 = re.compile('"num":"(\d+?)"', re.U | re.S)
                # result1 = pattern1.search(rs.text)
                # key_list.append('关注ta')
                # total_dict['关注ta'] = result1.group(1)

                self.v_sql = 'insert into jy_data_4 ('
                for col in self.key_list:
                    self.v_sql += col + ','
                self.v_sql += "自我介绍) values ('"

                for col in self.key_list:
                    self.v_sql += self.total_dict[col] + "', '"
                self.v_sql = self.v_sql[:len(self.v_sql) - 1] + ":self_intro)"

                clob_self_intro = self.sql.var(cx_Oracle.CLOB)
                clob_self_intro.setvalue(0, v_self_intro)
                # print(self.v_sql)
                self.sql.execute(self.v_sql, {"self_intro": clob_self_intro})
                # print(self.key_list)
                # print(self.total_dict)

            self.key_list = []
            self.total_dict = {}
                # if int(self.total_dict['照片数']) > 0:
                #     get_photo(response, self.key_list, self.total_dict, self.cookies)
        self.cx.commit()
        print(" ===== Execute commit and current spend time：[" + "%f s" % (time.clock() - self.start) + " - " + "%f m" % ((time.clock() - self.start) / 60) + " - " + "%f h" % ((time.clock() - self.start) / 3600) + "] =====")

    def get_proxy(self):
        # v_key = random.randint(1, self.sql.execute("select count(*) from proxy").fetchone()[0])
        # print(v_key)

        # v_dict = {}
        # v_num = 1
        # for line in self.sql.execute("select ip from proxy"):
        #     print(line[0])
            # v_dict[v_num] = line[0]
            # v_num += 1

        # print(v_dict)
        # print(v_dict[v_key])

        # v_proxy = {'http': 'http://' + v_dict[v_key], 'https': 'http://' + v_dict[v_key]}
        # print(v_proxy)

        address = self.sql.execute("select ip from proxy where flag = '1'").fetchone()[0]

        return {'http': 'http://' + address, 'https': 'http://' + address}

s = spider()
# s.execute(1000000)
# s.execute(10721906)  # 正常
# s.execute(1000003)
# s.execute(103813120) # 身份证+港澳通行证
# s.execute(37189779)  # 该用户找到意中人,关闭
# s.execute(1000001)   # 该用户找到一种人，text
# s.execute(108223085)   # 离异,有小孩归自己
# s.execute(127147467)   # 有懂你 爱情DNA
# s.execute(164471979)   # ON-LINE
# s.execute(163263189)  # 男的
# s.execute(164441239)  # 无照片无礼物
# s.execute(1000006)  # 有照片会员可见

# s.execute(2856507, 4000000)
# s.execute(4360064, 6000000)
# s.execute(6185984, 8000000)
# s.execute(8235264, 10000000)

s.execute(200000001)
# s.execute(2991698)