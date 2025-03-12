#!/usr/bin/python3
# coding: utf-8
# about zabbix python script
# Author： www.yuchaoit.cn

import requests,json,sys,os,datetime

# 钉钉机器人API
webhook_url='https://oapi.dingtalk.com/robot/send?access_token=9b297f0fd752d837eff1a49a95a86b33*******************************'

# 给脚本参数手机号参数1
user_phone=sys.argv[1]

# 参数2，消息正文
text=sys.argv[2] + "\n\n" + sys.argv[3]

# 构造json数据体
data={
    "msgtype":"text",
    "text":{
        "content":text
    },
    "at":{
        "atMobiles":[user_phone],
        "isAtAll":False
    }
}

# 请求头，表明请求类型是json
headers={"Content-Type":"application/json"}

# 发HTTP请求，POST方式，传入数据与请求头
response=requests.post(url=webhook_url,data=json.dumps(data),headers=headers)
print(response.content)

# 日志目录生成
if os.path.exists("/tmp/dingding.log"):
    with open("/tmp/dingding.log","a+") as f:
        print("该文件以存在，追加写入中")
        if response.json().get("errcode")==0:
            f.write("\n" + str(datetime.datetime.now()) + "    " + str(user_phone) + "    " + "发送成功" + "\n" + str(text) )
        else:
            f.write("\n" + str(datetime.datetime.now()) + "    " + str(user_phone) + "    " + "发送失败" + "\n" + str(text) )
else:
    with open("/tmp/dingding.log","w+") as f:
        print("该日志文件不存在，创建且写入中")
        if response.json().get("errcode")==0:
            f.write("\n" + str(datetime.datetime.now()) + "    " + str(user_phone) + "    " + "发送成功" + "\n" + str(text) )
        else:
            f.write("\n" + str(datetime.datetime.now()) + "    " + str(user_phone) + "    " + "发送失败" + "\n" + str(text) )
            
# 命令行测试：python3 dingding.py  <手机号，可以实现@的效果> "来自zabbix的报警" "快来处理呀""


# 钉钉报警有一定要记得再内容里添加在钉钉里自定义的关键词

# 创建媒介类型脚本参数如下：
# {ALERT.SENDTO}
# {ALERT.SUBJECT}
# {ALERT.MESSAGE}

# 消息模板如下：
# 消息类型：问题
# 主题：服务器{HOSTNAME1}，发生故障{TRIGGER.STATUS}: {TRIGGER.NAME}！
# 消息：=======发生了如下的报警问题================
# 关键字：zabbix
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
# 关键字：zabbix
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
