#!/usr/bin/python
#-*- coding=utf-8 -*-

import requests
import sys
import pickle
import os
import logging
import json

class checkin:
    def __init__(self, username, passwd):
        self.username = username
        self.passwd = passwd
        self.cookies = {}
        self.session  = requests.session()
        self.setlog()

    def setlog(self):
        log_format = "[%(asctime)s]: %(levelname)s %(funcName)s(%(lineno)d) %(message)s"
        logging.basicConfig(format=log_format,level=20,stream=sys.stderr)
        
    def rcookies(self):
        basepath = os.path.dirname(os.path.realpath(__file__))
        cookie_file = os.path.join(basepath, "cookies")
        if not os.path.exists(cookie_file):
            return False

        try:
            with open(cookie_file, "rb") as fd:
                self.cookies = pickle.load(fd)
        except Exception as e:
            logging.error(e)
            return False

        return True

    def wcookies(self, cookies):
        basepath = os.path.dirname(os.path.realpath(__file__))
        cookie_file = os.path.join(basepath, "cookies")
        if not cookies:
            return False
        if cookies == self.cookies:
            return True

        logging.debug(str(cookies))
        with open(cookie_file, "wb") as fd:
            pickle.dump(cookies, fd)
            self.cookies = cookies
            pickle.dump
        return True

    def login(self):
        url = "http://17wo.cn/Login!process.action"
        data = {
            "backurl":"",
            "backurl2": "",
            "chk": "",
            "chkType": "on",
            "loginType": 0,
            "mobile": self.username, 
            "password": self.passwd
        }
        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }
        ret = self.session.post(url=url, data=data, cookies=self.cookies, headers=headers)
        logging.debug(ret)
        logging.debug(ret.cookies)
        logging.debug(ret.headers)
        newcookies = dict(ret.cookies)
        if newcookies:
            self.wcookies(newcookies)

        if ret.text.find("登录") != -1:
            return False
        return True

    def checkin(self):
        if not self.rcookies():
            self.login()
        url = "http://17wo.cn/SignIn!checkin.action?checkIn=true"
        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }

        if not "JSESSIONID" in self.cookies:
            self.login()
        try:
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
        except Exception as e:
            logging.error(e)

        ret = self.session.get(url=url, cookies=self.cookies)
        logging.debug(ret)
        ret_dict = json.loads(ret.text)
        logging.info(ret_dict["message"])

        if not ret_dict["success"] and ret_dict["message"].find("登录") != -1:
            self.login()
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
            ret = self.session.get(url, cookies=self.cookies)
            logging.info(ret.text)
            ret_dict = json.loads(ret.text)
            logging.info(ret_dict["message"])
            if not ret_dict["success"] and ret_dict["message"].find("登录") != -1:
                return False

    def redpocket(self): 
        if not self.rcookies():
            self.login()
        url = "http://17wo.cn/FlowRedPacket!LuckDraw.action?pageName="
        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }
        data = {
            "pageName": ""        
        }

        if not "JSESSIONID" in self.cookies:
            self.login()
        try:
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
        except Exception as e:
            logging.error(e)

        ret = self.session.get(url=url, cookies=self.cookies, data=data)
        logging.debug(ret)
        logging.debug(ret.text)
        ret_dict = json.loads(ret.text)
        if not "activityId" in ret_dict["data"]:
            self.login()
            ret = self.session.get(url=url, cookies=self.cookies, data=data)
            logging.debug(ret)
            logging.debug(ret.text)
            ret_dict = json.loads(ret.text)

        try:
            errmsg = ret_dict["data"]["message"]["errMsg"]
            if errmsg:
                logging.info(errmsg)
        except Exception as e:
            pass

        try:
            infomsg = ret_dict["data"]["message"]["info"]
            if infomsg:
                logging.info(infomsg)
        except Exception as e:
            pass

    def memberday(self):
        if not self.rcookies():
            self.login()
        url = "http://wap.17wo.cn/MemberDay!draw.action?_="
        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }
        data = {
            "_" : ""
        }
        if not "JSESSIONID" in self.cookies:
            self.login()
        try:
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
        except Exception as e:
            logging.error(e)

        ret = self.session.get(url=url, cookies=self.cookies, data=data)
        logging.debug(ret)
        logging.debug(ret.text)
        ret_dict = json.loads(ret.text)
        logging.info(ret_dict["message"])
        if not ret_dict["success"] and ret_dict["message"].find("登录") != -1:
            self.login()
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
            ret = self.session.get(url=url, cookies=self.cookies, data=data)
            logging.debug(ret.text)
            ret_dict = json.loads(ret.text)
            logging.info(ret_dict["message"])
        return True
    
    def gaintask(self, taskid):
        if not self.rcookies():
            self.login()

        url = "http://17wo.cn/UserCenterGrowup!gainTaskAwards.action?aId=117&taskId=%d&_=1444124375859" % (taskid)
        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }
        data = {
            "_" : "",
            "taskId": taskid,
            "aId": 117,
        }
        if not "JSESSIONID" in self.cookies:
            self.login()
        try:
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
        except Exception as e:
            logging.error(e)

        ret = self.session.get(url=url, cookies=self.cookies, data=data)
        logging.debug(ret)
        logging.debug(ret.text)
        ret_dict = json.loads(ret.text)
        logging.info(ret_dict["message"])
        if not ret_dict["success"] and (ret_dict["message"].find("登录") != -1 \
                or ret_dict["message"].find("领取任务失败") != -1):
            self.login()
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
            ret = self.session.get(url=url, cookies=self.cookies, data=data)
            logging.debug(ret.text)
            ret_dict = json.loads(ret.text)
            logging.info(ret_dict["message"])
        return True

    def diamond(self, diamondbutton):
        url  = "http://17wo.cn/DiamondFlow!changeStatusOfDiamonds.action?diamondButton=%s" % diamondbutton

        headers = {
            "Host": "17wo.cn",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0"
        }
        data = {
            "diamondButton": diamondbutton,
        }

        if not "JSESSIONID" in self.cookies:
            self.login()
        try:
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
        except Exception as e:
            logging.error(e)

        ret = self.session.get(url=url, cookies=self.cookies, data=data)
        logging.debug(ret)
        logging.debug(ret.text)
        ret_dict = json.loads(ret.text)

        logging.info(ret_dict["data"]["tip"])
        if ret_dict["success"] and (ret_dict["data"]["tip"].find("登录") != -1):
            self.login()
            self.cookies["sessionid"] = self.cookies["JSESSIONID"]
            ret = self.session.get(url=url, cookies=self.cookies, data=data)
            logging.debug(ret.text)
            ret_dict = json.loads(ret.text)
            logging.info(ret_dict["data"]["tip"])

        return True

if __name__ == "__main__":
    check = checkin("phonenum", "passwd")
    if len(sys.argv) < 2:
        check.checkin() 
        for taskid in [28, 29]:
            check.gaintask(taskid)
        check.redpocket()
        check.memberday()
        for button in ["green-con", "red-con", "yellow-con"]:
            check.diamond(button)
    elif sys.argv[1] == "checkin":
        check.checkin() 
    elif sys.argv[1] == "redpocket":
        check.redpocket()
    elif sys.argv[1] == "memerday":
        check.memberday()
    elif sys.argv[1] == "gaintask":
        for taskid in [28, 29]:
            check.gaintask(taskid)
    elif sys.argv[1] == "diamond":
        for button in ["green-con", "red-con", "yellow-con"]:
            check.diamond(button)
