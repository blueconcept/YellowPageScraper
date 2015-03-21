# Yellow Pages Webcrawler

The yellow pages webcrawler uses a combintion of urllib and bs4 to scrape the listings from queries.  In order to scrape all listings the crawler scrapes in a DFS pattern using a stack and using the pagination's next button (although only 1 page is in the stack at a time).  If there is no next button, then it's determined that the last page is found and the crawler will end the crawl.  A generator is used to avoid storing all of the listings into memory.  

I have only implemented csv formating and an option for printing to console.  The empty functions serve to show how I could implement the different formats.  For csv formating I made my own csv writer because the Python built in csv dictionary writer adds an extra line for some reason.     

### Version
1.0.0 - 3/20/2015

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