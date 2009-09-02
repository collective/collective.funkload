import os
import re
import optparse

from funkload import utils
from funkload import ReportRenderHtml
from funkload import ReportBuilder

results_re = re.compile(
    r'^([^-]*)-bench-(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2}).xml$')

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
    utils.trace("Creating html report: ...")
    html_path = ReportRenderHtml.RenderHtml(
        xml_parser.config, xml_parser.stats,
        xml_parser.error, xml_parser.monitor,
        options)()
    utils.trace("done: \n")
    utils.trace("file://%s\n" % html_path)

def build_html_reports(options, directory):
    """Build HTML reports for all bench results in the directory"""
    for path in os.listdir(directory):
        match = results_re.match(path)
        if match is not None:
            abs_path = os.path.join(directory, path)
            xml_parser = ReportBuilder.FunkLoadXmlParser()
            xml_parser.parse(abs_path)
            if not os.path.isdir(os.path.join(
                directory,
                xml_parser.config['method']+match.group(1))):
                build_html_report(options, abs_path)
