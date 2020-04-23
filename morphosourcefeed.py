# Florida Museum of Natural History
# Office of Museum Technology, 2018
# Author: Warren Brown
# Morphopsource RSS Feed Downloader
# https://github.com/FLMNH/MorphoSourceRSSDownloader
# https://floridamuseum.ufl.edu/omt
# This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# https://creativecommons.org/licenses/by-nc-sa/4.0/


import feedparser, os, sys, urllib, datetime, shutil, zipfile

def check_log_file(collection_guid):
    """Checks for log file. If not found, creates one with backdated timestamp."""
    if os.path.isfile('{}.log'.format(collection_guid)):
        if os.access('{}.log'.format(collection_guid), os.R_OK):
            return True
        else:
            exit("Error! Unable to access log file {}.log".format(collection_guid))
    else:
        back_date = datetime.datetime.now() - datetime.timedelta(days=45)
        write_pub_date(collection_guid, back_date)
    return True

def read_pub_date(collection_guid):
    """Returns datetime object of the last pub date for given collection."""
    try:
        with open('{}.log'.format(collection_guid),'r') as f:
            return datetime.datetime.strptime(f.read(), "%Y-%m-%d %H:%M:%S.%f")
    except:
        sys.exit('Error! Unable to read {}.log.'.format(collection_guid))

def write_pub_date(collection_guid,pub_date):
    """Writes publication date to lastpubdate.log."""
    try:
        with open('{}.log'.format(collection_guid),'w') as f:
            f.write(datetime.datetime.strftime(pub_date, "%Y-%m-%d %H:%M:%S.%f"))
        #f.closed()
    except:
        sys.exit('Error! Unable to write {}.log'.format(collection_guid))

def check_if_new(collection_guid,pub_date):
    """Returns True if given pub date is newer than recorded."""
    return pub_date > read_pub_date(collection_guid)

def get_new_morphosource_file(link, collection_guid, file_path):
    """Downloads new Morphosource file."""
    return urllib.request.urlretrieve(link, "{}/{}.txt".format(file_path,collection_guid))

def get_new_specify_file(link, collection_guid, file_path):
    '''Downloads new Specify7 dwca and extracts, renames audubon core'''
    temp_dir = '{}_{}'.format('tmp', collection_guid)
    os.mkdir(temp_dir)
    archive, headers = urllib.request.urlretrieve(link, '{}/{}.zip'.format(temp_dir, collection_guid))
    with zipfile.ZipFile(archive) as archive_zip:
        with archive_zip.open('multimedia.txt') as audubon_file:
            with open('{}/{}.txt'.format(file_path, collection_guid), 'w') as outfile:
                for line in audubon_file:
                    outfile.write(line.decode())
    shutil.rmtree(temp_dir)



def main(argv):
    if len(argv) == 4:
        collection_guid = argv[1]
        if check_log_file(collection_guid):
            file_path = argv[3]
            feed_address = argv[2]
            article_exists = False
            link = None
            published_at = None
            feed = feedparser.parse(feed_address)
            feed_title = feed['feed']['title']
            feed_entries = feed.entries

            for i,entry in enumerate(feed.entries):
                # Morphosource feed or Specify7 feed
                morphosource_feed = "Audubon Core format" in entry.title and collection_guid in entry.title
                specify_feed = 'specify.floridamuseum.ufl.edu' in feed_address and collection_guid in entry.id
                if morphosource_feed or specify_feed:
                    link = entry.link
                    published_at = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
                    article_exists = True

            if article_exists:
                if check_if_new(collection_guid, published_at):
                    if morphosource_feed:
                        get_new_morphosource_file(link, collection_guid, file_path)
                    if specify_feed:
                        get_new_specify_file(link, collection_guid, file_path)
                    write_pub_date(collection_guid, published_at)
                    print("Update downloaded to {}/{}.txt".format(file_path,collection_guid))
                else:
                    print("No update.")
            else:
                print("{} does not exist in {}.".format(collection_guid, feed_address))
    else:
        print("\n\tUsage: python morphosourcefeed.py COLLECTIONGUID FEEDADDRESS /PATH/TO/SAVE/FILE")
        print("\n\tRequires Python 3.6.")
    return

if __name__ == "__main__":
    main(sys.argv)

