#coding:utf-8
import os
import time
import send_email
from config import Alarm_cache
from config import Settings


#监控逻辑
def monitor():
    #获取本机IP
    localIp = os.popen(Settings["getIp_command"]).read().strip()
    print '本机IP：',localIp
    #查找目标进程
    monitor_ports = '|'.join(Settings["server_dict"].keys())
    print '需要监控的端口：',monitor_ports
    #循环检查
    p_command = Settings["getProcess_command"] % (localIp,monitor_ports)
    # print '查找目标进程命令：',p_command
    services = []
    # 拼接校验url
    for port in Settings["server_dict"].keys():
        services.append(localIp + ':' +port + '\n')
    # print '期望存在服务：',services
    while True:
        host_ports = os.popen(p_command).readlines()
        print '找到进程：',host_ports
        # 如果目标服务数量已不足期望，检查是哪个服务挂了
        if len(host_ports) < len(Settings["server_dict"].keys()):
            # 获取期望存在服务与实际存在服务之间的差集
            diffs = list(set(services).difference(set(host_ports)))
            # 发送告警短信与邮件
            for diff in diffs:
                # 替换发短信命令的占位符
                module_name = Settings['profile'] + '-' + Settings["server_dict"][diff.strip().split(':')[1]]
                command = Settings["sendMsg_commad"] % (Settings["alarm_phones"],module_name,'进程已终止')
                if diff not in Alarm_cache["dead_process"]:
                    print diff.strip(),'服务挂了,发送短信提醒'
                    #发短信
                    os.system(command)
                    #发邮件
                    send_email.send("【"+module_name +"】异常","进程已终止，赶快修复")
                    Alarm_cache["dead_process"].append(diff) #加入缓存 避免大量重复报警

        else:
            print '进程没挂，继续检查心跳'
            Alarm_cache['dead_process'] = []
        # 给服务发送心跳
        for host_port in host_ports:
            host_port = host_port.strip()
            ping_url = "http://"+host_port+"/api/ping"
            command = Settings["pingPong_command"] + ping_url
            http_status = os.popen(command).read()
            print 'ping:',ping_url,'状态码:',http_status
            if http_status != '200':
                if diff not in Alarm_cache["ping_error"]:
                    print '心跳检查异常，发送报警短信:',Settings["alarm_phones"]
                    module_name = Settings['profile'] + '-' +Settings["server_dict"][host_port.strip().split(':')[1]]
                    #发短信
                    os.system(Settings["sendMsg_commad"] % (Settings["alarm_phones"],module_name,'心跳不通,服务可能是挂了'))
                    #发邮件
                    send_email.send("【"+module_name +"】异常","心跳不通,服务可能是挂了")
                    Alarm_cache["ping_error"].append(diff) #加入缓存 避免大量重复报警
        print '一分钟后再次检查'
        time.sleep(60)

if __name__=='__main__':
    monitor()