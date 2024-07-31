from datetime import timedelta
from modules.Renamer import Renamer
from modules.Database import Database

from modules.Parser import Parser
from modules.Clockify import Clockify
from modules.Summary import Summary
from modules.TimeTable import TimeTable
from modules.utils import update_add

args = Parser()

print("From :", args.startdate, "to :", args.enddate)
print()
print()

clockify = Clockify(args.token)

days = dict()
projects = dict()
total_work = timedelta()
db = Database()

for w in clockify.get_workspaces():
    for e in clockify.get_time_entries(w, args.startdate, args.enddate):
        # print(e.dump())
        # print(e)
        db.add_entry(e)
db.finalize()

list_day = db.list_day_total(args.startdate, args.enddate, args.ignored_projects, include_not_billable=args.billable)
list_ptday = db.list_projects_tasks_time(args.startdate, args.enddate, args.ignored_projects, include_not_billable=args.billable)
list_ptday_renamed = []

renamer = Renamer(args.projects_rename, args.tasknames)
for x in list_ptday:
    list_ptday_renamed.append(renamer.rename(x))

summary = Summary(list_ptday_renamed)
summary.print()
print()
print()
summary.print(lambda e : e.project)
print()
print()
Summary(list_ptday).print()

ttable = TimeTable(list_day, list_ptday_renamed)
ttable.print()
if args.export:
    ttable.export_csv(args.export_dir, args.rename_export)
