#Import necessary libraries
import pandas as pd
from riotwatcher import LolWatcher
import requests

#Create DataFrame
df_final = pd.DataFrame()

#Enter your API Key, Regions and URL to scrap for top 100 summoners of the region
api_key = input("Enter API Key: ")
watcher = LolWatcher(api_key)
region = input("Enter Region 1: ")
region2 = input("Enter Region 2: ")
url = input('Enter League of graph URL to scrap :')

#Get headers for scrap
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'es-US,es;q=0.9,ko-KR;q=0.8,ko;q=0.7,es-419;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'lolg_euconsent=nitro; languageBanner_es_count=1; _ga=GA1.2.1116464290.1664373462; _gid=GA1.2.439626399.1664373462; _pbjs_userid_consent_data=3524755945110770; na-unifiedid=%7B%22TDID%22%3A%22de7b5400-2ce8-46c3-b424-e71774614bc8%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222022-08-28T13%3A57%3A45%22%7D; cto_bundle=7nQp-V8lMkZTOTdjRDBXNDhVREtseHh2ODY1T3lLUlhWbjlGJTJGUzRXeUNnWnQxaVh4YU5DcHdEdzJZSFFqWURhQktnWk5NV1ROekpIOHByVGFNMmtUcU16aURYUlRDZnB2b3ZvVEhRdk1rJTJGeGFseXVDQmViUFBHYiUyRkR4TWZRMDcwQ0JYbWtHcWIlMkJNeVNGSDB3bmZXYmtDMkFmcWhYMSUyQmJLcTlXUXJkZWJIWklzSDhFJTJCayUzRA',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
#Scrap and get top 100 summoners of the region
response = requests.get(url, headers = headers)
df_summoners = pd.read_html(response.text)[0]
df_summoners = df_summoners.drop(7)
df_summoners['Name'] = df_summoners['Name'].str.split(" KR").str[0]
summoner_list = df_summoners['Name'].tolist()

#Set count to 0 fo keep track
count = 0

#For loop to get info of the 50 last matches of each summoner
for summoner in summoner_list:

    count +=1

    #To start asking thing to the API, we first need the 'Puuid' which is a unique ID for each summoner
    try:
        #To start asking thing to the API, we first need the 'Puuid' which is a unique ID for each summoner
        me = watcher.summoner.by_name(region, summoner)

        #By using this puuid we can get a the last matches of the summoner. The ammount is set to 50, but you can get upto 100 matches
        my_matches = watcher.match.matchlist_by_puuid(region2, me['puuid'], count = 50)
        
        #Now we iterate through each match and get the info of each match
        for match in my_matches:
                
                try:
                    #We get match basic info using match API
                    match_detail_end = watcher.match.by_id(region2, match)
                    
                    #We will only fecth info from classic games, not ARAMs
                    if match_detail_end["info"]["gameMode"] == "CLASSIC":

                        #We get info minute by minute about the match using timeline API
                        match_detail = watcher.match.timeline_by_match(region2, match)

                        #Create dict for team1 and team2 that will later become a df
                        team_1 = {"Gold": 0, "Level": 0, "Minions": 0, "Jungle_minions": 0, "Kills": 0, "Assists": 0, "Deaths": 0, "Plates": 0, "Towers": 0, "Dragons": 0, "Heralds": 0, "Sight_wards": 0, "Control_wards": 0}
                        team_2 = {"Gold": 0, "Level": 0, "Minions": 0, "Jungle_minions": 0, "Kills": 0, "Assists": 0, "Deaths": 0, "Plates": 0, "Towers": 0, "Dragons": 0, "Heralds": 0, "Sight_wards": 0, "Control_wards": 0}
                        
                        #Get All data available in minute 14 for team1
                        for i in range(1, 6): 
                           team_1["Gold"] = team_1["Gold"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["totalGold"]
                           team_1["Level"] = team_1["Level"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["level"]
                           team_1["Minions"] = team_1["Minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["minionsKilled"]
                           team_1["Jungle_minions"] = team_1["Jungle_minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["jungleMinionsKilled"]

                        #Get All data available in minute 14 for team2   
                        for i in range(6, 11): 
                           team_2["Gold"] = team_2["Gold"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["totalGold"]
                           team_2["Level"] = team_2["Level"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["level"]
                           team_2["Minions"] = team_2["Minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["minionsKilled"]
                           team_2["Jungle_minions"] = team_2["Jungle_minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["jungleMinionsKilled"]
                           
                        #Get mean level for each team  
                        team_1["Level"] = team_1["Level"]/5
                        team_2["Level"] = team_2["Level"]/5

                        #Get gold difference         
                        team_1["Gold_diff"] = team_1["Gold"] - team_2["Gold"]
                        team_2["Gold_diff"] = team_2["Gold"] - team_1["Gold"]
                        
                        #The rest of the info is not available in the minute 14 data, so it has to be scarped minute by minute that why we iterate from 1 to 14
                        for i in range(1, 15):

                            #For each minute a list of events its presented, so we can iterate through each event and get necessary info
                            for j in match_detail["info"]["frames"][i]["events"]:

                                #Get Kills, deaths and assists. Each event has a KillerID. 
                                #If the Killer ID is between 1 and 5 is corresponds to team1, if its bigger than 5 is for team2. This pattern is repeated through out the iteration of events
                                if (j["type"] == "CHAMPION_KILL") and (1 <= j["killerId"] <= 5):
                                    team_1["Kills"] += 1
                                    team_2["Deaths"] += 1
                                    try:
                                        team_1["Assists"] += len(j["assistingParticipantIds"])
                                    except:
                                        pass
                                if (j["type"] == "CHAMPION_KILL") and (j["killerId"] > 5):
                                    team_2["Kills"] += 1
                                    team_1["Deaths"] += 1
                                    try:
                                        team_2["Assists"] += len(j["assistingParticipantIds"])
                                    except:
                                        pass
                                
                                #Get Turret plates destroyed
                                if (j["type"] == "TURRET_PLATE_DESTROYED") and (1 <= j["killerId"] <= 5):
                                    team_1["Plates"] += 1
                                if (j["type"] == "TURRET_PLATE_DESTROYED") and (j["killerId"] > 5):
                                    team_2["Plates"] += 1
                                    
                                if (j["type"] == "BUILDING_KILL") and (j["teamId"] == 200):
                                    team_1["Towers"] += 1
                                if (j["type"] == "BUILDING_KILL") and (j["teamId"] == 100):
                                    team_2["Towers"] += 1 
                                
                                #Get Dragons and Heralds
                                if (j["type"] == "ELITE_MONSTER_KILL") and (1 <= j["killerId"] <= 5):
                                    if j["monsterType"] == "DRAGON":
                                        team_1["Dragons"] += 1
                                    elif j["monsterType"] == "RIFTHERALD":
                                        team_1["Heralds"] += 1
                                    
                                if (j["type"] == "ELITE_MONSTER_KILL") and (j["killerId"] > 5):
                                    if j["monsterType"] == "DRAGON":
                                        team_2["Dragons"] += 1
                                    elif j["monsterType"] == "RIFTHERALD":
                                        team_2["Heralds"] += 1                
                                
                                #Get wards placed
                                if (j["type"] == "WARD_PLACED" and j["wardType"] == "CONTROL_WARD") and (1 <= j["creatorId"] <= 5):
                                    team_1["Control_wards"] += 1
                                if (j["type"] == "WARD_PLACED" and j["wardType"] == "CONTROL_WARD") and (j["creatorId"] > 5):
                                    team_2["Control_wards"] += 1
                                    
                                if (j["type"] == "WARD_PLACED" and (j["wardType"] == "SIGHT_WARD" or j["wardType"] == "YELLOW_TRINKET")) and (1 <= j["creatorId"] <= 5):
                                    team_1["Sight_wards"] += 1
                                if (j["type"] == "WARD_PLACED" and (j["wardType"] == "SIGHT_WARD" or j["wardType"] == "YELLOW_TRINKET")) and (j["creatorId"] > 5):
                                    team_2["Sight_wards"] += 1
                        
                        #Get info of team win or lose
                        if match_detail_end["info"]["teams"][0]["win"] == True:
                            team_1["Win"] = 1
                            team_2["Win"] = 0
                        else:
                            team_1["Win"] = 0
                            team_2["Win"] = 1
                        
                        #Dicts of team1 and team2 to df
                        team_1 = pd.DataFrame([team_1], columns=team_1.keys())
                        team_2 = pd.DataFrame([team_2], columns=team_2.keys())

                        #Concat both df to df_final
                        df_temp = pd.concat([team_1, team_2])
                        df_final = pd.concat([df_final, df_temp])
                        
                except:
                    print(f"Match not found: {match}")
       
    except:
        print(f"Summoner not found: {summoner}")
    
    print(f"{count}/100")

#Send df to an excel        
df_final.to_excel(f"{region}-History")