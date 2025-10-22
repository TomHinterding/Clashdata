import requests as req
import pandas as pd
import json
import streamlit as st
import pprint


with open("token.env", "r") as f:
    API_TOKEN = f.read().strip()
header = {"Authorization" : f"Bearer {API_TOKEN}"}
baseUrl = "https://api.clashofclans.com/v1/"

def urlTag(tag):
    return tag.replace('#', '%23')

def getResponse(url):
    response = req.get(url, headers = header)
    if response.status_code == 200:
        response_data = json.loads(response.text)
        return response_data
    else:
        response.raise_for_status()

def getMemberTable(clantag):
    clantag = urlTag(clantag)
    response_data = getResponse(f"https://api.clashofclans.com/v1/clans/{clantag}")
    memberDict = {"name" : [], "tag" : [], "role" : [], "townHallLevel" : [], "trophies" : [], "clanRank" : [], "donationsReceived" : [], "donations" : [], "expLevel" : []}
    rawMemberList = response_data["memberList"]
    for i in range(len(rawMemberList)):
        for col in memberDict:
            memberDict[col].append(rawMemberList[i][col])
    memberDict = pd.DataFrame(memberDict)
    memberDict["role"] = memberDict["role"].replace("admin", "elder")
    return memberDict

def getClantable(clantag):
    clantag = urlTag(clantag)
    response_data = getResponse(f"{baseUrl}clans/{clantag}")

def addWar(clantag):
    clantag = urlTag(clantag)
    response_data = getResponse(f"{baseUrl}clans/{clantag}/currentwar")
    

warstats = addWar("#2P9YRQOGJ")
print(warstats)
st.dataframe(warstats)
Crew_members = getMemberTable("#YV0LULVC")

st.dataframe(Crew_members)