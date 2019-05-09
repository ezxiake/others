# coding=utf8
import configparser


def get_conf(section, option):

    filename = "./../../config/log.ini"
    conf = configparser.ConfigParser()
    conf.read(filename)  # 文件路径
    return conf.get(section, option)
