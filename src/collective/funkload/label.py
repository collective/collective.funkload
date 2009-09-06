import sys
import os
import collections
import optparse
import cStringIO

from zope.testing.testrunner import options
from zope.pagetemplate import pagetemplatefile

from funkload import utils

from collective.funkload import report

cur_path = os.path.abspath(os.path.curdir)
parser = optparse.OptionParser(
    description="""\
Build HTML (fl-build-report --html) and differential (fl-build-report
--diff) reports for multiple bench results at once based on the bench
result labels.  Labels are selected for the X and Y axes to be
compared against each other.""")
parser.add_option(report.output_option)
parser.add_option(report.report_option)
parser.add_option(report.percent_option)

labels_group = optparse.OptionGroup(parser, "Labels", """\
Options in this group are used to define the lables for which to build
reports.  Specify a bench label filter as regular expressions.  These
are case-sensitive regular expression, used in search (not match)
mode, to limit which labels are included.  The regular expressions are
checked against the label given to the"fl-run-bench --label" option .
In an extension of Python regexp notation, a leading"!" is stripped
and causes the sense of the remaining regexp to be negated (so "!bc"
matches any string that does not match "bc", and vice versa).  The
option can be specified multiple times. Reports are generated for the
latest bench results whose label matched any of the label filters.  If
no label filter is specified, then all bench results with a label are
used.  The bench results inside HTML report directories are included
in the search.""")

default_filter = [options.compile_filter('.')]
def append_filter(option, opt_str, value, parser):
    values = getattr(parser.values, option.dest)
    if values is default_filter:
        values = []
    values.append(options.compile_filter(value))
    setattr(parser.values, option.dest, values)

labels_group.add_option(
    '--x-label', '-x', type='string', default=default_filter,
    action="callback", callback=append_filter, metavar='REGEXP',
    help="""\
A label filter specifying which reports to include on the X axis.""")
labels_group.add_option(
    '--y-label', '-y', type='string', default=default_filter,
    action="callback", callback=append_filter, metavar='REGEXP',
    help="""\
A label filter specifying which reports to include on the Y axis.""")
labels_group.add_option(report.reverse_option)

parser.add_option_group(labels_group)

def open_callback(option, opt_str, value, parser):
    setattr(parser.values, option.dest, open(value))

content_group = optparse.OptionGroup(
    parser, "Content", "Content to render above the index matrix")
title_option = content_group.add_option(
    '--title', '-t', default="", metavar="STRING",
    help="Title to render in the HTML head and at the top.  "
    "[default: 'collective.funkload label matrix report']")
sub_title_option = content_group.add_option(
    '--sub-title', '-s', default="", metavar="STRING",
    help="Sub-title to render below the title.  "
    "[default: <generated from labels for X and Y axes>]")
input_default = os.isatty(
    sys.stdin.fileno()) and cStringIO.StringIO('') or sys.stdin
input_option = content_group.add_option(
    '--input', '-i', type='string', metavar="FILE",
    action='callback', callback=open_callback, default=input_default,
    help="Text or HTML to include below the subtitle and above the "
    "matrix.  [default: stdin]")
parser.add_option_group(content_group)

def build_index(directory, x_labels, y_labels,
                reverse=report.reverse_option.default,
                title=title_option.default,
                sub_title=sub_title_option.default,
                input_=input_option.default):
    utils.trace("Creating report index ...")
    html_path = os.path.join(directory, 'index.html')
    template = pagetemplatefile.PageTemplateFile('label.pt')
    open(html_path, 'w').write(
        template(x_labels=x_labels, y_labels=y_labels, reverse=reverse,
                title=title, sub_title=sub_title, input_=input_.read()))
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)
    return html_path

Test = collections.namedtuple(
    'Test', ['report', 'name', 'diffs', 'module', 'class_', 'method'])

def process_axis(options, found, labels, labels_vs, label):
    tests = labels.setdefault(label, {})
    for test in sorted(found[label]):
        found_test = found[label][test]
        bench = found_test.times[max(found_test.times)]

        if test in labels_vs.get(label, {}):
            test_tuple = tests.setdefault(
                test, labels_vs[label][test])
            path = test_tuple.report
            abs_path = os.path.join(options.output_dir, path)
        else:
            path = bench.path
            abs_path = os.path.join(options.output_dir, path)

            if not os.path.isfile(
                os.path.join(abs_path, 'funkload.xml')):
                abs_path = report.build_html_report(options, abs_path)
                path = os.path.basename(abs_path)

            test_tuple = tests.setdefault(
                test, Test(report=path,
                           name=test.rsplit('.', 1)[-1],
                           diffs={},
                           module=found_test.module,
                           class_=found_test.class_,
                           method=found_test.method))

        for label_vs in sorted(labels_vs):
            tests_vs = labels_vs[label_vs]
            if label == label_vs or test not in tests_vs:
                continue

            test_vs_tuple = tests_vs[test]
            diff_path = bench.diffs.get(test_vs_tuple.report)
            if not diff_path:
                diff_path = report.build_diff_report(
                    options, abs_path, os.path.join(
                        options.output_dir, test_vs_tuple.report))
                diff_path = os.path.basename(diff_path)
            test_vs_tuple.diffs[label] = diff_path
            test_tuple.diffs[label_vs] = diff_path

def run(options):
    found = report.results_by_label(options.output_dir)
    x_labels = {}
    y_labels = {}
    for label in sorted(found, reverse=options.reverse):
        matched = False
        for filter in options.x_label:
            if filter(label):
                process_axis(
                    options, found, x_labels, y_labels, label)
                break

        for filter in options.y_label:
            if filter(label):
                process_axis(
                    options, found, y_labels, x_labels, label)
                break

    return build_index(
        options.output_dir, x_labels, y_labels, options.reverse,
        options.title, options.sub_title, options.input)
    
def main(args=None, values=None):
    (options, args) = parser.parse_args(args, values)
    if args:
        parser.error('does not accept positional arguments')
    return run(options)

if __name__=='__main__':
    main()
