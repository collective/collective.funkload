import os
import re
import bisect
import datetime

from funkload import ReportRenderDiff
from funkload import utils

from collective.funkload import report

description = """\
Generate FunkLoad differential reports against the previous report and
against any available reports from a day, a week, a month and a year
ago."""

zero_delta = datetime.timedelta(0)

report_re = re.compile(
    r'^([^-]*)-(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})$')

def parse_date(match):
    return datetime.datetime(*map(int, match.groups()[1:]))

def get_report_dates(reports_dir):
    results = {}
    for path in os.listdir(reports_dir):
        match = report_re.match(path)
        if match is not None:
            test = match.group(1)
            bisect.insort(
                results.setdefault(test, []),
                (parse_date(match), os.path.join(reports_dir, path)))
    return results

def build_diff(options, report_dir1, report_dir2):
    utils.trace("Creating diff report ...")
    html_path = ReportRenderDiff.RenderDiff(
        report_dir1, report_dir2, options)
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)

def get_yesterday(from_date):
    return (from_date-datetime.timedelta(days=2),
            from_date-datetime.timedelta(days=1))

def get_last_week(from_date):
    return (from_date-datetime.timedelta(weeks=2),
            from_date-datetime.timedelta(weeks=1))

def get_last_month(from_date):
    return (from_date.replace(month=from_date.month-2),
            from_date.replace(month=from_date.month-1))

def get_last_year(from_date):
    return (from_date.replace(year=from_date.year-2),
            from_date.replace(year=from_date.year-1))

intervals = (get_yesterday,
             get_last_week,
             get_last_month,
             get_last_year)

def reverse_reports(reports):
    while reports:
        yield reports.pop()

def get_interval_reports(latest_date, latest_path, reports):
    candidate_date = latest_date
    candidate_path = latest_path
    reports_iter = reverse_reports(reports)
    for interval in intervals:
        min, target = interval(latest_date)
        candidate_delta = candidate_date - target

        for report_date, report_path in reports_iter:
    
            if report_date > target:
                report_delta = report_date - target
            else:
                report_delta = target - report_date
    
            if report_delta < candidate_delta:
                pass
            elif report_date < target or report_date < min:
                yield candidate_date, candidate_path
                candidate_date = report_date
                candidate_path = report_path
                candidate_delta = report_delta
                break
    
            candidate_date = report_date
            candidate_path = report_path
            candidate_delta = report_delta

        else:
            if candidate_date > min:
                yield candidate_date, candidate_path

def run(options):
    report.build_html_reports(options, options.output_dir)
    for reports in get_report_dates(options.output_dir).itervalues():
        if len(reports) < 2:
            continue

        latest_date, latest_path = reports.pop()

        # Generate the diff for the previous report
        prev_date, prev_path = reports.pop()
        build_diff(options, prev_path, latest_path)

        if not reports:
            continue

        # Generate the diffs for the intervals
        for report_date, report_path in get_interval_reports(
            latest_date, latest_path, reports):
            build_diff(options, report_path, latest_path)

def main():
    (options, args) = parser.parse_args()
    if args:
        parser.error('does not accept positional arguments')
    return run(options)

if __name__=='__main__':
    main()
