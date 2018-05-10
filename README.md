# MorphoSourceRSSDownloader
MorphoSource RSS Downloader
Florida Museum of Natural History  
Office of Museum Technology, 2018  
Author: Warren Brown  
https://floridamuseum.ufl.edu/omt  

# About
This application is intended to run as a scheduled task, such as a cron job, and downloads Audubon Core data files for a given collection. The application is a tool to automate the the flow of information as Morphosources releases new data.

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


# License
This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
https://creativecommons.org/licenses/by-nc-sa/4.0/