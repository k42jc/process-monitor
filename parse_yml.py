# coding:utf-8

# 专门用于解析config.yml
import yaml


def load():
    __config = open('config.yml')
    return yaml.load(__config)


#加载了的配置
Config = load()
#用于已发送报警进程的缓存
Cache = {
    "dead_process_list": [],
    "ping_error_list": []
}
