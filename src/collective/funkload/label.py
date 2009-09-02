import os
import optparse

from zope.testing.testrunner import options

from funkload import utils

from collective.funkload import report

def append_filter(option, opt_str, value, parser):
    parser.values.ensure_value(option.dest, []).append(
        options.compile_filter(value))

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
labels_group.add_option(
    '--x-label', '-x',
    action="callback", callback=append_filter, type='string',
    help="""\
A label filter specifying which reports to include on the X axis.""")
labels_group.add_option(
    '--y-label', '-y',
    action="callback", callback=append_filter, type='string',
    help="""\
A label filter specifying which reports to include on the Y axis.""")

def build_index(directory, labels):
    utils.trace("Creating report index: ...")
    html_path = os.path.join(directory, 'index.html')
    open(html_path, 'w').write(repr(labels))
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)
    return html_path

def run(options):
    found = report.results_by_label(options.output_dir)
    labels = {}
    for label in found:
        for filter in options.x_label + options.y_label:
            if filter(label):
                break
        else:
            continue

        tests = labels.setdefault(label, {}) # XXX
        for test, times in found[label].iteritems():
            rel_path = times[max(times)]
            path = os.path.join(options.output_dir, rel_path)
            if report.results_re.match(path) is not None:
                path = report.build_html_report(options, path)

            path, diffs = tests.setdefault(test, (path, {}))
            for label_vs, tests_vs in labels.iteritems():
                if label == label_vs or test not in tests_vs:
                    continue

                path_vs, diffs_vs = tests_vs[test]
                diff_path = report.build_diff_report(
                    options,
                    os.path.dirname(path), os.path.dirname(path_vs))
                    
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
