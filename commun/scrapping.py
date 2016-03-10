#!/usr/bin/env python
# -*- coding: utf-8 -*-

from config.logconfig import logger

def geturlpost(session_requests,url,data,headers):
    logger.debug("Scrap (POST) " +  url);
    #result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    result = session_requests.post(url, data=data, headers= headers);
    return result
    
def geturlget(session_requests, url, data, headers):
    logger.debug("Scrap " +  url);
    # result = session_requests.get(config.URL, headers = dict(referer = config.URL))
    result = session_requests.get(url,data = data, headers = headers)
    return result