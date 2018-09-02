#!/usr/bin/python
# -*-coding:utf-8 -*-
from yunapp import app, result, connection, request, tool, config
from yunapp.result import *
import urllib, urllib2
import geoip2.database
import json
from flask import jsonify
from datetime import datetime
import whois
from flask import make_response
'''
获取ip和ips
{

}
'''
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

@app.route('/app/getip', methods=['GET', 'POST'])
def getIp():
    if request.method == 'POST':
        data = None
        ip = None
        try:
           data = request.get_json()
        except Exception as e:
            pass
        try:
            if data:
                for key in data:
                    if key == 'ip':
                        ip = data['ip']
            if ip == None:
                ip = request.remote_addr
            rsl = kuaidi(ip)
            rsdic = json.loads(rsl)
            try:
                response = reader.city(rsdic['data']['ip'])
                rsdic['data']['latitude']= response.location.latitude
                rsdic['data']['longitude'] = response.location.longitude
            except Exception as e:
                pass

            try:
                if rsdic['data']['ip']:
                    jilv = connection.WanNeng.find_one({'appkey': '5b2856b964fec03d28ba674a', 'w2': rsdic['data']['ip']},{'del': 0})
                    if not jilv:
                        wn = connection.WanNeng()
                        wn.w1 = u'ipjilv'
                        wn.w2 = rsdic['data']['ip']
                        wn.appkey = u'5b2856b964fec03d28ba674a'
                        wn.save()
                    else:
                        jilv.date = datetime.now()
                        jilv.save()
            except Exception as e:
                pass
            return jsonify(rsdic)
        except Exception as e:
            return MyExceptionWithResult(param.CHECK_FAILURE,unicode(e)).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST


def kuaidi(ip):
    url = 'http://ip.taobao.com/service/getIpInfo2.php?ip=' + ip
    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req,timeout=1)
    res = res.read()
    return res

# 查询whios
@app.route('/app/getwhios', methods=['GET', 'POST'])
def getwhios():
    if request.method == 'POST':
        data = None
        ip = None
        try:
           data = request.get_json()
        except Exception as e:
            pass
        try:
            if data:
                for key in data:
                    if key == 'domain':
                        ip = data['domain']
            if not ip:
                return  MyException(param.CHECK_FAILURE).toJson()
            obj = whois.whois(str(ip))
            # rsdic = json.loads(obj)
            try:
                if data['domain']:
                    jilv = connection.WanNeng.find_one({'appkey': '5b2856b964fec03d28ba674a', 'w2': data['ip']},{'del': 0})
                    if not jilv:
                        wn = connection.WanNeng()
                        wn.w1 = u'whoisjilv'
                        wn.w2 = data['domain']
                        wn.appkey = u'5b2856b964fec03d28ba674a'
                        wn.save()
                    else:
                        jilv.date = datetime.now()
                        jilv.save()
            except Exception as e:
                pass
            return MyResult(obj).toJson()
        except Exception as e:
            return MyExceptionWithResult(param.CHECK_FAILURE,unicode(e)).toJson()

    if request.method == 'GET':
        return param.PLEASE_USE_POST