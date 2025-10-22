import requests as req
import pandas as pd
import json
import streamlit as st
import os

#Part That initializes the connection
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
#This section includes anything to do with working on the Dataframes

#adds a new row, or updates the old Dataframe
def upsert(df1, df2, indexvariable):
    df1[indexvariable] = df1[indexvariable].astype(str)
    df2[indexvariable] = df2[indexvariable].astype(str)
    df1 = df1.set_index(indexvariable)
    df2 = df2.set_index(indexvariable)
    df_merged = df2.combine_first(df1).reset_index()
    return df_merged

#saves/reads a Dataframe to/from a pickle file
def saveDFasPkl(df, folder, filename):
    full_path = os.path.join(folder, f"{filename}.pkl")
    os.makedirs(folder, exist_ok = True)
    df.to_pickle(full_path)

def readPklFile(folder, filename):
    full_path = os.path.join(folder, f"{filename}.pkl")
    os.makedirs(folder, exist_ok = True)
    file = pd.read_pickle(full_path)
    return file


#This section includes all the getter functions for the different Tables

#returns a pandas Dataframe containing informmation about a Clan
def getClantable(clantag):
    clantag = urlTag(clantag)
    responseData = getResponse(f"{baseUrl}clans/{clantag}")
    clanData = {"tag" : [], "name" : [], "members" : [], "clanLevel" : [], "warWins" : [], "warTies" : [], "warLosses": [], "isWarLogPublic" : []}
    for col in clanData:
        clanData[col].append(responseData[col])
    clanData = pd.DataFrame(clanData)
    return clanData

def getMemberTable(clantag):
    clantag = urlTag(clantag)
    responseData = getResponse(f"https://api.clashofclans.com/v1/clans/{clantag}")
    memberDict = {"name" : [], "tag" : [], "role" : [], "townHallLevel" : [], "trophies" : [], "clanRank" : [], "donationsReceived" : [], "donations" : [], "expLevel" : []}
    rawMemberList = responseData["memberList"]
    for i in range(len(rawMemberList)):
        for col in memberDict:
            memberDict[col].append(rawMemberList[i][col])
    memberDict = pd.DataFrame(memberDict)
    memberDict["role"] = memberDict["role"].replace("admin", "elder")
    return memberDict


#Update funcs
def updateClanTable(df):
    clantags = df["tag"].values.tolist()
    print(clantags)
    for clantag in clantags:
        newClanData = getClantable(clantag)
        print(newClanData.head())
        df = upsert(df, newClanData, "tag")
    return df


# returns a pandas Dataframe containing clanwar information
def addWar(clantag):
    clantag = urlTag(clantag)
    response_data = getResponse(f"{baseUrl}clans/{clantag}/currentwar")
    
clanTable = readPklFile("DataFrames", "clanTable")
st.dataframe(clanTable)
clanTable = updateClanTable(clanTable)
st.dataframe(clanTable)
warstats = addWar("#2P9YRQOGJ")
print(warstats)
st.dataframe(warstats)
Crew_members = getMemberTable("#YV0LULVC")

st.dataframe(Crew_members)
