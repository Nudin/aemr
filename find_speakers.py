#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime
import dateutil.parser
import pytz
import sys

api_url = "https://de.wikipedia.org/w/api.php"
if len(sys.argv) == 2:
    language = sys.argv[1]
else:
    language = "tr"

def get_last_active(username):
    query = {
            "action": "query",
            "format": "json",
            "list": "usercontribs",
            "uclimit": "1",
            "ucuser": username,
            "ucprop": "timestamp"
    }

    r = requests.get(api_url, params=query)
    ts = r.json()['query']['usercontribs'][0]['timestamp']
    date = dateutil.parser.parse(ts)
    return date

def test_if_user_active(username, days=30):
    past = datetime.datetime.now() - datetime.timedelta(days=days)
    past = past.replace(tzinfo=pytz.UTC)
    last_edit = get_last_active(username)
    return last_edit > past

def get_users_by_lang(lang):
    query = {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": "Kategorie:User {}-M".format(lang),
            "cmnamespace": "2",
            "cmtype": "page",
            "cmlimit": "max"
    }
    r = requests.get(api_url, params=query)
    members = r.json()['query']['categorymembers']
    return map(lambda x: x['title'], members)


native_speakers = get_users_by_lang(language)
active_users = filter(test_if_user_active, native_speakers)
for user in active_users:
    print(user)

