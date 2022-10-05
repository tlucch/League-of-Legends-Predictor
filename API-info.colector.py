import pandas as pd
from riotwatcher import LolWatcher
import requests

df_final = pd.DataFrame()

api_key = input("Enter API Key: ")
watcher = LolWatcher(api_key)

region = input("Enter Region 1: ")
region2 = input("Enter Region 2: ")

url = input('Enter League of graph URL to scrap :')
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
response = requests.get('https://www.leagueofgraphs.com/rankings/summoners/kr', headers = headers)
df_summoners = pd.read_html(response.text)[0]
df_summoners = df_summoners.drop(7)

df_summoners['Name'] = df_summoners['Name'].str.split(" KR").str[0]

summoner_list = df_summoners['Name'].tolist()

count = 0
for summoner in summoner_list:

    count +=1
    try:
        me = watcher.summoner.by_name(region, summoner)
    
        my_matches = watcher.match.matchlist_by_puuid(region2, me['puuid'], count = 50)
        
        
        for match in my_matches:
                
                try:
                    match_detail_end = watcher.match.by_id(region2, match)
                
                    if match_detail_end["info"]["gameMode"] == "CLASSIC":
                        
                        match_detail = watcher.match.timeline_by_match(region2, match)
                        team_1 = {"Gold": 0, "Level": 0, "Minions": 0, "Jungle_minions": 0, "Kills": 0, "Assists": 0, "Deaths": 0, "Plates": 0, "Towers": 0, "Dragons": 0, "Heralds": 0, "Sight_wards": 0, "Control_wards": 0}
                        team_2 = {"Gold": 0, "Level": 0, "Minions": 0, "Jungle_minions": 0, "Kills": 0, "Assists": 0, "Deaths": 0, "Plates": 0, "Towers": 0, "Dragons": 0, "Heralds": 0, "Sight_wards": 0, "Control_wards": 0}
                        
                        for i in range(1, 6): 
                           team_1["Gold"] = team_1["Gold"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["totalGold"]
                           team_1["Level"] = team_1["Level"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["level"]
                           team_1["Minions"] = team_1["Minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["minionsKilled"]
                           team_1["Jungle_minions"] = team_1["Jungle_minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["jungleMinionsKilled"]
                           
                        for i in range(6, 11): 
                           team_2["Gold"] = team_2["Gold"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["totalGold"]
                           team_2["Level"] = team_2["Level"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["level"]
                           team_2["Minions"] = team_2["Minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["minionsKilled"]
                           team_2["Jungle_minions"] = team_2["Jungle_minions"] + match_detail["info"]["frames"][14]["participantFrames"][f"{i}"]["jungleMinionsKilled"]
                           
                           
                        team_1["Level"] = team_1["Level"]/5
                        team_2["Level"] = team_2["Level"]/5        
                        team_1["Gold_diff"] = team_1["Gold"] - team_2["Gold"]
                        team_2["Gold_diff"] = team_2["Gold"] - team_1["Gold"]
                        
                        for i in range(1, 15):
                            for j in match_detail["info"]["frames"][i]["events"]:
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
                                
                                if (j["type"] == "TURRET_PLATE_DESTROYED") and (1 <= j["killerId"] <= 5):
                                    team_1["Plates"] += 1
                                if (j["type"] == "TURRET_PLATE_DESTROYED") and (j["killerId"] > 5):
                                    team_2["Plates"] += 1
                                    
                                if (j["type"] == "BUILDING_KILL") and (j["teamId"] == 200):
                                    team_1["Towers"] += 1
                                if (j["type"] == "BUILDING_KILL") and (j["teamId"] == 100):
                                    team_2["Towers"] += 1 
                                
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
                                
                                if (j["type"] == "WARD_PLACED" and j["wardType"] == "CONTROL_WARD") and (1 <= j["creatorId"] <= 5):
                                    team_1["Control_wards"] += 1
                                if (j["type"] == "WARD_PLACED" and j["wardType"] == "CONTROL_WARD") and (j["creatorId"] > 5):
                                    team_2["Control_wards"] += 1
                                    
                                if (j["type"] == "WARD_PLACED" and (j["wardType"] == "SIGHT_WARD" or j["wardType"] == "YELLOW_TRINKET")) and (1 <= j["creatorId"] <= 5):
                                    team_1["Sight_wards"] += 1
                                if (j["type"] == "WARD_PLACED" and (j["wardType"] == "SIGHT_WARD" or j["wardType"] == "YELLOW_TRINKET")) and (j["creatorId"] > 5):
                                    team_2["Sight_wards"] += 1
                        
                        if match_detail_end["info"]["teams"][0]["win"] == True:
                            team_1["Win"] = 1
                            team_2["Win"] = 0
                        else:
                            team_1["Win"] = 0
                            team_2["Win"] = 1
                        
                        team_1 = pd.DataFrame([team_1], columns=team_1.keys())
                        team_2 = pd.DataFrame([team_2], columns=team_2.keys())
                        df_temp = pd.concat([team_1, team_2])
                        df_final = pd.concat([df_final, df_temp])
                        
                except:
                    print(f"Match not found: {match}")
       
    except:
        print(f"Summoner not found: {summoner}")
    
    print(f"{count}/100")
        
df_final.to_excel(f"{region}-History")