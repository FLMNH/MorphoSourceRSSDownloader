# MorphoSourceRSSDownloader
MorphoSource RSS Downloader  
Florida Museum of Natural History  
Office of Museum Technology, 2018  
Author: Warren Brown  
https://floridamuseum.ufl.edu/omt  

# About
This application is intended to run as a scheduled task on an IPT server and downloads Audubon Core data files for a given collection. The application is a tool to automate the the flow of information as Morphosources releases new data.

The date of publication from the most recent download is recorded in a log file and the application only downloads a new file if the date of publication on the RSS feed is more recent than the recorded date. The intent is to schedule the application's execution to compliment the current Morphosource publication schedule.

# Python Best Practice - Virtual Environments
Use of Python Virtual Environments is strongly encouraged and is regarded as a best practice. To quote the Python Documentation:

"Python applications will often use packages and modules that don’t come as part of the standard library. Applications will sometimes need a specific version of a library, because the application may require that a particular bug has been fixed or the application may be written using an obsolete version of the library’s interface.

This means it may not be possible for one Python installation to meet the requirements of every application. If application A needs version 1.0 of a particular module but application B needs version 2.0, then the requirements are in conflict and installing either version 1.0 or 2.0 will leave one application unable to run.

The solution for this problem is to create a virtual environment, a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages.

Different applications can then use different virtual environments. To resolve the earlier example of conflicting requirements, application A can have its own virtual environment with version 1.0 installed while application B has another virtual environment with version 2.0. If application B requires a library be upgraded to version 3.0, this will not affect application A’s environment."

https://docs.python.org/3/tutorial/venv.html

Python Virtual Environments offer an additional layer of safety in that Python is a critical part of many modern operating systems, such as Mac and Linux. Use of VENV's isolate packages and modules from the OS, thus precluding the possibility of version conflict with packages required by the operating system.

# Recommended Installation
Requires Python 3.6, which is available for all platforms. Python dependencies are containted in requirements.txt. Following the Virtual Environment best practice, typical installation on a Linux Server would be:

```bash
cd /usr/local/sbin
git clone https://github.com/FLMNH/MorphoSourceRSSDownloader.git
python3.6 -m venv MorphoSourceRSSDownload
cd MorphoSourceRSSDownload
source bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
Refer to the Usage section for instructions to test the application.

# Usage
The application is a command line tool that accepts arguments of the a collection GUID, RSS feed address, and the path to which the downloaded file should be saved.

Information on the MorphoSource RSS feed is avaialable at https://www.morphosource.org/About/report and may be used to obtain your collection's GUID.

Abstractly, usage is 
```bash
python morphosourcefeed.py COLLECTIONGUID FEEDADDRESS /PATH/TO/SAVE/FILE
```
PATH/TO/SAVE/FILE will be determined by your specific IPT server configuration and should be the "Source Data" path for your resource.

## Run Manually
Presuming installation as described in this document:
```bash
cd /usr/local/sbin/MorphoSourceRSSDownload
source bin/activate
python morphosourcefeed.py COLLECTIONGUID FEEDADDRESS /PATH/TO/SAVE/FILE
deactivate
```
### Concrete Example
For a concrete example, this translates to the following for our IPT server:
```bash 
cd /usr/local/sbin/MorphoSourceRSSDownload
source bin/activate
python morphosourcefeed.py "bd7cfd55-bf55-46fc-878d-e6e11f574ccd" "https://www.morphosource.org/rss/ms_rss" "/srv/iptdata/resources/herpetology/sources"
deactivate
```
YOUR PATH AND GUID WILL BE DIFFERENT.

## Run As Scheduled Task with CRON
The Virtual Environment introduces little change from normal cron scheduling. Simply include activating the VENV.

# Pulling it all together with IPT
To make all this magic work with IPT, do the following. Please note, order of operations here is important.
For best results, do these steps in order. Also, these instructions presume familiarity with IPT configuration and
administrative access.

1. Use morphosourcefeed.py to download the data file from the RSS feed to a temporary directory, like your user home directory.
2. Login to manage your resource in IPT and add the file you just downloaded as a data source. You will need to upload the file 
via the IPT management interface in your browser, so if you downloaded the file on the server, you will need to copy it to your
local machine first. DO NOT CHANGE THE NAME OF THE FILE. The file must be named after the GUID.
3. Record the server file path of the data source. You will need this path when scheduling morphosourcefeed.py to update the file.
4. Add an Audubon Media Description in your resource Darwin Core Mappings. Select the data source created in step 2.
5. Complete the mapping. Build and check for errors and correctness.
6. Schedule a task (probably cron) to invoke morphosourcefeed.py and update your data source using the file path from step 3.

# License
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/