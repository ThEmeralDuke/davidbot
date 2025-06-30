import json
with open("settings.json") as file:
    thing=file.read()
file.close()
data= json.loads(thing)
role=data["1170300324381216798"]["Settings"]["RRLeaderboardTimer"]
print(role)
