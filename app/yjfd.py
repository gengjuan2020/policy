#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#Author: nols

import paramiko,time,re


class yjfd:

    def huasan_ssh(self,ip,user,passwd,blackip):
        # blckip是一个列表
        try:
            transport = paramiko.Transport((ip, 22))
            transport.connect(username=user, password=passwd)
            connect = ('连接%s成功' % ip)
            print(connect.center(50, '*'))
            channel = transport.open_session()
            # 获取一个终端
            channel.get_pty()
            # 激活器
            channel.invoke_shell()
            time.sleep(1)
            channel.send('dis object-group name hw_ip_deny\n')
            result = ''
            while not result.endswith(' '):
                time.sleep(5)
                res = channel.recv(65535).decode()
                result += res
                channel.send(' ')
            #获取number号
            print(result)
            huasan = re.findall('(\d+)\s+network\s+host', result)
            huasan_number = huasan[-1]
            print(huasan_number)
            #发送封堵添加
            channel.send('sys\n')
            time.sleep(0.5)
            channel.send('object-group ip address hw_ip_deny\n')
            time.sleep(0.5)
            for i in blackip:
                huasan_number = str(int(huasan_number)+1)
                channel.send('%s network host address %s\n'%(huasan_number,i))
                time.sleep(0.5)
            # 关闭通道
            channel.close()
            # 关闭链接
            transport.close()
        except:
            print('%s地址连接错误' % ip)
            raise Exception('connect Error ')


    def huawei_ssh(self,ip,user,passwd,blackip):
        #blckip是一个列表
        try:
            transport = paramiko.Transport((ip, 22))
            transport.connect(username=user, password=passwd)
            connect = ('连接%s成功' % ip)
            print(connect.center(50, '*'))
            channel = transport.open_session()
            # 获取一个终端
            channel.get_pty()
            # 激活器
            channel.invoke_shell()
            time.sleep(1)
            channel.send('dis ip address verbose hw_ip_deny item\n')
            result = ''
            while not result.endswith(' '):
                time.sleep(0.5)
                res = channel.recv(65535).decode()
                result += res
                channel.send(' ')
            #获取number号
            print(result)
            huawei = re.findall('address\s+(\d+)\s+', result)
            huawei_number = huawei[-1]
            #发送封堵添加
            channel.send('sys\n')
            time.sleep(0.5)
            channel.send('ip address-set hw_ip_deny\n')
            time.sleep(0.5)
            for i in blackip:
                huawei_number = str(int(huawei_number)+1)
                channel.send('address %s %s mask 32\n'%(huawei_number,i))
                time.sleep(0.5)
            # 关闭通道
            channel.close()
            # 关闭链接
            transport.close()
        except:
            print('%s地址连接错误' % ip)
            raise Exception('connect Error ')

    def trx_ssh(self,ip,user,passwd,blackip):
        # blckip是一个列表
        try:
            transport = paramiko.Transport((ip, 22))
            transport.connect(username=user, password=passwd)
            connect = ('连接%s成功' % ip)
            print(connect.center(50, '*'))
            channel = transport.open_session()
            # 获取一个终端
            channel.get_pty()
            # 激活器
            channel.invoke_shell()
            time.sleep(1)
            channel.send('define host show vsid 0\n')
            result = ''
            while not result.endswith(' '):
                time.sleep(0.5)
                res = channel.recv(65535)
                result += str(res, encoding="gb2312")
                channel.send(' ')
            # 获取number号
            print(result)
            #获取封堵已有列表
            ss = re.findall("hw_ip_deny\s+ipaddr\s+\x27([^\x27]+)", result)
            fdlist = ss[0].replace('\n', '').replace('\r', '').strip(' ')
            print(fdlist)
            # 发送封堵添加
            for i in blackip:
                ip_list = fdlist + ' ' + i
                channel.send("define host modify name hw_ip_deny ipaddr '%s' macaddr 00:00:00:00:00:00 vsid 0\n" % ip_list)
                time.sleep(1)
            # 关闭通道
            channel.close()
            # 关闭链接
            transport.close()
        except:
            print('%s地址连接错误' % ip)
            raise Exception('connect Error ')


