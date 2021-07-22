from django.conf import settings
from django.core import serializers
from django.db.models import Q
import string
from django.views.decorators.csrf import csrf_exempt

from app.models import AppDevice, devgroup, devgroup_name,dev_type,mgt_type,attlog,Analysis,Fdjl,Code_name
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render,redirect
from django.core.paginator import Paginator

# Create your views here.
from django.urls import reverse

from nols.settings import BASE_DIR
from rbac.server.init_permission import init_permission

def GLoad_data(request):
    wfd_sum = attlog.objects.filter(log_status='未封堵').count()
    return {'wfd_sum':wfd_sum}

@login_required(login_url='/login/')
def index(request):
    sum = AppDevice.objects.all().count()
    sb_sum=attlog.objects.all().count()
    fd_sum = attlog.objects.filter(log_status='已封堵').count()
    group = devgroup_name.objects.all().count()
    user=request.user

    return render(request,'index.html',locals())


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user:
            auth.login(request,user)
            print(user.roles.all())
            init_permission(user,request)
            return redirect('/index/')
        else:
            error='登陆失败'
            return redirect('/index')
    else:
        return render(request,'login.html')

@login_required(login_url='/login/')
def dev_add(request):
    if  request.method != 'GET':
        dev_all = AppDevice.objects.all()
        return render(request,'device.html',locals())
    else:
        type_all = dev_type.objects.all()
        dev_all = AppDevice.objects.all()
        dev_mgt = mgt_type.objects.all()
        code_all = Code_name.objects.all()
        page = Paginator(dev_all,5)
        page_sum = page.num_pages
        now_page = request.GET.get('page')
        if now_page:
            page_data = page.page(now_page)
        else:
            page_data =page.page(1)
        return render(request,'device.html',locals())

@login_required(login_url='/login/')
def dev_add_dev(request):
    if  request.method != 'GET':
        print(request.POST)
        try:
            dev = AppDevice(
                dev_name=request.POST.get('dev_name'),
                dev_type_id=request.POST.get('dev_type'),
                dev_ip=request.POST.get('dev_ip'),
                dev_user=request.POST.get('dev_user'),
                dev_password=request.POST.get('dev_password'),
                dev_mgt_id = request.POST.get('type_sb'),
                dev_code_id=request.POST.get('js_name'),

            )
            dev.save()
        except Exception:
            return JsonResponse({'result': "fail"})
        return  JsonResponse({'result':"ok"})

@login_required(login_url='/login/')
def dev_add_del(request):
    if request.method != 'GET':
        dev_id= request.POST.getlist("ids[]")
        for i in dev_id:
            dev = AppDevice.objects.get(dev_ip=i)
            dev.delete()
        group1 = devgroup.objects.all()
        group2 = devgroup_name.objects.all()
        group1_list = []
        group2_list = []
        for i in group1:
            group1_list.append(i.group_name_id)
        for i in group2:
            group2_list.append(i.devgroup_name)
        for i in group2_list:
            if i not in group1_list:
                dev = devgroup_name.objects.get(devgroup_name=i)
                dev.delete()

        return JsonResponse({'result': "ok"})


@login_required(login_url='/login/')
@csrf_exempt
def policy(request):
    if request.method == "GET":
        dev = AppDevice.objects.all()
        group_dev = devgroup.objects.all().values("group_name_id").distinct()
        print(group_dev)
        #下拉菜单选择已添加设备
        dev = AppDevice.objects.all()
        test_list = devgroup.objects.all().values()
        name = []
        for i in test_list:
            name.append(i['group_name_id'])
        name = list({}.fromkeys(name).keys())
        group_name = devgroup.objects.all().values().distinct()
        group = {}
        for i in name:

            ip = devgroup.objects.filter(group_name_id = i)

            dev_ip = []
            for x in ip:
                dev_ip.append(x.dev_ip_id)

            group[i] = dev_ip

        print(group)

        return render(request,'policy.html',locals())
    if request.method =="POST":
        ip_list = request.POST.get('ip').strip()
        fdip=ip_list.split('&')
        name = request.POST.get('name')
        dev_ip = devgroup.objects.filter(group_name_id=name)
        device_ip = []
        for i in dev_ip:
            device_ip.append(i.dev_ip_id)
        for i in device_ip:
            ip = i
            user = AppDevice.objects.get(dev_ip=i).dev_user
            password=AppDevice.objects.get(dev_ip=i).dev_password
            code_name= AppDevice.objects.get(dev_ip=i).dev_code_id
            from importlib import import_module
            file_name= code_name.split('.')[0]
            cmd = import_module('cmd.%s'%file_name)
            try:
                getattr(cmd,'%s'%file_name)(ip,user,password,fdip)
            except:
                return JsonResponse({'result': 'error'})
            break
        for i in fdip:
            log = Fdjl(log_ip=i)
            log.save()
        return JsonResponse({'result':'ok'})

















@login_required(login_url='/login/')
def dev_group(request):
    if request.method == "GET":
        #下拉菜单选择已添加设备
        dev = AppDevice.objects.all()


        test_list = devgroup.objects.all().values()
        name = []
        for i in test_list:
            name.append(i['group_name_id'])

        name = list({}.fromkeys(name).keys())



        group_name = devgroup.objects.all().values().distinct()

        group = {}

        for i in name:

            ip = devgroup.objects.filter(group_name_id= i)

            dev_ip = []
            for x in ip:
                dev_ip.append(x.dev_ip_id)

            group[i] = dev_ip

        print(group)








        #设备组内容信息


        return render(request,'device_group.html',locals())
    else:
        print(request.POST)
        group_ip = request.POST.getlist('group[]')
        group_name = request.POST.get('name')
        if len(group_name) == 0 or len(group_ip) ==0:
            result=({'result':'error'})
            return JsonResponse(result)
        elif len(group_name) >0 and len(group_ip) >0:
            # 添加组名到单独的组名表进行外键关联
            devvicegroup_name = devgroup_name(
                devgroup_name=request.POST.get('name'),
            )
            devvicegroup_name.save()
            for i in request.POST.getlist('group[]'):
            #添加关联组IP及组名
                group_dev=devgroup(
                    group_name_id = request.POST.get('name'),
                    dev_ip_id = i,
                )
                group_dev.save()


            result = ({'result': 'ok'})
            return JsonResponse(result)

@login_required(login_url='/login/')
def decode(request):

    if request.method == "POST":
        lx = request.POST.get('lx')
        if lx=='urlcode':
            undata = request.POST.get('undata')
            from .decode import urldecode
            data = ({'result':urldecode(undata)})
            return JsonResponse(data)

        elif lx=='base64':

            undata = request.POST.get('undata')
            from .decode import base64decode
            data = ({'result':base64decode(undata)})
            return JsonResponse(data)
        elif lx=='unicode':
            undata = request.POST.get('undata')
            from .decode import Unicode
            un = Unicode(r'%s'%undata)
            print(un)
            data = ({'result':Unicode(undata)})

            return JsonResponse(data)
        elif lx == 'code16':
            undata = request.POST.get('undata')
            from .decode import str2byte
            data = ({'result': str2byte(undata)})
            return JsonResponse(data)
    else:
        return render(request,'decode.html')

@login_required(login_url='/login/')
def ip_location(request):
    if request.GET.get('ip'):
        from .ip_vote import vote
        ip = request.GET.get('ip').strip(' ')
        print(ip)
        if vote(ip):
            from .ip_localtion import search

            data =({'location':search(ip)})
            return JsonResponse(data)
        else:
            return render(request,'ip_location.html')
    else:

        return render(request, 'ip_location.html')

@login_required(login_url='/login/')
def dev_group_del(request):

    if request.method=="POST":
        print(request.POST)
        name = request.POST.getlist('ids[]')
        print(name)
        for i in name:
            glnameg=devgroup_name.objects.filter(devgroup_name=i)
            glnameg.delete()
        return JsonResponse({'result':'ok'})


    else:
        return render(request,'device_group.html')

@login_required(login_url='/login/')
def device_type(request):

    if request.method=="POST":
        type_sb = request.POST.get('dev_type')
        try:
            dev_type.objects.create(
                d_type=type_sb
            )
            return JsonResponse({"result": "ok"})
        except  :
            return JsonResponse({"error": "类型已存在"})

    else:
        type_all = dev_type.objects.all()
        return render(request,'device_type.html',locals())

@login_required(login_url='/login/')
def type_del(request):
    if request.method=="POST":
        type_lx = request.POST.getlist('ids[]')
        if len(type_lx) > 0:
            for i in type_lx:
                dev_type.objects.filter(d_type=i).delete()

                groupname = devgroup.objects.values('group_name_id').distinct()
                print(groupname)
                name = []
                name1 = []
                for i in groupname:
                    name.append(i['group_name_id'])
                groupname1 = devgroup_name.objects.values('devgroup_name')

                for x in groupname1:
                    name1.append(x['devgroup_name'])

                if len(name) < len(name1):
                    for i in name1:
                        if i not in name:
                            xyname=devgroup_name.objects.filter(devgroup_name=i)
                            xyname.delete()



            return JsonResponse({"result": "ok"})
        else:
            return JsonResponse({"result": "删除失败"})
    else:
        type_all = dev_type.objects.all()
        return render(request,'device_type.html',locals())


def login_out(request):
    if request.method=="GET":
        auth.logout(request)
        return redirect('/login')

@login_required(login_url='/login/')
def policy_group_del(request):
    if request.method=='POST':
        print(request.POST)
        group_name = request.POST.getlist('group')
        print(len(group_name[0]))
        if len(group_name[0])!=0:
            glnameg = devgroup_name.objects.filter(devgroup_name=group_name[0])
            glnameg.delete()
            return JsonResponse({"result": "ok"})
        else:
            return render(request,'policy.html')

@login_required(login_url='/login/')
def dev_mgt(request):
    if request.method=="POST":
        mgt_xx = request.POST.getlist('mgt')

        mgt_type.objects.create(
            type_sb=mgt_xx[0]
        )
        return JsonResponse({"result": "ok"})
    else:
        type_sb = mgt_type.objects.all()


        return render(request,'device_mgt.html',locals())

@login_required(login_url='/login/')
def dev_mgt_del(request):
    if request.method=="POST":
        type_mgt = request.POST.getlist('ids[]')
        if len(type_mgt) > 0:
            for i in type_mgt:
                mgt_type.objects.filter(type_sb=i).delete()
                groupname = devgroup.objects.values('group_name').distinct()
                print(groupname)
                name = []
                name1 = []
                for i in groupname:
                    name.append(i['group_name'])
                groupname1 = devgroup_name.objects.values('devgroup_name')

                for x in groupname1:
                    name1.append(x['devgroup_name'])

                if len(name) < len(name1):
                    for i in name1:
                        if i not in name:
                            xyname = devgroup_name.objects.filter(devgroup_name=i)
                            xyname.delete()

            return JsonResponse({"result": "ok"})

    return None

@login_required(login_url='/login/')
def policy_group_edit(request):
    if request.method=="POST":
        print(request.POST)
        name = request.POST.getlist('name')[0]
        print(name)
        new_ip = request.POST.getlist('ip[]')
        print(new_ip)

        devgroup.objects.filter(group_name_id=name).delete()
        for i in new_ip:
            devgroup.objects.create(
                group_name_id=name,
                dev_ip_id=i
            )

        return render(request,'policy.html')

@login_required(login_url='/login/')
def monitor(request):


    if request.method=="POST":
        name = request.POST.get('name')
        dev = request.POST.get('dev')
        src_area=request.POST.get('src_area')
        srcip = request.POST.get('srcip').strip(' ')
        dstip = request.POST.get('dstip')
        payload = request.POST.get('payload')

        ipct=attlog.objects.filter(log_srcip=srcip)
        print(len(ipct))
        if len(ipct)>0:
            return JsonResponse({"result": "error"})

        if "<" in payload:
            new_payload=payload.replace('<','&lt;')
            new_payload=new_payload.replace('>','&gt;')
            if len(name) >= 1 and len(srcip) >= 1:
                attlog.objects.create(
                    log_name=name,
                    log_dev=dev,
                    log_area=src_area,
                    log_srcip=srcip,
                    log_dstip=dstip,
                    log_payload=new_payload,
                    log_status='未封堵',

                )
                return JsonResponse({"result": "ok"})
            else:
                return JsonResponse({"result": "error"})
        else:
            pass

        if len(name) >= 1 and len(srcip) >=1 :
            attlog.objects.create(
                log_name=name,
                log_dev=dev,
                log_area=src_area,
                log_srcip=srcip,
                log_dstip=dstip,
                log_payload=payload,
                log_status='未封堵',

            )
            return JsonResponse({"result": "ok"})
        else:

            return JsonResponse({"result": "error"})


    else:
        log_att = attlog.objects.order_by('-id')
        page = Paginator(log_att, 10)
        page_id = request.GET.get('page')
        if page_id == None:
            page_data = page.page(1)
            return render(request, 'monitor.html', locals())
        else:
            page_data = page.page(page_id)
            return render(request, 'monitor.html', locals())
        return render(request, 'monitor.html', locals())


@login_required(login_url='/login/')
def monitor_del(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.getlist('id[]')
        print(id)
        if len(id)==0:
            return JsonResponse({"result": "error"})
        else:
            for i in id:
                attlog.objects.filter(id=i).delete()
            return JsonResponse({"result": "ok"})

@login_required(login_url='/login/')
def monitor_search(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.get('cx')
        q = Q(Q(log_name__contains=id)|Q(log_dev__contains=id)|Q(log_area__contains=id)|Q(log_srcip__contains=id)
              |Q(log_dstip__contains=id)|Q(log_status__contains=id))
        res = attlog.objects.filter(q).order_by('-id')
        page =Paginator(res, 10)
        print(page.num_pages)

        data = serializers.serialize('json', queryset=res)
        return HttpResponse(data)

@login_required(login_url='/login/')
def monitor_status(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.getlist('id[]')

        for i in id:
            print(i)
            attlog.objects.filter(id=i).update(
                log_status='已封堵'
            )
        return JsonResponse({"result": "ok"})

@csrf_exempt
@login_required(login_url='/login/')
def monitor_export(request):
    if request.method=="POST":
        import csv,codecs
        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        all = attlog.objects.all()
        writer = csv.writer(response)
        writer.writerow(['事件名称','监测设备', '攻击区域', '源IP','目的IP', '攻击载荷','时间'])
        for i in all:
            writer.writerow([i.log_name, i.log_dev, i.log_area, i.log_srcip,i.log_dstip,i.log_payload,i.log_time])

        return response
    else:
        return JsonResponse({"result": "error"})

@login_required(login_url='/login/')
def monitor_check_cf(request):
    if request.method=="POST":
        ip = request.POST.get('ip',None)
        ipcheck = attlog.objects.filter(log_srcip=ip).count()
        if ipcheck >0:
            return JsonResponse({"result": "error"})
        else:
            return JsonResponse({"result": "ok"})

@login_required(login_url='/login/')
def wxfx(request):
    if request.method=="POST":
        print(request.POST)
        name = request.POST.get('name').strip(' ')
        dev = request.POST.get('dev').strip(' ')
        src_area=request.POST.get('src_area').strip(' ')
        srcip = request.POST.get('srcip').strip(' ')
        dstip = request.POST.get('dstip').strip(' ')
        payload = request.POST.get('payload').strip(' ')
        if "<" in payload:
            new_payload=payload.replace('<','&lt;')
            new_payload=new_payload.replace('>','&gt;')
            if len(name) >= 1 and len(srcip) >=1 :
                Analysis.objects.create(
                    log_name=name,
                    log_dev=dev,
                    log_area=src_area,
                    log_srcip=srcip,
                    log_dstip=dstip,
                    log_payload=new_payload,
                    log_status='待分析',
                )
                return JsonResponse({"result": "ok"})
            else:

                return JsonResponse({"result": "error"})


            return render(request,'Analysis.html')
        else:
            if len(name) >= 1 and len(srcip) >=1 :
                Analysis.objects.create(
                    log_name=name,
                    log_dev=dev,
                    log_area=src_area,
                    log_srcip=srcip,
                    log_dstip=dstip,
                    log_payload=payload,
                    log_status='待分析',
                )
                return JsonResponse({"result": "ok"})
            else:

                return JsonResponse({"result": "error"})
    else:
        log_att = Analysis.objects.order_by('-id')
        page = Paginator(log_att, 10)
        page_id = request.GET.get('page')
        if page_id == None:
            page_data = page.page(1)
            return render(request, 'Analysis.html', locals())
        else:
            page_data = page.page(page_id)
            return render(request, 'Analysis.html', locals())
        return render(request, 'Analysis.html', locals())

@login_required(login_url='/login/')
def wxfx_del(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.getlist('id[]')
        print(id)
        if len(id)==0:
            return JsonResponse({"result": "error"})
        else:
            for i in id:
                Analysis.objects.filter(id=i).delete()
            return JsonResponse({"result": "ok"})

@csrf_exempt
@login_required(login_url='/login/')
def wxfx_export(request):
    if request.method=="POST":
        import csv,codecs
        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        response['Content-Disposition'] = 'attachment; filename="export-wxfx.csv"'
        all = Analysis.objects.all()
        writer = csv.writer(response)
        writer.writerow(['事件名称','监测设备', '攻击区域', '源IP','目的IP', '攻击载荷','时间','分析结果'])
        for i in all:
            writer.writerow([i.log_name, i.log_dev, i.log_area, i.log_srcip,i.log_dstip,i.log_payload,i.log_time,i.log_status])

        return response
    else:
        return JsonResponse({"result": "error"})

    return None

@login_required(login_url='/login/')
def wxfx_status(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.getlist('id[]')
        val = request.POST.get('val')
        fxyj=request.POST.get('fxyj')
        if val == '1':

            for i in id:
                Analysis.objects.filter(id=i).update(
                    log_status='处置封堵',
                    log_fenxi=fxyj,
                )

                data = Analysis.objects.get(id=i)
                name = data.log_name
                dev = data.log_dev
                src_area = data.log_area
                srcip = data.log_srcip
                dstip = data.log_dstip
                payload = data.log_payload

                if len(attlog.objects.filter(log_srcip=srcip))==0:

                    attlog.objects.create(
                        log_name=name,
                        log_dev=dev,
                        log_area=src_area,
                        log_srcip=srcip,
                        log_dstip=dstip,
                        log_payload=payload,
                        log_status='未封堵',
                    )

            return JsonResponse({"result": "ok"})
        elif val == '2':
            for i in id:
                Analysis.objects.filter(id=i).update(
                    log_status='继续观察',
                    log_fenxi=fxyj,

                )

            return JsonResponse({"result": "ok"})

    return None


def fdjl(request):
    log = Fdjl.objects.order_by('-id')
    page = Paginator(log, 10)
    page_id = request.GET.get('page')
    if page_id == None:
        page_data = page.page(1)
        return render(request, 'fdjl.html', locals())
    else:
        page_data = page.page(page_id)
        return render(request, 'fdjl.html', locals())

    return render(request, 'fdjl.html', locals())

@csrf_exempt
@login_required(login_url='/login/')
def fdjl_export(request):
    if request.method=="POST":
        import csv,codecs
        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        response['Content-Disposition'] = 'attachment; filename="export-fdjl.csv"'
        all = Fdjl.objects.all()
        writer = csv.writer(response)
        writer.writerow(['封堵IP','时间'])
        for i in all:
            writer.writerow([i.log_ip,i.log_time])

        return response

@login_required(login_url='/login/')
def fdjl_search(request):
    if request.method=="POST":
        print(request.POST)
        id = request.POST.get('cx')
        q = Q(Q(log_ip__contains=id))
        res = Fdjl.objects.filter(q).order_by('-id')
        page =Paginator(res, 10)
        print(page.num_pages)

        data = serializers.serialize('json', queryset=res)
        return HttpResponse(data)

@login_required(login_url='/login/')
def wxfx_search(request):
    if request.method == "POST":
        print(request.POST)
        id = request.POST.get('cx')
        q = Q(Q(log_srcip__contains=id))
        res = Analysis.objects.filter(q).order_by('-id')
        page = Paginator(res, 10)
        print(page.num_pages)

        data = serializers.serialize('json', queryset=res)
        return HttpResponse(data)

@login_required(login_url='/login/')
def messges(request):
    if request.method=="POST":
        wfd_sum = attlog.objects.filter(log_status='未封堵').count()
        return JsonResponse({'result':wfd_sum})

@login_required(login_url='/login/')
def js_code(request):
    import os
    code_path = BASE_DIR+'/cmd/'
    js_name=Code_name.objects.all()
    if request.method=='POST':
        code = request.POST.get('code')
        name = request.POST.get('name')
        bm_utf8='# -*- coding: GBK -*-\n'
        with open(code_path+name,'a+') as f:
            f.write(bm_utf8)
            f.write(code)
            Code_name.objects.create(
                name=name,
                neirong=code,
            )
        return JsonResponse({'result':'ok'})

    return render(request,'js_code.html',locals())

@login_required(login_url='/login/')
def js_view(request):
    if request.method=='POST':
        js_name = request.POST.get('name')
        neirong=Code_name.objects.filter(name=js_name)
        data = serializers.serialize('json', queryset=neirong)

        return JsonResponse({'result':data})
    else:

        name = request.GET.get('name').strip()
        q = Q(Q(name__contains=name))
        res = Code_name.objects.filter(q)
        data =serializers.serialize('json', queryset=res)
        return JsonResponse({'result': data})



@login_required(login_url='/login/')
def js_del(request):
    if request.method=="POST":
        js_name=request.POST.getlist('name[]')
        for i in js_name:
            dev = Code_name.objects.filter(name=i)
            dev.delete()
            import os
            code_path = BASE_DIR + '/cmd/'+i
            os.remove(code_path)
        group1 = devgroup.objects.all()
        group2 = devgroup_name.objects.all()
        group1_list = []
        group2_list = []
        for i in group1:
            group1_list.append(i.group_name_id)
        for i in group2:
            group2_list.append(i.devgroup_name)
        for i in group2_list:
            if i not in group1_list:
                dev = devgroup_name.objects.get(devgroup_name=i)
                dev.delete()
        return JsonResponse({'result':'ok'})
def test_sad(request):
    data = AppDevice.objects.all()
    data1 =[]
    for i in data:
        zd = {}
        zd['dev_name']=i.dev_name
        zd['dev_type']=i.dev_type_id
        zd['dev_ip']=i.dev_ip
        zd['dev_user']=i.dev_user
        zd['dev_password']=i.dev_password
        zd['dev_mgt']=i.dev_mgt_id
        zd['dev_code']=i.dev_code_id
        zd['dev_time']=i.dev_time
        data1.append(zd)
    print(data1)

    data2 ={
        "total": 800,
        "totalNotFiltered": 800,
        "rows":data1

    }
    return JsonResponse(data2)