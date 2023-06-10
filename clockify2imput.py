from datetime import timedelta
import itertools

from modules.Parser import Parser
from modules.Clockify import Clockify

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
        if not args.billable and not e.billable:
            continue

        d = days.get(e.startdate.date(), dict())
        if len(e.tags) == 0 or "Daily" in e.tags or "Entretien Technique" in e.tags:
            k = e.project
        else:
            k = e.project + "___" + str(e.tags)
        maxlenghtname = max(maxlenghtname, len(k))
        v = d.get(k, timedelta())
        v += e.duration
        d[k] = v

        s = d.get("Sum", timedelta())
        s += e.duration
        d["Sum"] = s
        days[e.startdate.date()] = d

        day_set.add(e.startdate.date())
        projects_set.add(k)

        p = projects.get(k, timedelta())
        p += e.duration
        projects[k] = p

        total_work += e.duration

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
