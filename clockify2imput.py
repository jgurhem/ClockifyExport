import json
from datetime import timedelta
import dateutil.parser
import itertools

from modules.Parser import Parser
from modules.Clockify import Clockify

def extract_tag_name(entry: dict):
    tags = list()
    for t in entry["tags"]:
        tags.append(t["name"])
    return tags


args = Parser()

print("From :", args.startdate, "to :", args.enddate)
print()
print()
print()

clockify = Clockify(args.token)

days = dict()
projects = dict()
total_work = timedelta()
maxlenghtname = 0
day_set = set()
projects_set = set()

for w in clockify.get_workspaces():
    for e in clockify.get_time_entries(w, args.startdate, args.enddate):
        # print(json.dumps(e, indent=4))

        billable = e["billable"]
        if not args.billable and not billable:
            continue

        proj = e["project"]["name"]
        tags = extract_tag_name(e)

        enddate = dateutil.parser.isoparse(e["timeInterval"]["end"])
        startdate = dateutil.parser.isoparse(e["timeInterval"]["start"])
        duration = enddate - startdate

        d = days.get(startdate.date(), dict())
        if len(tags) == 0 or "Daily" in tags or "Entretien Technique" in tags:
            k = proj
        else:
            k = proj + "___" + str(tags)
        maxlenghtname = max(maxlenghtname, len(k))
        v = d.get(k, timedelta())
        v += duration
        d[k] = v

        s = d.get("Sum", timedelta())
        s += duration
        d["Sum"] = s
        days[startdate.date()] = d

        day_set.add(startdate.date())
        projects_set.add(k)

        p = projects.get(k, timedelta())
        p += duration
        projects[k] = p

        total_work += duration

if args.perday:
    for k1 in days.keys().__reversed__():
        v1 = days[k1]
        print(k1, v1)
        # sum = timedelta(hours=7.5)
        for k2, v2 in v1.items():
            if k2 == 'Sum':
                continue
            print("\t", f"{k2:{maxlenghtname}s}", " --- ", f"{v2/v1['Sum']:.2f}")
        print()
    print()
    print()
    print()

day_set = sorted(day_set)
for key, group in itertools.groupby(day_set, key=lambda e : (e.year, e.month)):
    group = list(group)
    print(f"{str(key):{maxlenghtname}s}", end='  ')
    for d in group:
        print(f"{d.day:6d}", end='')
    print(f"{'Sum':>7}", end='')
    print()
    print()
    for p in sorted(projects_set):
        line = f"{p:{maxlenghtname}s}  "
        s = 0
        for d in group:
            t = int(days[d].get(p, timedelta(0))/days[d]['Sum']*100)
            s += t
            line += f"{t:6d}"
        line += f"{s:7d}"
        if s > 0:
            print(line)
    print()
    print()
    print()

for k in sorted(projects.keys()):
    v = projects[k]
    print(f"{k:{maxlenghtname}s}", " --- ", f"{v/total_work*100:=6.2f}")
