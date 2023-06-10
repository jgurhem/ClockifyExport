import argparse


class Parser:
    def __init__(self) -> None:
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
            default=None,
        )
        parser.add_argument(
            "-e",
            "--end-date",
            dest="enddate",
            help="End date to which retrieve time entries",
            default=None,
        )

        args = parser.parse_args()
        self.token : str = args.token
        self.billable : bool = args.billable
        self.perday : bool = args.perday
        self.startdate : str = args.startdate
        self.enddate : str = args.enddate
