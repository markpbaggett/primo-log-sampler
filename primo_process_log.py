# import libraries
import re
import random
import csv
from optparse import OptionParser

# set initial variables
# date range/logfile name
file_num = 1
output = open('./output_files/all_search_queries.html', 'w')
output_csv = csv.writer(open('./output_files/output.csv', 'w'))
link_csv = csv.writer(open('./output_files/links.csv', 'w'))
logs_parsed = queries_written = num_of_deeps = advanced = browse = 0
extension = "log"
year = "2013"
month = "10"
file_num_str = ""
url = 'http://search.library.vcu.edu'
number_of_files = 10
month_str = {"01":"Jan", "02":"Feb", "03":"Mar", "04":"Apr", "05":"May", "06":"Jun", "07":"Jul", "08":"Aug", "09":"Sep",
             "10":"Oct", "11":"Nov", "12":"Dec"}
known_items = 1000

# Argument Parsing

parser = OptionParser()
parser.add_option("-x", "--extension", dest="extension", help="Specify extension.  The default is log.")
parser.add_option("-y", "--year", dest="year", help="Specify year.  The default is 2013.")
parser.add_option("-m", "--month", dest="month", help="Specify month.  The default is 10.")
parser.add_option("-l", "--link", dest="link", help="Specify Primo URL.  The default is http://search.library.vcu.edu.")
parser.add_option("-f", "--files", dest="files", help="Specify the number of files to parse.  The default is 10.")
parser.add_option("-s", "--start", dest="start", help="Specify the file to start with.  The default is 1.")

(options, args) = parser.parse_args()

if options:
    if options.extension:
        extension = options.extension
    if options.year:
        year = options.year
    if options.month:
        month = options.month
    if options.link:
        url = options.link
    if options.files:
        number_of_files = int(options.files)
    if options.start:
        file_num = int(options.start)

# date range/logfile name
number_of_files += file_num
while file_num < number_of_files:
    # date range/logfile name
    file_num_str = str(file_num)
    if len(file_num_str) == 1:
        file_num_str = "0" + str(file_num)
    else:
        file_num_str = str(file_num)
    logfile = open('./access_logs/localhost_access_log.{0}-{1}-{2}.{3}'.format(year, month, file_num_str, extension),
                   'r')
    print("Parsing file localhost_access_log.{0}-{1}-{2}.{3}").format(year, month, file_num_str, extension)
    headers = logfile.readlines()
    for header in headers:
        # date range/logfile name
        log = re.search('(^\d+[.]\d+[.]\d+[.]\d+) - - [()[]+(\d+/{0}/{1}):(\d+:\d+:\d+)'.format(month_str[month], year),
                        header)
        query_type = []
        if log:
            ip = log.group(1)
            date = log.group(2)
            time = log.group(3)
            m = re.search('GET (/primo_library/libweb/action/d?l?S?s?earch\.do.*) HTTP/1.1', header)
            # exclude Ex Libris IPs
            if m is not None and ip != '10.14.0.4' and ip != '10.28.0.10':
                m = m.group(1)
                # exclude faceted results pages, browse, course reserve, link resolver
                # first page results only
                if (
                    m.find('ct=facet') == -1 and
                    m.find('&fct') == -1 and
                    m.find('fn=showBrowse') == -1 and
                    m.find('query=browse') == -1 and
                    m.find('fn=BrowseRedirect') == -1 and
                    m.find('tab=cr') == -1 and
                    m.find('&isSerivcesPage=true') == -1 and
                    m.find('%2B') == -1 and
                    m.find('ct=Next') == -1 and
                    (m.find('indx=1') > 0 or m.find('indx') == -1) and
                    (m.find('query=') > 0 or m.find('freeText') > 0)
                    ):
                    query = ''
                    issn = ''
                    if m.find('query=') > 0:
                        query = re.search('query=any[%2C,]+contains[%2C,]+([a-zA-z+%207]*)', m)
                        if query is not None:
                            query = query.group(1)
                        else:
                            query = ''
                            issn = ''
                            issn = re.search('query=is[sb]n[%2C,]+[exactcoins]+[%2C,]+([0-9-]*)', m)
                            if issn is not None:
                                issn = issn.group(1)
                    logs_parsed += 1
                    # search URL prefix
                    link = url + m
                    if "afterPDS=" not in link and "almaAzSearch=" not in link:
                        if 'dlSearch' in link:
                            query_type.append('Deep Link')
                            num_of_deeps += 1
                        else:
                            query_type.append('Internal Search')
                        if 'mode=Advanced' in link:
                            query_type.append('Advanced Search')
                            advanced += 1
                        if '&mode=BrowseSearch' in link:
                            query_type.append('Browse Search')
                            browse += 1
                        output.write('<a href="' + link + '">' + str(logs_parsed) + '</a>&nbsp;&nbsp;&nbsp;Type: ' +
                                     str(query_type) + '</b>\n')
                        output_csv.writerow([str(logs_parsed), date, time, query, issn, link])
                        link_csv.writerow([link])
                        queries_written += 1
    file_num += 1
print("Number of logs parsed: {0}\n".format(logs_parsed))
print("Number of queries written to file: {0}\n".format(queries_written))
print("Number of deep links: {0}\n".format(num_of_deeps))
print("Number of advanced searches: {0}\n".format(advanced))

subs = open('./output_files/sample_set_search_queries.html', 'w')
inp2 = open('./output_files/all_search_queries.html', 'r')
subset = random.sample(inp2.readlines(), known_items)
subs.write("<br>".join(str(x) for x in subset))
reader = csv.reader(open('./output_files/links.csv'))
# my_queries = dict((rows[0],rows[1]) for rows in reader)
my_queries = {}
row_num = 0
for row in reader:
    row_num += 1
    k = str(row_num)
    my_queries[k] = row[0]

known_item_txt = open('./output_files/known_item.txt', 'w')
kx = 1
while kx <= known_items:
    known_item_txt.write('{0}. Is this a <a href="'.format(kx))
    known_item_txt.write(str(my_queries.get(str(kx), 0)))
    known_item_txt.write('">known-item search</a>?\n\nYes\nNo\n\n')
    if kx % 5 == 0:
        known_item_txt.write('[[PageBreak]]\n')
    kx += 1
