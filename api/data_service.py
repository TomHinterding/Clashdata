import client as c
import pandas as pd

class getTables:
    def __init__(self):
        self.api = c.APIManager()

    def getClantable(self, clantag):
        clantag = self.api.urlTag(clantag)
        responseData = self.api.getResponse(f"{self.api.baseUrl}clans/{clantag}")
        clanData = {"tag" : [], "name" : [], "members" : [], "clanLevel" : [], "warWins" : [], "warTies" : [], "warLosses": [], "isWarLogPublic" : []}
        for col in clanData:
            clanData[col].append(responseData[col])
        clanData = pd.DataFrame(clanData)
        return clanData
    
    def getMemberTable(self, clantag):
        clantag = self.api.urlTag(clantag)
        responseData = self.api.getResponse(f"{self.api.baseUrl}clans/{clantag}")
        memberDict = {"name" : [], "tag" : [], "role" : [], "townHallLevel" : [], "trophies" : [], "clanRank" : [], "donationsReceived" : [], "donations" : [], "expLevel" : []}
        rawMemberList = responseData["memberList"]
        for i in range(len(rawMemberList)):
            for col in memberDict:
                memberDict[col].append(rawMemberList[i][col])
        memberDict = pd.DataFrame(memberDict)
        memberDict["role"] = memberDict["role"].replace("admin", "elder")
        return memberDict