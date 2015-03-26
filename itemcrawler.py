from bs4 import BeautifulSoup
import urllib2

class MoreInfoScraper():
    """
    Crawls the url for 1 item and getting the prospective information set in data_field_set
    """
    
    def __init__(self, url, data_field_set={"hours", "general-info", "payment-method", "location", "neightborhood", "aka", "categories"}):
        """
        INPUT: String, Set
        OUTPUT: None
        Initializes MoreInfoScraper, if data_field_set is None then just set it to a default value
        """
        self.data_field_set = data_field_set
        self.url = url
        self.scraped_dict = self.get_dict(urllib2.urlopen(url))
        
    def get_dict(self, response):
        """
        INPUT: BeautifulSoup
        OUTPUT: Dictionary
        Creates the dictionary and for the information check to see if that information is needed with data_field_set
        """
        scraped_dict = {}
        bs = BeautifulSoup(response)
        if "hours" in self.data_field_set:
            scraped_dict["hours"] = self.get_hours(bs)
        if "general-info" in self.data_field_set:
            scraped_dict["general-info"] = self.get_general_info(bs)
        if "payment-method" in self.data_field_set:
            scraped_dict["payment-method"] = self.get_payment_method(bs)
        if "location" in self.data_field_set:
            scraped_dict["location"] = self.get_location(bs)
        if "neighborhood" in self.data_field_set:
            scraped_dict["neighborhood"] = self.get_neightborhood(bs)
        if "aka" in self.data_field_set:
            scraped_dict["aka"] = self.get_aka(bs)
        if "categories" in self.data_field_set:
            scraped_dict["categories"] = self.get_categories(bs)
        response.close()
        return scraped_dict
    
    def check_for_none(self, lst):
        """
        INPUT: List
        OUTPUT: None or BeautifulSoup
        Checks if the List is empty or not and returns None if it is empty otherwise returns the first element
        """
        if len(lst) is 0:
            return None
        else:
            return lst[0]
    
    def get_text(self, bs, name, class_name, split=False):
        """
        INPUT: BeautifulSoup, String, String
        OUTPUT: String
        Returns the text if the bs returned isn't None
        """

        description = self.check_for_none(bs.find_all(name, class_=class_name))
        if description is None:
            return None
        elif split:
            return description.text.split()
        else:
            return description.text

    def get_hours(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: String
        
        """
        times = {}
        hours = self.check_for_none(bs.find_all("div", class_="open-details"))
        if hours is not None:
            for time_comp in hours.find_all("time"):
                days_times = time_comp.attrs["datetime"].split()
                if len(days_times) is 2:
                    times[days_times[0]] = days_times[1]
            if len(times) is 0:
                return None
            return times
        return None
    
    def get_general_info(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: String
        
        """

        return self.get_text(bs, "dd", "description")
    
    def get_payment_method(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: List
        
        """
        return self.get_text(bs, "dd", "payment", split=True)
    
    def get_location(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: String
        
        """
        return self.get_text(bs, "dd", "location-description")
    
    def get_neightborhood(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: List
        
        """
        return self.get_text(bs, "dd", "neightborhoods", split=True)

    def get_aka(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: String
        
        """
        return self.get_text(bs, "dd", "aka")
    
    def get_categories(self, bs):
        """
        INPUT: BeautifulSoup
        OUTPUT: List
        
        """
        return self.get_text(bs, "dd", "categories", split=True)