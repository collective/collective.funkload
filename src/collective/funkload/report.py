import os
import collections
import optparse
import xml.parsers.expat

from funkload import utils
from funkload import ReportRenderHtml
from funkload import ReportRenderDiff
from funkload import ReportBuilder

parser = optparse.OptionParser(
    ReportBuilder.USAGE,
    formatter=optparse.TitledHelpFormatter(),
    version="FunkLoad %s" % utils.get_version())
parser.add_option("-o", "--output-directory", type="string",
                  dest="output_dir",
                  help="Parent directory to store reports, the directory"
                  "name of the report will be generated automatically.",
                  default=os.path.abspath(os.getcwd()))
parser.add_option("-r", "--report-directory", type="string",
                  dest="report_dir",
                  help="Directory name to store the report.",
                  default=None)
parser.add_option("-P", "--with-percentiles", action="store_true",
                  default=True, dest="with_percentiles",
                  help=("Include percentiles in tables, use 10%, 50% and"
                        " 90% for charts, default option."))

def build_html_report(options, xml_file):
    """Build a HTML report for the given XML bench results file"""
    options.xml_file = xml_file
    options.html = True
    xml_parser = ReportBuilder.FunkLoadXmlParser()
    xml_parser.parse(xml_file)
    utils.trace("Creating html report ...")
    html_path = ReportRenderHtml.RenderHtml(
        xml_parser.config, xml_parser.stats,
        xml_parser.error, xml_parser.monitor,
        options)()
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)
    return os.path.dirname(html_path)

def build_diff_report(options, directory_1, directory_2):
    """Build a differential report for the given HTML report directories"""
    utils.trace("Creating diff report ...")
    output_dir = options.output_dir
    html_path = ReportRenderDiff.RenderDiff(
        directory_1, directory_2, options)
    utils.trace("done: \n")
    utils.trace("%s\n" % html_path)
    return os.path.dirname(str(html_path))

Test = collections.namedtuple(
    'Test', ['times', 'diffs', 'module', 'class_', 'method'])

class FunkLoadConfigParser(ReportBuilder.FunkLoadXmlParser, object):
    """XML bench results parser that only extracts config"""

    def __init__(self):
        """Disable the eng element handler"""
        super(FunkLoadConfigParser, self).__init__()
        self.parser.EndElementHandler = None

def results_by_label(directory):
    labels = {}
    for path in os.listdir(directory):
        abs_path = os.path.join(directory, path)
        xml_parser = FunkLoadConfigParser()

        is_report = False
        report_path = os.path.join(path, 'funkload.xml')
        report_abs_path = os.path.join(directory, report_path)
        diff_path = os.path.join(path, 'diffbench.dat')
        diff_abs_path = os.path.join(directory, diff_path)
        path_vs = None

        if os.path.isfile(report_abs_path):
            # Is a HTML report directory, use the contained XML
            xml_parser.parse(report_abs_path)
            is_report = True
        elif os.path.isfile(diff_abs_path):
            # Is a diff report directory, use the contained DAT to get
            # the two test paths, parse the 
            diff_path = path
            opened = open(diff_abs_path)
            abs_path, abs_path_vs = opened.readline(
                )[1:].strip().split(' vs ')
            opened.close()
            path = os.path.basename(abs_path)
            path_vs = os.path.basename(abs_path_vs)
            parse_path = abs_path
            report_path = os.path.join(abs_path, 'funkload.xml')
            if os.path.isfile(report_path):
                parse_path = report_path
            xml_parser.parse(parse_path)
        else:
            try:
                xml_parser.parser.ParseFile(open(abs_path))
            except (IOError, xml.parsers.expat.ExpatError):
                # Is not a parsable funkload file, ignore
                continue
            # Is a bench results XML file itself, use directly

        if 'label' in xml_parser.config and xml_parser.config[
            'label']:
            label = labels.setdefault(xml_parser.config['label'], {})
            test = label.setdefault(
                xml_parser.config['method'], Test(
                    times={}, diffs={},
                    module=xml_parser.config['module'],
                    class_=xml_parser.config['class'],
                    method=xml_parser.config['method']))
            time = xml_parser.config['time']
            if time not in test.times or is_report:
                test.times[time] = path
            if path_vs:
                test.diffs[path_vs] = diff_path
                
    return labels
