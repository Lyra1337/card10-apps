import requests
import datetime
import json


URL = "https://fahrplan.events.ccc.de/camp/2019/Fahrplan/schedule.json"


def main():
    r = requests.get(URL)
    ev_json = r.json()

    events = []
    for day in ev_json["schedule"]["conference"]["days"]:
        for room in day["rooms"].values():
            for e in room:
                new_e = {}
                new_e["date"] = e["date"]
                new_e["start"] = e["start"]
                new_e["duration"] = e["duration"]
                new_e["room"] = e["room"]
                new_e["title"] = e["title"]
                new_e["language"] = e["language"]
                new_e["abstract"] = e["abstract"]
                new_e['timestamp'] = int(datetime.datetime.fromisoformat(e['date']).timestamp()) - 946684800
                new_e["day"] = str(day["index"])

                events.append(new_e)

    events = sorted(events, key=lambda e: e["timestamp"])

    conf = {
        "events": events,
        "daysCount": ev_json["schedule"]["conference"]["daysCount"]
    }

    with open("schedule.json", "w") as f:
        f.write(json.dumps(conf))

if __name__ == "__main__":
    main()
