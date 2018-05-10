import feedparser, os, sys, urllib, datetime

#Config Variables
# Morphosource used the iDigBio GUID
#collection_guid = "bd7cfd55-bf55-46fc-878d-e6e11f574ccd"
#feed_address = "https://www.morphosource.org/rss/ms.rss"

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

def get_new_file(link, collection_guid, file_path):
    """Downloads the new file."""
    return urllib.request.urlretrieve(link, "{}/{}.csv".format(file_path,collection_guid))
    
def main(argv):
    if len(argv) == 4:
        collection_guid = argv[1]
        if check_log_file(collection_guid):
            file_path = argv[3]
            article_title = "MorphoSource media, Audubon Core format for recordset {}".format(collection_guid)
            feed_address = argv[2]
            article_exists = False
            link = None
            published_at = None
            feed = feedparser.parse(feed_address)
            feed_title = feed['feed']['title']
            feed_entries = feed.entries

            for i,entry in enumerate(feed.entries):
                if article_title == entry.title:
                    link = entry.link
                    published_at = datetime.datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z').replace(tzinfo=None)
                    article_exists = True

            if article_exists:
                if check_if_new(collection_guid, published_at):
                    get_new_file(link, collection_guid, file_path)
                    write_pub_date(collection_guid, published_at)
                    print("Update downloaded to {}/{}.csv".format(file_path,collection_guid))
                else:
                    print("No update.")
            else:
                print("{} does not exist in {}.".format(article_title, feed_address))

            # pub_datetime_object = datetime.strptime(feed.entries[0]["published"], '%a, %d %b %Y %H:%M:%S %z')
    else:
        print("\n\tUsage: python3 morphosourcefeed.py COLLECTIONGUID FEEDADDRESS /PATH/TO/SAVE/FILE")
    return

if __name__ == "__main__":
    main(sys.argv)

