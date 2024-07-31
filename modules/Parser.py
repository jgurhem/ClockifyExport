import argparse
from datetime import datetime
import dateutil.parser
from calendar import monthrange
import shlex


class MultiLignArgumentParser(argparse.ArgumentParser):
    def convert_arg_line_to_args(self, arg_line):
        args = shlex.split(arg_line)
        if len(args) > 0 and args[0].startswith("#"):
            return []
        return args


class Parser:
    def __init__(self) -> None:
        now = datetime.now()
        ndays = monthrange(now.year, now.month)[1]
        default_start = datetime(now.year, now.month, 1, 0, 0, 0)
        default_end = datetime(now.year, now.month, ndays, 23, 59, 59)

        parser = MultiLignArgumentParser(
            description="Download the entries in Clockify to make timesheets for Aneo.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            fromfile_prefix_chars="@",
        )
        parser.add_argument("token", help="User token for API authentication", type=str)
        parser.add_argument(
            "-b",
            "--include-not-billable",
            dest="billable",
            help="Include not billable entries in the output sheet",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--show-per-day",
            dest="perday",
            help="Print daily timetable",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-s",
            "--start-date",
            dest="startdate",
            help="Start date from which retrieve time entries",
            default=default_start,
            type=dateutil.parser.isoparse,
        )
        parser.add_argument(
            "-e",
            "--end-date",
            dest="enddate",
            help="End date to which retrieve time entries",
            default=default_end,
            type=dateutil.parser.isoparse,
        )
        parser.add_argument(
            "-t",
            "--task-in-project",
            dest="tasknames",
            action="extend",
            help="Tasks to count in project instead of a task",
            default=[],
            nargs="+",
            type=str,
        )
        parser.add_argument(
            "-I",
            "--ignore-project",
            dest="ignored_projects",
            action="extend",
            help="Projects and tasks to ignore during computations. 'Project' ignores all tasks from the project. 'Project___' ignores empty tasks. 'Project___Task' ignore the given task.",
            default=[],
            nargs="+",
            type=str,
        )
        parser.add_argument(
            "-r",
            "--rename-project",
            dest="projects_rename",
            action="append",
            help="Projects to rename during entries processing (also allows to merge two projects)",
            default=[],
            nargs=2,
            type=str,
            metavar=("OLD_NAME", "NEW_NAME"),
        )
        parser.add_argument(
            "--export",
            dest="export",
            help="Export in CSV",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--export-dir",
            dest="export_dir",
            help="Directory in which the CSV files will be created",
            default="./exports",
            type=str,
        )
        parser.add_argument(
            "-R",
            dest="rename_export",
            action="append",
            help="Projects+tasks to rename during export only",
            default=[],
            nargs=2,
            type=str,
            metavar=("OLD_NAME", "NEW_NAME"),
        )

        args = parser.parse_args()
        self.token: str = args.token
        self.billable: bool = args.billable
        self.perday: bool = args.perday
        self.startdate: datetime = args.startdate
        self.enddate: datetime = args.enddate
        self.tasknames: list = args.tasknames
        self.ignored_projects: list = args.ignored_projects
        self.export: bool = args.export
        self.export_dir: str = args.export_dir
        self.rename_export: dict = dict()
        for p in args.rename_export:
            self.rename_export[p[0]] = p[1]
        self.projects_rename: dict = dict()
        for p in args.projects_rename:
            self.projects_rename[p[0]] = p[1]
