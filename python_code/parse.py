import os
import re
from time import sleep
import time
from urllib.request import urlopen

import io
import requests
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


""" ID """
def get_id(response, key_list, total_dict):
    pattern = re.compile('<span>ID:(\d+)</span></h4>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        key_list.append('ID')
        total_dict['ID'] = result.group(1).strip()

""" 昵称 + 性别 + 照片数 + 礼物数 """
def get_nickname(response, key_list, total_dict):
    pattern1 = re.compile('<h4>(.+?)<span>ID:\d+</span></h4>', re.S | re.U)
    result1 = pattern1.search(response.text)
    # print(result1.group(1))
    if result1 is not None:
        key_list.append('昵称')
        # result1_sub = re.sub('\W+', '', result1.group(1).strip())
        total_dict['昵称'] = result1.group(1).strip().replace("'", "")
        # total_dict['昵称'] = result1.group(1).strip()
        # pattern5 = re.compile('\w', re.U | re.S)
        # list_nickname = pattern5.findall(result1.group(1).strip())
        # total_dict['昵称'] = "".join(list_nickname)
        # print(total_dict['昵称'])

    pattern2 = re.compile('<h4>(\S+)的择偶要求</h4>', re.S | re.U)
    result2 = pattern2.search(response.text)
    if result2 is not None:
        key_list.append('性别')
        if result2.group(1).strip() == '他':
            total_dict['性别'] = '1'
        else:
            total_dict['性别'] = '0'

    pattern3 = re.compile('的照片\((\d+)\)</a></li>', re.S | re.U)
    result3 = pattern3.search(response.text)
    key_list.append('照片数')
    if result3 is not None:
        total_dict['照片数'] = result3.group(1).strip()
    else:
        total_dict['照片数'] = '0'

    pattern4 = re.compile('的礼物\((\d+)\)</a></li>', re.S | re.U)
    result4 = pattern4.search(response.text)
    key_list.append('礼物数')
    if result4 is not None:
        total_dict['礼物数'] = result4.group(1).strip()
    else:
        total_dict['礼物数'] = '0'

    return key_list, total_dict

""" 最近登录时间 """
def get_last_login_time(response, key_list, total_dict):
    last_login_time = ''
    check_online = response.text.count('<div class="on_line')
    if check_online > 0:
        last_login_time = time.strftime("%Y-%m-%d %H:%M")
    else:
        pattern = re.compile('最近登录时间：([ \S]+)\s+</div>', re.U | re.S)
        result = pattern.search(response.text)
        if result is not None: last_login_time = result.group(1).strip()
    key_list.append('最近登录时间')
    total_dict['最近登录时间'] = last_login_time

    return key_list, total_dict

""" 关注ta (男：他关注的人；女：关注她的人) """
def get_care(response, key_list, total_dict):
    pattern = re.compile('<a href="\S+hash=(\w+?)&show=2" target=[ \S]+?的缘分圈\S*?</a></li>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        key_list.append('关注ta')
        total_dict['关注ta'] = result.group(1).strip()
    return key_list, total_dict

""" 魅力值 """
def get_charm_value(response, key_list, total_dict):
    pattern = re.compile('<h6>(\d+)</h6>\s*<p>魅力值</p>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        key_list.append('魅力值')
        total_dict['魅力值'] = result.group(1).strip()

    return key_list, total_dict

""" 会员身份 """
def get_member_sf(response, key_list, total_dict):
    pattern = re.compile('<span class="member_dj">(.*?)</span>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        member_dj = result.group(1)
        pattern2 = re.compile('title="([\S ]+?)"', re.U | re.S)
        split_member_dj = pattern2.findall(member_dj)
        key_list.append('会员身份')
        if len(split_member_dj) == 0:
            total_dict['会员身份'] = member_dj.strip()
        else:
            total_dict['会员身份'] = split_member_dj[0].strip()

    return key_list, total_dict

""" 诚信等级 + 认证 """
def get_honesty_level(response, key_list, total_dict):
    honesty_level = response.text.count('src="http://images.jiayuan.com/w4/profile/i/star_icon.gif"')
    key_list.append('诚信等级')
    total_dict['诚信等级'] = str(honesty_level)

    identification_list = []
    pattern = re.compile('<span class="member_ico fn-clear">(.*?)</span>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        tgt_result = result.group(1)

        if tgt_result.count('member_ico10') > 0: identification_list.append('手机')
        if tgt_result.count('member_ico17') == 0:
            # identification_list.append('---------------截取')
            pattern1 = re.compile('<a title="([ \S]+)" href="http://www.jiayuan.com/usercp/approve/identity.php"', re.U | re.S)
            result1 = pattern1.search(tgt_result)
            if result1 is not None:
                tgt_result1 = result1.group(1)
                for var in tgt_result1.split('&nbsp;', tgt_result.count('&nbsp;')):
                    if var != '': identification_list.append(var)
        if tgt_result.count('member_ico11') > 0: identification_list.append('邮箱')
        if tgt_result.count('member_ico13') > 0: identification_list.append('视频')
        if tgt_result.count('member_ico14') > 0: identification_list.append('学历')
        if tgt_result.count('member_ico12') > 0: identification_list.append('财产')
        if tgt_result.count('member_ico16') > 0: identification_list.append('芝麻信用')
        if tgt_result.count('member_ico23') == 0: identification_list.append('离婚证')

        key_list.append('认证')
        total_dict['认证'] = str(identification_list).replace("[", "").replace("]", "").replace("'", '').replace(', ', '+')

    return key_list, total_dict

""" 年龄 + 婚姻状态 + 来自 """
def get_age_marry_from(response, key_list, total_dict):
    pattern = re.compile('<h6 class="member_name">(.*?)</h6>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        age_marry_from = result.group(0)
        # print(age_marry_from)
        pattern2 = re.compile('<h6 class="member_name">([ \S]+)来自', re.U | re.S)
        split_age_marry = pattern2.search(age_marry_from)
        if split_age_marry is not None:
            age_marry = split_age_marry.group(1).replace('，', ' ').strip().split(" ", 1)
            key_list.append('年龄')
            total_dict['年龄'] = age_marry[0].replace('岁', '')
            key_list.append('婚姻状态')
            total_dict['婚姻状态'] = age_marry[1]

        pattern3 = re.compile('target="_blank">([ \S]*?)</a>', re.U | re.S)
        split_from = pattern3.findall(age_marry_from)
        if len(split_from) != 0:
            key_list.append('来自')
            v_from = str(split_from).replace('[', '').replace(']', '').replace("'", "").replace(' ','')
            if v_from == ',':
                total_dict['来自'] = ''
            else:
                total_dict['来自'] = v_from

    return key_list, total_dict

""" 学历 + 身高 + 体重 + 星座 + 民族 + 属相 + 血型 """
def get_member_info_map(response, key_list, total_dict):
    pattern = re.compile('<ul class="member_info_list fn-clear">(.*?)</ul>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        member_info_list = result.group(1)
        pattern2 = re.compile('<div class="fl f_gray_999">(\w+)：</div>\s*<div class="fl pr">\s*<em[ ]*>(.*?)</em>', re.S | re.U)
        result = pattern2.findall(member_info_list)
        for item in result:
            key, val = item
            if key in ['购车', '月薪', '住房']:
                continue
            else:
                key_list.append(key)
                total_dict[key] = val.strip()

    return key_list, total_dict

""" 征友状态 """
def get_mdjlp_status(response, key_list, total_dict):
    pattern = re.compile('我的征友状态：(\S+)</p>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        mdjlp_status = result.group(1)
        key_list.append('征友状态')
        total_dict['征友状态'] = mdjlp_status

    return key_list, total_dict

""" 自我介绍 """
def get_self_intro(response):
    pattern = re.compile('<div class="js_text">(.*?)</div>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        # key_list.append('自我介绍')
        # result.group(1).strip().replace('\n', ' ').replace("'", "").replace('\u3000', '').replace("<br />", "").replace("%", "").replace("?", "").replace(" ", "").replace('\u0000', '').replace("´", "`")
        # result_sub = re.sub('\W+', ' ', result.group(1).replace('\n', ' ').replace("'", "").replace('\u3000', '').replace("<br />", "").replace("%", "").replace("?", "").replace(" ", "").replace('\u0000', '').strip())
        result_sub = result.group(1).replace("'", "").replace('\u3000', '').replace("<br />", "").replace("%", "").replace("?", "").replace('\u0000', '').strip()
        # total_dict['自我介绍'] = result_sub
    else:
        raise AttributeError
        # result_sub = ""
    return result_sub

""" 兴趣爱好 """
# def get_hobbies(response, key_list, total_dict):
#     pattern = re.compile('<span\s*title="(\w+)"></span>(.*?)</li>', re.S | re.U)
#     result = pattern.findall(response.text)
#     for item in result:
#         catagory, specific = item
#         if self.hobbies.has_key(catagory.strip()):
#             self.hobbies[catagory.strip()].append(specific.strip())
#         else:
#             self.hobbies[catagory.strip()] = []
#             self.hobbies[catagory.strip()].append(specific.strip())

""" 个性标签 """
# def get_labels(response, key_list, total_dict):
#     pattern = re.compile(u'<div\s*class="pag_list_grey_c"\s*id="\d+">(.*?)</div>', re.S | re.U)
#     result = pattern.findall(response.text)
#     for item in result:
#         self.labels.append(item.strip())

""" 择偶要求 [zo年龄, zo身高, zo民族, zo学历, zo相册, zo婚姻状况, zo居住地, zo诚信] """
def get_claims(response, key_list, total_dict):
    pattern = re.compile('<h4>\S+的择偶要求</h4>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        claims = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="[\S]+">([ \S]+)</div>\s*</li>', re.S | re.U)
        claim_list = pattern2.findall(claims)
        for item in claim_list:
            key, val = item
            # claims[re.sub('&nbsp;', '', key.strip())] = val.strip()
            key_list.append('zo' + re.sub('&nbsp;', '', key.strip()))
            # print(val.strip())
            total_dict['zo' + re.sub('&nbsp;', '', key.strip())] = val.strip().replace('&nbsp;<font color="#848284">', '').replace('</font>', '')

    return key_list, total_dict

""" 生活方式 [吸烟, 饮酒, 锻炼习惯, 饮食习惯, 逛街购物, 宗教信仰, 作息时间, 交际圈子, 最大消费, 家务, 家务分配, 宠物, 关于宠物] """
def get_habbits(response, key_list, total_dict):
    pattern = re.compile('<h6 class="yh">嗜好习惯</h6>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        habbits = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([\S ]+)：</span>\s*<div class="ifno_r_con"><em[\S ]*?>([\S ]+)</em>', re.S | re.U)
        habbits_list = pattern2.findall(habbits)
        for item in habbits_list:
            key, val = item
            key_list.append(re.sub('&nbsp;', '', key.strip()))
            total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()

    house_keeping_pattern = re.compile('<div class="js_tit yh">家务</div>(.*?)</dl>', re.U | re.S)
    result = house_keeping_pattern.search(response.text)
    if result is not None:
        house_keeping_content = result.group(1)
        pattern = re.compile('<dd class="cur" >(\w+)</dd>', re.U | re.S)
        level = pattern.search(house_keeping_content)
        if level is not None:
            key_list.append('家务')
            total_dict['家务'] = level.group(1)
    pattern = re.compile('家务分配：</span>.*?<em[\S ]*?>(.*?)</em>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        key_list.append('家务分配')
        total_dict['家务分配'] = result.group(1)

    pattern = re.compile(u'<div class="js_tit yh">宠物</div>(.*?)</dl>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        house_keeping_content = result.group(1)
        pattern = re.compile(u'<dd class="cur" >(\w+)</dd>', re.U | re.S)
        level = pattern.search(house_keeping_content)
        if level is not None:
            key_list.append('宠物')
            total_dict['宠物'] = level.group(1)
    pattern = re.compile('关于宠物：</span>.*?<em[\S ]*?>(.*?)</em>', re.S | re.U)
    result = pattern.search(response.text)
    if result is not None:
        key_list.append('关于宠物')
        total_dict['关于宠物'] = result.group(1)

    return key_list, total_dict

""" 经济实力 [月薪, 购房, 购车, 经济观念, 投资理财, 外债贷款] """
def get_economic_power(response, key_list, total_dict):
    pattern = re.compile('<h4>经济实力</h4>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        salary = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="[\S ]*?">([\S ]+)</div>\s*</li>', re.S | re.U)
        salary_list = pattern2.findall(salary)
        for item in salary_list:
            key, val = item
            pattern2 = re.compile('<em[\S ]+?>([\S ]+)</em>', re.S | re.U)
            tmp = pattern2.search(val)
            if tmp is None:
                total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()
            else:
                total_dict[re.sub('&nbsp;', '', key.strip())] = tmp.group(1).strip()

            key_list.append(re.sub('&nbsp;', '', key.strip()))

    return key_list, total_dict

""" 工作学习 [职业职位, 公司行业, 公司类型, 福利待遇, 工作状态, 调动工作可能性, 事业与家庭, 海外工作可能性, 毕业院校, 专业类型, 语言能力] """
def get_work_study(response, key_list, total_dict):
    pattern = re.compile('<h6 class="yh">工作</h6>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        work = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="ifno_r_con"><em[\S ]*?>([ \S]+)</em></div>\s*</li>', re.S | re.U)
        work_list = pattern2.findall(work)
        for item in work_list:
            key, val = item
            key_list.append(re.sub('&nbsp;', '', key.strip()))
            total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()

    pattern = re.compile('<h6 class="yh">学习</h6>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        study = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="[\S ]*?"><em[\S ]*?>([ \S]+)</em></div>\s*</li>', re.S | re.U)
        study_list = pattern2.findall(study)
        for item in study_list:
            key, val = item
            key_list.append(re.sub('&nbsp;', '', key.strip()))
            total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()

    return key_list, total_dict

""" 婚姻观念 [籍贯, 户口, 国籍, 个性待征, 幽默感, 脾气, 对待感情, 是否要小孩, 何时结婚, 是否能接受异地恋, 理想婚姻, 愿与对方父母同住, 家中排行, 父母情况, 兄弟姐妹, 父母经济情况, 父母医保情况, 父母的工作] """
def get_marriage_concept(response, key_list, total_dict):
    pattern = re.compile('<h6 class="yh">关于自己</h6>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        about_self = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="[\S ]*?"><em[\S ]*?>([ \S]+)</em></div>\s*</li>', re.S | re.U)
        about_self_list = pattern2.findall(about_self)
        for item in about_self_list:
            key, val = item
            key_list.append(re.sub('&nbsp;', '', key.strip()))
            total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()

    pattern = re.compile('<h6 class="yh mt5">关于家庭</h6>\s*<ul class="js_list fn-clear">(.*?)</ul>', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        about_family = result.group(1)
        pattern2 = re.compile('<li class="fn-clear">\s*<span>([ \S]+)：</span>\s*<div class="[\S ]*?"><em[\S ]*?>([ \S]+)</em></div>\s*</li>', re.S | re.U)
        about_family_list = pattern2.findall(about_family)
        for item in about_family_list:
            key, val = item
            key_list.append(re.sub('&nbsp;', '', key.strip()))
            total_dict[re.sub('&nbsp;', '', key.strip())] = val.strip()

    return key_list, total_dict

""" 保存照片 """
def get_photo(response, key_list, total_dict, cookies):
    pattern = re.compile('href="(\S+?)" target="_blank">她的照片', re.U | re.S)
    result = pattern.search(response.text)
    if result is not None:
        photo_page = result.group(1)
        response = requests.get(photo_page, cookies=cookies)
        # print(response.text)

        bsObj = BeautifulSoup(response.text)
        girl_list = bsObj.findAll('img')

        path = os.getcwd()
        new_path = os.path.join(path, 'photo\\' + total_dict['ID'])
        if not os.path.isdir(new_path):
            os.mkdir(new_path)

        for girl in girl_list:
            link = girl.get('src')
            if str(link)[-4:] == '.jpg':
                try:
                    content = urlopen(link).read()
                    with open('photo\\' + total_dict['ID'] + '\\' + link[-14:], 'wb') as code:
                        code.write(content)
                except TimeoutError as e:
                    print(e)
