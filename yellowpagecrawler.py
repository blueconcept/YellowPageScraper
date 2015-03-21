from bs4 import BeautifulSoup
import time
import json
import csv
import urllib2

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
        self.formats = {"print": print_funct, "csv": csv_funct}
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
            if next_url != None:
                stack.append(next_url)
            for item in lst_items:
                item_id += 1
                if self.limit == None:
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
        #response = requests.get(url) GIVES UNICODE fail equals warning
        response = urllib2.urlopen(url)
        bs = BeautifulSoup(txt)
        results_pane = bs.find_all("div", class_="search-results organic")[0]
        result = results_pane.find_all("div", class_="result")
        lst_items = self.get_items(result)
        next_url = self.get_next_url(bs)
        return (lst_items, next_url)

    def get_items(self, results):
        """
        INPUT: String
        OUTPUT: List
        Gets the list of items, each item is a dictionary with information about it's listing
        """
        item_lst = []
        for result in results:
            item = {}
            item["name"] = result.find_all("a", class_="business-name")[0].text
            item["street-address"] = self.check_for_none(result.find_all("span", class_="street-address"))
            locality = self.check_for_none(result.find_all("span", class_="locality"))
            if locality != None:
                item["locality"] = locality.strip(",")
            else:
                item["locality"] = None
            item["region"] = self.check_for_none(result.find_all("span", attrs={"itemprop":"addressRegion"}))
            item["postal-code"] = self.check_for_none(result.find_all("span", attrs={"itemprop":"postalCode"}))
            item["phone-number"] = self.check_for_none(result.find_all("div", class_="phones phone primary"))
            item_lst.append(item)
        return item_lst
    
    def check_for_none(self, lst):
        """
        INPUT: List
        OUTPUT: None/String
        Checks if the List is a size of more then 1 and if it is return the first element stripped.
        """
        if len(lst) == 0:
            return None
        else:
            return lst[0].text.strip(", ")

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

def json_funct(filename, generator):
    """
    INPUT: String, Generator
    OUTPUT: None
    """
    pass

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

class CSVWriter():
    """
    Custom Writer for CSV because the Python built-in one kept giving me extra spaces
    """
    
    
    def __init__(self, csv_file, fieldnames, fillnone="NA"):
        """
        INPUT: file, String, String
        OUTPUT: None
        Iinitializes CSVWriter
        """
        self.csv_file = csv_file
        self.fieldnames = fieldnames
        self.fillnone = fillnone
    
    def write_header(self):
        """
        INPUT: None
        OUTPUT: None
        Writes the headers for the csv file
        """
        for i,name in enumerate(self.fieldnames):
            self.csv_file.write(name)
            if i < len(self.fieldnames)-1:
                self.csv_file.write(",")
        self.csv_file.write("\n")

    def write_row(self, item_dict):
        """
        INPUT: Dictionary
        OUTPUT: None
        Writes the row based on the item_dict with the order from the fieldnames list
        """
        for i,item in enumerate(self.fieldnames):
            if item_dict[item] == None:
                self.csv_file.write(self.fillnone)
            else:
                self.csv_file.write(unicode(item_dict[item]))
            if i < len(self.fieldnames)-1:
                self.csv_file.write(",")
        self.csv_file.write("\n")
        
def cardv(filename, generator):
    """
    INPUT: String, Generator
    OUTPUT: None
    Writes in cardv format the data from the generator to a file with the filename.
    """
    pass

def main():
    """
    Initializes query, locality (city), region (state)
    file name is based on query-locality-region.format
    """
    query = "cupcakes"
    locality = "Tucson"
    region = "AZ"
    ypc = YellowPageCrawler(query, locality, region)
    filename = query+"-"+locality+"-"+region
    ypc.crawl(filename)
    print "Crawling completed for: ",filename

if __name__ == '__main__':
    main()