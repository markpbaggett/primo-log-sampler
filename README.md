# Primo Log Sampler

---

### About

This script was developed by Emily Owens at VCU and Mark Baggett at UTK. It is the method of search sampling used for the article "Building Bridges with Logs: Collaborative Conversations about Discovery across Library Departments" (http://journal.code4lib.org/?p=11355) as well as the ELUNA 2016 presentation "Territory Folks Should all be Pals: Qualitative Use of Search Logs to Improve Confidence in and Communication about a Library Discovery Service".

This script will create a HTML report of 100 search queries from a Primo search log file. The report excludes Ex Libris IPs from searches, faceted results pages, browse, course reserve, link resolver searches and only include the first page of search results. After running it will report back the number of logs parsed, the number of queries writen to the file, number of deep links and the number of advanced searches. The script is written in Python and requires the re, random and csv libraries.

### Option Parsing

The following arguments are available from the CLI:

* -y 
	* Allows you to specify the year of your logs
	* Defaults to **2013**
* -m 
	* Allows you to specify the month of your logs
	* Defaults to **10**
* -x
	* Allows you to specify the log extension
	* Defaults to **log**  	
* -l
	* Allows you to specify the Primo Url.
	* Defaults to **http://search.library.vcu.edu**
* -f
	* Allows you to specify the number of log files to parse.
	* Defaults to **10**
* -s
	* Allows you to specify the log number to start with
	* Defaults to **1** 

### Examples 	
 
**python primo_process_log.py**

* This command process logs that match the following format:
	* localhost_access_log.2013-10-*.log
* The first log processed with this would be:
	* localhost_access_log.2013-10-1.log
* The expected institution value would be:
	* http://search.library.vcu.edu
* The number of log files to be parsed would be 10:
	* 10 	

**python primo_process_log.py -y 2016 -m 02 -x txt -l http://utk-almaprimo.hosted.exlibrisgroup.com -f 3 -s 11**

* This command process logs that match the following format:
	* localhost_access_log.2016-02-*.txt
* The first log processed with this would be:
	* localhost_access_log.2016-02-11.log
* The expected institution value would be:
	* http://utk-almaprimo.hosted.exlibrisgroup.com
* The number of log files to be parsed would be 10:
	* 3