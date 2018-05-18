#coding:utf-8

#配置
Settings = {
    "profile": "test",#监控环境，一般test和prod
    "server_dict": {
        "8091": "Loan",
        "8092": "Payment",
        "8093": "User",
        "8094": "Pub"
    },# 需要监控的端口以及对于的服务名
    "getIp_command": "/sbin/ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d '地址:'", #获取本机IP命令
    "getProcess_command": "netstat -lpn|grep java|grep '%s'|egrep '%s'|awk '{print $4}'",#需要IP 和 目標端口
    "from_email": "notice@lixiangpai888.com",
    "alarm_phones": "13148899469,18929335653,18665800014,13480912834,18137666880",
    "alarm_emails": "liaoxudong@dafy.com,hedaiyong@dafy.com,yaoyuping@dafy.com,liyuming@dafy.com,niexiang@dafy.com",
    #发送短信命令
    "sendMsg_commad": "curl -X POST -F 'p=%s' -F 'msg=【理享派】系统异常！所属模块：[%s]，异常信息：%s.' -F 'charSetStr=UTF-8' -F 'pwd=cdaf269a6480cc6f3b63e1065d16bb8e' -F 'username=szsdfkj' http://api.app2e.com/smsBigSend.api.php",
    "pingPong_command": "curl -I -m 10 -o /dev/null -s -w %{http_code} " #心跳命令
}

#用于已发送报警消息后的对应进程缓存，避免重复发太多次报警
Alarm_cache = {
    "dead_process": [],
    "ping_error": []
}