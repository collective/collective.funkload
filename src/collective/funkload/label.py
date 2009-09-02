import os
import optparse
import xml.parsers.expat

from zope.testing.testrunner import options
from zope.pagetemplate import pagetemplatefile

from funkload import utils
from funkload import ReportBuilder

from collective.funkload import report

cur_path = os.path.abspath(os.path.curdir)
parser = optparse.OptionParser(
    usage="Usage: %prog", description="""\
Build HTML (fl-build-report --html) and differential (fl-build-report
--diff) reports for multiple bench results at once based on the bench
result labels.  Labels are selected for the X and Y axes to be
compared against each other.""")
parser.add_option(report.parser.get_option('--output-directory'))
parser.add_option(report.parser.get_option('--report-directory'))
parser.add_option(report.parser.get_option('--with-percentiles'))

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
    action="callback", callback=append_filter,
    help="""\
A label filter specifying which reports to include on the X axis.""")
labels_group.add_option(
    '--y-label', '-y', type='string', default=default_filter,
    action="callback", callback=append_filter,
    help="""\
A label filter specifying which reports to include on the Y axis.""")

def build_index(directory, labels):
    utils.trace("Creating report index ...")
    html_path = os.path.join(directory, 'index.html')
    template = pagetemplatefile.PageTemplateFile('label.pt')
    open(html_path, 'w').write(template(labels=labels))
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)
    return html_path

def run(options):
    found = report.results_by_label(options.output_dir)
    labels = {}
    for label in sorted(found):
        for filter in options.x_label + options.y_label:
            if filter(label):
                break
        else:
            continue

        tests = labels.setdefault(label, {}) # XXX
        for test in sorted(found[label]):
            times, paths_vs = found[label][test]
            path = times[max(times)]
            abs_path = os.path.join(options.output_dir, path)

            if not os.path.isfile(os.path.join(abs_path, 'funkload.xml')):
                abs_path = report.build_html_report(options, abs_path)
                path = os.path.basename(abs_path)

            test_d = tests.setdefault(
                test, dict(report=path,
                           name=test.rsplit('.', 1)[-1],
                           diffs={}))
            diffs = test_d['diffs']
            for label_vs in sorted(labels):
                tests_vs = labels[label_vs]
                if label == label_vs or test not in tests_vs:
                    continue

                test_vs_d = tests_vs[test]
                path_vs = test_vs_d['report']
                diffs_vs = test_vs_d['diffs']
                if os.path.dirname(path_vs) not in paths_vs:
                    diff_path = report.build_diff_report(
                        options, abs_path,
                        os.path.join(options.output_dir, path_vs))
                    diff_path = os.path.basename(diff_path)
                    
                diffs_vs[label] = diff_path
                diffs[label_vs] = diff_path

    return build_index(options.output_dir, labels)
    
def main(args=None, values=None):
    (options, args) = parser.parse_args(args, values)
    if args:
        parser.error('does not accept positional arguments')
    return run(options)

if __name__=='__main__':
    main()
