from bs4 import BeautifulSoup
from csvwriter import CSVWriter
from itemcrawler import MoreInfoScraper
import time
import json
import csv
import urllib2
import sys

class YellowPageCrawler():
    """
    Scrapes all listings from a query for Yellow Pages
    """
    
    def __init__(self, query, locality, region, sleep_time=1, limit=None):
        """
        INPUT: String, String, int, int 
        OUTPUT: None
        Given a query, location query create a crawler for getting listings from YellowPages
        """
        self.starting_urls = self.get_url(query, locality, region, page=1)
        self.formats = {"print": print_funct, "csv": csv_funct, "json": json_funct}
        self.sleep_time = sleep_time
        self.limit = limit
        self.query = query
        self.locality = locality
        self.region = region

    def get_url(self, query, locality, region, page=1):
        """
        INPUT: String, String, String, int
        OUTPUT: Unicode
        TODO: implement with regex
        Combines the strings into a proper url to scrape from.
        """
        return unicode("http://www.yellowpages.com/search?search_terms=" + query + 
                "&geo_location_terms=" + locality + "%2C%20" + region + "&page="+str(page))

    def next_page_url(self, next_url):
        """
        INPUT: String
        OUTPUT: unicode
        TODO: implement with regex
        Combines the next_url from the next button onto the yellow pages url
        """
        return unicode("http://www.yellowpages.com" + next_url)

    def crawl(self, filename, format_="csv"):
        """
        INPUT: String, 
        OUTPUT: None
        Creates a generator from the spyder function and writes the results based on the format chosen
        """
        gen = self.spyder()
        funct = self.formats[format_]
        funct(filename, gen)

    def spyder(self):
        """
        INPUT: None
        OUTPUT: Generator
        Is the generator for scaped listings, each next is a dictionary
        """
        stack = [self.starting_urls]
        item_id = -1
        while(stack):
            time.sleep(self.sleep_time)
            url = stack.pop()
            print url
            lst_items, next_url = self.extract_page(url)
            if next_url is not None:
                stack.append(next_url)
            for item in lst_items:
                item_id += 1
                if self.limit is None:
                    item["id"] = item_id
                    yield item
                elif item_id < self.limit:
                    item["id"] = item_id
                    yield item

    def extract_page(self, url):
        """
        INPUT: String 
        OUTPUT: Tuple(String, String)
        Gets the list of items from the page and the next url
        """
        response = urllib2.urlopen(url)
        bs = BeautifulSoup(response)
        results_lst = bs.find_all("div", class_="search-results organic")
        if len(results_lst) is not None:
            results_pane = results_lst[0]
            result = results_pane.find_all("div", class_="result")
            lst_items = self.get_items(result)
            next_url = self.get_next_url(bs)
            response.close()
            return (lst_items, next_url)
        return None, None

    def get_items(self, results):
        """
        INPUT: String
        OUTPUT: List
        Gets the list of items, each item is a dictionary with information about it's listing
        """
        item_lst = []
        for result in results:
            item = {}
            item["name"] = self.check_for_none(result.find_all("a", class_="business-name"))
            item["street-address"] = self.check_for_none(result.find_all("span", class_="street-address"))
            locality = self.check_for_none(result.find_all("span", class_="locality"))
            if locality is not None:
                item["locality"] = locality.strip(",")
            else:
                item["locality"] = None
            item["region"] = self.check_for_none(result.find_all("span", attrs={"itemprop":"addressRegion"}))
            item["postal-code"] = self.check_for_none(result.find_all("span", attrs={"itemprop":"postalCode"}))
            item["phone-number"] = self.check_for_none(result.find_all("div", class_="phones phone primary")) 
            item["website-url"] = self.get_href(result, "a", "track-visit-website")
            item["information"] = self.get_additional_info(result, "a", "track-more-info")
            item_lst.append(item)
        return item_lst

    def get_href(self, result, name, class_name):
        web = self.check_for_none(result.find_all(name, class_=class_name), text=False) 
        if web is None:
            return None
        else:
            return web.attrs["href"]

    def get_additional_info(self, result, name, class_name):
        direct = self.get_href(result, name, class_name)
        if direct is None:
            return None
        else:
            url = self.next_page_url(self.get_href(result, name, class_name))
            mis = MoreInfoScraper(url)
            return mis.scraped_dict

    def check_for_none(self, lst, text=True):
        """
        INPUT: List
        OUTPUT: None/String
        Checks if the List is a size of more then 1 and if it is return the first element stripped.
        """
        if len(lst) is 0:
            return None
        elif text:
            return lst[0].text.strip(", ")
        else:
            return lst[0]

    def get_next_url(self,bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: None/String
        Extracts the url from the next button if there is one.  If there is no next button return None.
        """
        page = bs.find_all("div", class_="pagination")
        if len(page) == 0:
            return None
        else:
            a = page[0].find_all("a", class_="next ajax-page")
            if len(a) == 0:
                return None
            else:
                return self.next_page_url(a[0].attrs["href"])    

def json_funct(filename, generator, file_size=30):
    """
    INPUT: String, Generator
    OUTPUT: None
    This function writes the items into a json file, I chose to write multiple files of the scraped data
    inorder to not load all of the data into memory.
    """
    item_dict = {}
    file_count = 1

    for item in generator:
        item_dict[item['id']] = item
        if len(item_dict) is file_size:
            json_name = filename + str(file_count) + ".json"
            json.dump(item_dict, open(json_name, 'w'))
            file_count += 1
            item_dict = {}

    if len(item_dict) < file_size:
        json_name = filename + str(file_count) + ".json"
        json.dump(item_dict, open(json_name, 'w'))


def print_funct(filename, generator):
    """
    INPUT: String, Generator
    OUTPUT: None
    """
    for item in generator:
        print item 

def csv_funct(filename, generator):
    """
    INPUT: String, Generator
    OUTPUT: None
    """
    with open(filename+'.csv', 'w') as csvfile:
        fieldnames = ['id', 'name', 'street-address', 'locality', 'region', 'postal-code', 'phone-number']
        writer = CSVWriter(csvfile, fieldnames)
        writer.write_header()
        for item in generator:
            writer.write_row(item)    
        
def cardv(filename, generator):
    """
    INPUT: String, Generator
    OUTPUT: None
    Writes in cardv format the data from the generator to a file with the filename.
    """
    pass

def main(query, locality, regio, form="json"):
    """
    Initializes query, locality (city), region (state)
    file name is based on query-locality-region.format
    """
    ypc = YellowPageCrawler(query, locality, region)
    filename = query+"-"+locality+"-"+region
    ypc.crawl(filename, format_=form)
    print "Crawling completed for: ",filename

if __name__ == '__main__':
    query = sys.argv[1]
    locality = sys.argv[2]
    region = sys.argv[3]
    main(query, locality, region)