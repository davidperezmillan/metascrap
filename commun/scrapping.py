#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

def geturlpost(session_requests,url,data,headers):
    logging.debug("Scrap (POST) " +  url);
    #result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    result = session_requests.post(url, data=data, headers= headers);
    return result
    
def geturlget(session_requests, url, data, headers):
    logging.debug("Scrap " +  url);
    # result = session_requests.get(config.URL, headers = dict(referer = config.URL))
    result = session_requests.get(url,data = data, headers = headers)
    return result