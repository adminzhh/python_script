#!/usr/bin/env python3

import requests
import sys
import os
import json
import logging

# 日志格式构造
logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
                datefmt = '%a, %d %b %Y %H:%M:%S',
                filename = os.path.join('/tmp','weixin_python.log'),
                filemode = 'a')
# 企业ID
corpid='ww76b67c7a9*******'

# 应用秘钥
appsecret='mrZiPnSDsod_DPVcF-TTyCtz6BCw************'

# 应用id
agentid='1000003'

# 获取身份令牌，用于和微信通信的认证
# 参考企业微信API文档https://developer.work.weixin.qq.com/document/path/90487
token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid +'&corpsecret=' + appsecret
req=requests.get(token_url)
accesstoken=req.json()['access_token']
msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken

# 构造消息体
#touser=sys.argv[1]
toparty=sys.argv[1]
subject=sys.argv[2]

# 发送微信消息的数据格式
message=sys.argv[2] + "\n\n" +sys.argv[3]

params={
        #"touser": touser,
        "toparty": toparty,
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": message
            },
    "safe":0
    }

# 最终发请求
req=requests.post(msgsend_url, data=json.dumps(params))
# 调试请求发送结果
print(req.content)
# 记录日志
logging.info('sendto:' + toparty + ';;subject:' + subject + ';;message:' + message)


# 创建媒介类型脚本参数如下：
# {ALERT.SENDTO}
# {ALERT.SUBJECT}
# {ALERT.MESSAGE}

# 消息模板如下：
# 消息类型：问题
# 主题：服务器{HOSTNAME1}，发生故障{TRIGGER.STATUS}: {TRIGGER.NAME}！
# 消息：=======发生了如下的报警问题================
# 告警主机：{HOSTNAME1} 
# 告警主机IP：{HOST.IP}
# 告警时间：{EVENT.DATE}-{EVENT.TIME}
# 告警等级：{TRIGGER.SEVERITY}
# 告警信息：{TRIGGER.NAME}
# 告警项目：{TRIGGER.KEY1}
# 问题详情：{ITEM.NAME} : {ITEM.VALUE}
# 当前状态：{TRIGGER.STATUS} : {ITEM.VALUE1}
# 事件ID：{EVENT.ID}　　
# ===========================================

# 消息类型：问题恢复
# 主题： 服务器{HOSTNAME1}，故障已恢复{TRIGGER.STATUS}: {TRIGGER.NAME}已恢复!
# 消息：=================恢复信息===============
# 告警主机：{HOSTNAME1}
# 告警主机IP：{HOST.IP}
# 告警时间：{EVENT.DATE}-{EVENT.TIME}
# 告警等级：{TRIGGER.SEVERITY}
# 告警信息：{TRIGGER.NAME}
# 告警项目：{TRIGGER.KEY1}
# 问题详情：{ITEM.NAME} : {ITEM.VALUE}
# 当前状态：{TRIGGER.STATUS} : {ITEM.VALUE1}
# 事件ID：{EVENT.ID}
# =========================================


# 最后在zabbixui界面里添加媒介，脚本执行，再给用户添加报警媒介，再改触发器动作添加定义的企业微信报警
# 把脚本发到zabbix-server的/usr/lib/zabbix/alertscripts目录里，因为主配置文件有定义，必须把脚本放在这
# 最后就是特别要注意权限的问题，chown zabbix.zabbix weixin.sh 再把脚本所关联的日志也设置为zabbix用户权限
