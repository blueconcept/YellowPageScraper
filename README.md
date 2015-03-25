# Yellow Pages Webcrawler

The yellow pages webcrawler uses a combintion of urllib and bs4 to scrape the listings from queries.  In order to scrape all listings the crawler scrapes in a DFS pattern using a stack and using the pagination's next button (although only 1 page is in the stack at a time).  If there is no next button, then it's determined that the last page is found and the crawler will end the crawl.  A generator is used to avoid storing all of the listings into memory.  

I have only implemented csv formating and an option for printing to console.  The empty functions serve to show how I could implement the different formats.  For csv formating I made my own csv writer because the Python built in csv dictionary writer adds an extra line for some reason.

An obstacle I ran into is that not all listings have all of it's associated information like street address and locality.  To go around this, I return None if that information is not found and write "NA" for the csv file for any values of None which could be changed in the future.  A lot of the strings are wrapped into unicode although probably not necessary, I used it to prevent the equals comparision of strings failure, a warning which came up associated with the starting url.

### Version
1.0.0 - 3/20/2015

This current version only supports either printing to console or writing to csv.

### Imports

This program requires only bs4 and urllib 

### How to Use YellowPagesCrawler
The query is what you are searching for and the locality + region determines where you are searching (geographical area).  For the United States, this is usually, the city for locality and region state.

You initialize an instance of the crawler and call the crawl function with a filename (without an extension).  

### Example from Code

    query = "cupcakes"
    locality = "Tucson"
    region = "AZ"
    ypc = YellowPageCrawler(query, locality, region)
    filename = query+"-"+locality+"-"+region
    ypc.crawl(filename)
    print "Crawling completed for: ",filename

### FeedBack

changed write_row of csv writer to have a sep parameter optional default to , but could be anything else

---You should use a built-in csv writer whenever possible, but also be aware of the risks of the csv format (namely, naturally-occurring commas in the values of a record). JSON would probably be a better choice for storage of web-scraped records so that you don't need to worry about commas. 

To deal with this issue I changed the default format to json and to prevent the entire scraped data to be in-memory at the same time I dumped the json files in increments of 30 items each which can be changed.

-Make sure to get all of the fields of information about a business, including website, categories, and any detail-link information (email, hours, lat+lon, etc.)

This doesn't sound like a hard change but it will take some time I'll make the changes later tonight and ping again about the changes.

---When checking equality of None objects in python, use `x is None` or `x is not None` instead of `x == None`
Okay I made the changes and started to change some other == comparision as well.

---extract_page() has some issues: 'response' is unused (and left unclosed) and 'txt' is undefined.

Simple fix, I don't know why the function was in the state it was in.  I may have been fiddling around and pushed it without thinking.
 
---When using find_all (or any scraping method that returns a list), make sure to check that the list of results actually contains values before slicing from it. Generally, the uncertainty inherent to any webscraping script requires particularly robust code. The main() method should take in its parameters rather than have them encoded locally. Perhaps input parameters via the command line?

I applied all fields to the None check function to return none if the lst is empty.

-It would be nice to have flexibility in specifying the parameters of the scrape, rather than having them encoded in get_items(). The less specific information is hard-coded in the scraper, the more extensible and flexible it is. 

I thought about this too but given that to get a field of data I would have to hard code the scraping (ie getting the correct web component) it would be difficult to avoid doing so.
But to implement this I could have a set of fields to be scraping from and a dictionary to point to the functions for scraping.  

-Try to use "itemprop" for other fields too, if possible.


-get_url does not allow one to query for terms that aren't URL safe.
I don't understand the context for this question.  Is alluding that I should make a more proper request?