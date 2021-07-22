# -*- coding: GBK -*-
import paramiko,time
def qmxc_fw(ip,user,passwd,blackip):
    try:
        transport = paramiko.Transport((ip, 22))
        transport.connect(username=user, password=passwd)
        connect = ('Connect %s Success' % ip)
        print(connect.center(50, '*'))
        channel = transport.open_session()
        channel.get_pty()
        channel.invoke_shell()
        time.sleep(1)
        channel.send('en\n')
        channel.send('config t\n')
        for i in blackip:
            channel.send('blacklist-ip %s timeout 0 \n'%i)
            time.sleep(0.5)
        channel.close()
        transport.close()
    except:
        print('%sconnect Error' % ip)
        raise Exception('connect Error ')