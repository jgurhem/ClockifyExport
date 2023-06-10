import argparse
from datetime import datetime
import dateutil.parser
from calendar import monthrange


class Parser:
    def __init__(self) -> None:

        now = datetime.now()
        ndays = monthrange(now.year, now.month)[1]
        default_start = datetime(now.year, now.month, 1, 0, 0, 0)
        default_end = datetime(now.year, now.month, ndays, 23, 59, 59)

        parser = argparse.ArgumentParser(
            description="Download the entries in Clockify to make timesheets for Aneo.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
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

        args = parser.parse_args()
        self.token : str = args.token
        self.billable : bool = args.billable
        self.perday : bool = args.perday
        self.startdate : datetime = args.startdate
        self.enddate : datetime = args.enddate
