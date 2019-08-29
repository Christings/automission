# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import MySQLdb
import time
import urllib
import base64
import subprocess
import json

import logging

logger = logging.getLogger("django.request")


def test_cookie(request):
    login_url = "https://login.sogou-inc.com/?appid=1138&sso_redirect=http://automission.web.tc.ted/test_cookie&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except:
        pass
    if ('uid' not in request.COOKIES and ptoken is ""):
        print "no login and not login"
        return HttpResponseRedirect(login_url)
    if (ptoken != ""):
        message = urllib.unquote(ptoken)
        child = subprocess.Popen(['/bin/php', '/search/odin/django/automission/autoQPS/rsa_decode.php', message], shell = False, stdout = subprocess.PIPE)
        child.wait()
        user = child.stdout.read().decode('utf-8')
        try:
            json_data = json.loads(user)
            uid = json_data['uid']
            login_time_stamp = int(json_data['ts'])/1000#s
            now_time = time.time()
            print "login time is %d" % login_time_stamp
            response = HttpResponse(uid)
            response.set_cookie("uid", uid)
        except:
            response = None
    elif ('uid' in request.COOKIES):
        try:
            uid = request.COOKIES['uid']
            response = HttpResponse(uid)
        except:
            response = None
    if (response == None):
        return HttpResponseRedirect(login_url)
    return response
# Create your views here.

def home(request):
    login_url = "https://login.sogou-inc.com/?appid=1138&sso_redirect=http://automission.web.tc.ted/&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except:
        pass
    if ('uid' not in request.COOKIES and ptoken is ""):
        print "no login and not login"
        return HttpResponseRedirect(login_url)
    if (ptoken != ""):#login request callback
        message = urllib.unquote(ptoken)
        child = subprocess.Popen(['/bin/php', '/search/odin/django/automission/autoQPS/rsa_decode.php', message], shell = False, stdout = subprocess.PIPE)
        child.wait()
        user = child.stdout.read().decode('utf-8')
        try:
            json_data = json.loads(user)
            uid = json_data['uid']
            login_time = int(json_data['ts'])/1000 #s
        except:
            uid = ""
            login_time = 0
        now_time = time.time()
        if (uid != "" and now_time - login_time < 60):
            response = render(request, 'home.html', {'uid': uid})
            if ('uid' not in request.COOKIES):
                response.set_cookie("uid", uid)
        else:
            print "maybe uid[%s] is empty or now_time[%d] - login_time[%d] >= 60" % (uid, now_time, login_time)
            response = None
    elif ('uid' in request.COOKIES):#already login
        try:
            uid = request.COOKIES['uid']
        except:
            print "should be login, but not login"
            uid = ""
        if (uid != ""):
            response = render(request, 'home.html', {'uid': uid})
        else:
            response = None
    if (response == None):
        print "response is none"
        return HttpResponseRedirect(login_url)
    return response


def index(request):
    login_url = "https://login.sogou-inc.com/?appid=1138&sso_redirect=http://automission.web.tc.ted/&targetUrl="
    ptoken = ""
    try:
        ptoken = request.GET['ptoken']
    except:
        pass
    if ('uid' not in request.COOKIES and ptoken is ""):
        print "no login and not login"
        return HttpResponseRedirect(login_url)
    if (ptoken != ""):#login request callback
        message = urllib.unquote(ptoken)
        child = subprocess.Popen(['/bin/php', '/search/odin/django/automission/autoQPS/rsa_decode.php', message], shell = False, stdout = subprocess.PIPE)
        child.wait()
        user = child.stdout.read().decode('utf-8')
        try:
            json_data = json.loads(user)
            uid = json_data['uid']
            login_time = int(json_data['ts'])/1000 #s
        except:
            uid = ""
            login_time = 0
        now_time = time.time()
        if (uid != "" and now_time - login_time < 60):
            response = render(request, 'autoQPS/index.html', {'uid': uid})
            if ('uid' not in request.COOKIES):
                response.set_cookie("uid", uid)
        else:
            print "maybe uid[%s] is empty or now_time[%d] - login_time[%d] >= 60" % (uid, now_time, login_time)
            response = None
    elif ('uid' in request.COOKIES):#already login
        try:
            uid = request.COOKIES['uid']
        except:
            print "should be login, but not login"
            uid = ""
        if (uid != ""):
            response = render(request, 'autoQPS/index.html', {'uid': uid})
        else:
            response = None
    if (response == None):
        print "response is none"
        return HttpResponseRedirect(login_url)
    return response

def statistic(request):
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT start_time, user, testsvn, test_qps, id FROM AutoQPS WHERE querydata='' order by start_time"
    cursor.execute(sql)
    data = cursor.fetchall()
    point_list = []
    k = 1
    for item in data:
        test_qps = item[3]
        start_time = str(item[0])
        user = item[1]
        testsvn = item[2]
        task_id = item[4]

        if (test_qps == None or test_qps == ''):
            continue
        try:
            qps = test_qps.split('=')[2].split('\n')[0]
        except:
            print "error:" + test_qps
            continue;
        message = "date: %s\nuser:%s\nsvn:%s\n" % (start_time, user, testsvn)
        point_list.append({'qps': qps, 'user': user, 'id': str(k), 'start_time': start_time, 'testsvn': testsvn, 'task_id': task_id})
        k += 1
    i_list = []
    for i in range(len(point_list)):
        i_list.append(i+1)
    return render(request, 'autoQPS/statistic.html', {'point_list': point_list, 'i_list': i_list})
def online(request):
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT test_time, testsvn, data_time,dump_time,test_qps FROM OnlineQps order by id"
    cursor.execute(sql)
    data = cursor.fetchall()
    point_list = []
    k = 1
    for item in data:
        test_time = item[0]
        testsvn = item[1]
        data_time = item[2]
        dump_time = item[3]
        test_qps = item[4]

        #message = "date: %s\nuser:%s\nsvn:%s\n" % (start_time, user, testsvn)
        point_list.append({'test_time': test_time, 'testsvn': testsvn, 'data_time': data_time, 'dump_time': dump_time, 'test_qps': test_qps})
        k += 1
    i_list = []
    for i in range(len(point_list)):
        i_list.append(i+1)
    return render(request, 'autoQPS/online.html', {'point_list': point_list, 'i_list': i_list})

def logout(request):
    response = HttpResponseRedirect('https://login.sogou-inc.com/logout.jsp?appid=1138&sso_redirect=http://automission.web.tc.ted&targetUrl=')
    if ('uid' in request.COOKIES):
        response.delete_cookie("uid")
    return response

def task_queue(request):
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    item_on_page = 15
    task_list_t = get_queue()
    total = len(task_list_t)
    total_page = total/item_on_page + 1
    if (total % item_on_page == 0):
        total_page -= 1
    if (page > total_page):
        page = total_page
    task_list = []
    begin = (page-1)*item_on_page
    end = page*item_on_page
    if (end > total):
        end = total
    for item in task_list_t[begin:end]:
        s_time = ""
        run_stat = ""
        if (item[0] != None):
            c_time = str(item[0])
        if (item[3] != None):
            s_time = str(item[3])
        testitem = 0
        if (item[5] != None):
            try:
                testitem = int(item[5])
            except:
                pass
        test_item = ""
        if (testitem/100 == 1):
            test_item = "Qps"
            item_qps = 1
            testitem %= 100
        if (testitem/10 == 1):
            if (len(test_item) != 0):
                test_item += ", "
            item_diff = 1
            test_item += "Diff"
            testitem %= 10
        if (testitem == 1):
            if (len(test_item) != 0):
                test_item += ", "
            item_cost = 1
            test_item += "Cost"
        if (test_item == ""):
            test_item = "Null"
        remarks = ''
        if (item[6] != None):
            remarks = str(item[6])

        #logger.debug("queryqps_remarks_read: %s" %remarks)
        
        task_list.append({'create_time': c_time, 'user': item[1], 'status': item[2], 'start_time': s_time, 'task_id': str(item[4]), 'test_item':test_item, 'remarks': remarks})
    page_list = []
    print "total page: %d" % total_page
    for i in range(total_page):
        page_list.append(i+1)
    try:
        uid = request.COOKIES['uid']
    except:
        uid = ''
    return render(request, 'autoQPS/task_queue.html', {'task_list': task_list, 'page_list': page_list, 'page': page, 'uid': uid})

def get_now_time():
    timeArray = time.localtime()
    return  time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def str_dos2unix(input):
    return input.replace('\r\n', '\n').replace(' ', '')

def str_dos2unix_space(input):
    return input.replace('\r\n', '\n')

def re_add(request):
    login_url = "https://login.sogou-inc.com/?appid=1138&sso_redirect=http://automission.web.tc.ted/&targetUrl="
    mission_id = int(request.POST['mission_id'])

    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT create_time, user, testitem, testsvn, basesvn, newdatapath, querydata, force_update_svn, force_update_newdisk FROM AutoQPS WHERE id=%d" % mission_id
    cursor.execute(sql)
    data = cursor.fetchone()
    (create_time, user, testitem_, testsvn, basesvn, newdatapath, querydata, force_update_svn, force_update_newdisk) = data

    try:
        user = request.COOKIES['uid']
    except:
        return HttpResponseRedirect(login_url)
    testitem = 0
    try:
        qps = str_dos2unix(request.POST['qps'])
        testitem += int(qps)*100
    except:
        pass
    try:
        diff = str_dos2unix(request.POST['diff'])
        testitem += int(diff)*10
    except:
        pass
    try:
        cost = str_dos2unix(request.POST['cost'])
        testitem += int(cost)*1
    except:
        pass
    test_env_update = 0
    base_env_update = 0
    newdisk_update = 0
    try:
        test_env_update = int(request.POST['test_env_update'])
    except:
        pass
    try:
        base_env_update = int(request.POST['base_env_update'])
    except:
        pass
    try:
        newdisk_update = int(request.POST['newdisk_update'])
    except:
        pass
   
    remarks = str_dos2unix_space(request.POST['remarks'])
 
    sql = "INSERT INTO AutoQPS (create_time, user, testitem, testsvn, basesvn, newdatapath, querydata, force_update_svn, force_update_svn_base, force_update_newdisk, remarks) VALUES('%s', '%s', %d, '%s', '%s', '%s', '%s', '%d' ,'%d', '%d', '%s')" %(get_now_time(), user, testitem, testsvn, basesvn, newdatapath, querydata, test_env_update, base_env_update, newdisk_update, remarks)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()
        return HttpResponse("Db Error<br><b>Maybe Chinese charactor</b><br>" + str(testitem)+ '<br>' + user +'<br>' + test_svn + '<br>' + base_svn +'<br>' + newdata +'<br>' + newdisk + '<br>')
    db.close()
    return HttpResponseRedirect('/task_queue')

def add(request):
    login_url = "https://login.sogou-inc.com/?appid=1138&sso_redirect=http://automission.web.tc.ted/&targetUrl="
    testitem = 0
    try:
        qps = str_dos2unix(request.POST['qps'])
        testitem += int(qps)*100
    except:
        pass
    try:
        diff = str_dos2unix(request.POST['diff'])
        testitem += int(diff)*10
    except:
        pass
    try:
        cost = str_dos2unix(request.POST['cost'])
        testitem += int(cost)*1
    except:
        pass
    try:
        user = request.COOKIES['uid']
    except:
        return HttpResponseRedirect(login_url)
    test_svn = str_dos2unix(request.POST['test_svn'])
    base_svn = str_dos2unix(request.POST['base_svn'])
    newdata = str_dos2unix(request.POST['newdata'])
    newdisk = str_dos2unix(request.POST['newdisk'])
    test_env_update = '0'
    base_env_update = '0'
    newdisk_update = '0'
    try:
        test_env_update = str_dos2unix(request.POST['test_env_update'])
    except:
        pass
    try:
        base_env_update = str_dos2unix(request.POST['base_env_update'])
    except:
        pass
    try:
        newdisk_update = str_dos2unix(request.POST['newdisk_update'])
    except:
        pass
    #return HttpResponse("Db Error<br><b>Maybe Chinese charactor</b><br>" + str(testitem)+ '<br>' + user +'<br>' + test_svn + '<br>' + base_svn +'<br>' + newdata +'<br>' + newdisk + '<br>Force Update:' + test_env_update)
   
    remarks = str_dos2unix_space(request.POST['remarks'])
    logger.debug("queryqps_remarks_type: %s" %type(remarks))

    logger.debug("queryqps_remarks: %s" %remarks)
 
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "INSERT INTO AutoQPS (create_time, user, testitem, testsvn, basesvn, newdatapath, querydata, force_update_svn, force_update_svn_base, force_update_newdisk, remarks) VALUES('%s', '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" %(get_now_time(), user, int(testitem), test_svn, base_svn, newdata, newdisk, test_env_update, base_env_update, newdisk_update, remarks)
    logger.debug("queryqps_sql: %s" %sql)

    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()
        return HttpResponse("Db Error<br><b>Maybe Chinese charactor</b><br>" + str(testitem)+ '<br>' + user +'<br>' + test_svn + '<br>' + base_svn +'<br>' + newdata +'<br>' + newdisk + '<br>')
    db.close()
    return HttpResponseRedirect('/task_queue')

def set_cancel(request):
    mission_id = int(request.GET['id'])
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    
    sql = "UPDATE AutoQPS set status = 6 WHERE id = %d" % mission_id
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()
    db.close()
    return

def get_queue():
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT create_time, user, status, start_time, id, testitem, remarks FROM AutoQPS ORDER BY create_time DESC;"
    cursor.execute(sql)
    
    data = cursor.fetchall()
    db.close()
    return data

def task_detail(request):
    task_id = int(request.GET['id'])
    data = get_task_log(task_id)
    if (data == None):
        return HttpResponseRedirect('/task_queue')
    (creat_time, user, status, start_time, errlog, runningIP, test_qps, base_qps, diff, testitem, testsvn, onlinesvn ,newdatapath, querydata, remarks) = data
    
    errlog_list = errlog.decode('utf-8').split('\n')
    c_time = ""
    s_time = ""
    if (creat_time != None):
        c_time = str(creat_time)
    if (start_time != None):
        s_time = str(start_time)
    test_item = ""
    item_qps = 0
    item_diff = 0
    item_cost = 0
    if (testitem/100 == 1):
        test_item = "Qps"
        item_qps = 1
        testitem %= 100
    if (testitem/10 == 1):
        if (len(test_item) != 0):
            test_item += ", "
        item_diff = 1
        test_item += "Diff"
        testitem %= 10
    if (testitem == 1):
        if (len(test_item) != 0):
            test_item += ", "
        item_cost = 1
        test_item += "Cost"
    if (test_item == ""):
        test_item = "Null"
    qps_raise_dict = {'qpstype': 'None', 'value': '0.000'}
    
    if (test_qps != "" and base_qps != ""):
        test_qps_num = -1
        base_qps_num = -1
        try:
            test_qps_num = float(test_qps.split('=')[2].split('\n')[0])
            base_qps_num = float(base_qps.split('=')[2].split('\n')[0])
        except:
            print "Get qps number error"
        print "%f, %f" % (test_qps_num, base_qps_num)
        if (test_qps_num != -1 and base_qps_num != -1):
            qps_raise = (test_qps_num-base_qps_num)/base_qps_num*100
            if (qps_raise > 0.0):
                qps_raise_dict['qpstype'] = 'gt'
                qps_raise_dict['value'] = "%.3f" % qps_raise
            elif (qps_raise < 0.0):
                qps_raise_dict['qpstype'] = 'lt'
                qps_raise_dict['value'] = "%.3f" % (0.0-qps_raise)
            else:
                qps_raise_dict['qpstype'] = 'eq'
                qps_raise_dict['value'] = "%.3f" % qps_raise
    
    test_item_mark = {'item_qps': item_qps, 'item_diff': item_diff, 'item_cost': item_cost}
    try:
        uid = request.COOKIES['uid']
    except:
        uid = ''
    task_detail = {'create_time': c_time, 'start_time': s_time, 'status': status, 'user': user, 'task_id': str(task_id), 'runningIP': runningIP, 'testitem': test_item, 'testsvn': testsvn.split('\n'), 'onlinesvn': onlinesvn.split('\n'), 'newdatapath': newdatapath, 'querydata': querydata, 'remarks': remarks}
    return render(request, 'autoQPS/task_detail.html', {'task_detail': task_detail, 'errlog': errlog_list, 'test_qps': test_qps.split('\n'), 'base_qps': base_qps.split('\n'), 'diff': diff.split('\n'), 'test_item_mark': test_item_mark, 'qps_raise': qps_raise_dict, 'uid': uid})

def get_task_log(id):
    database_host="datatest01.web.sjs.ted"
    database_data="AutoMission"
    database_user="root"
    database_pass=""
    
    db = MySQLdb.connect(database_host,database_user,database_pass,database_data, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT create_time, user, status, start_time, errorlog, runningIP, test_qps, online_qps, diff, testitem, testsvn, basesvn, newdatapath, querydata, remarks FROM AutoQPS WHERE id=%d;" % id
    cursor.execute(sql)
    
    data = cursor.fetchone()
    db.close()
    return data

