# Aurik Sarker
# 16 October 2023

# This module will attempt to take in input arguments from the command line
# It compartmentalizes parts of the code into functions
#   Parse user input 
#     In this script, they are command line arguments
#     but they will be changed to work with a discord bot later

#%% Imports
from sys import argv
from argparse import ArgumentParser
import re
import warnings

# Selenium throws a warning: 
#   NotOpenSSLWarning: urllib3 v2.0 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. 
#   See: https://github.com/urllib3/urllib3/issues/3020
# So first, ignore all warnings
warnings.simplefilter("ignore")

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

warnings.resetwarnings()


#%% Globals
URL_BASE = R"https://maplestory.nexon.net/rankings/"

# For testing the output html
# This should always be in the output html text
TEST_STR_1= "Rankings"
# This indicates if the javascript ran
# TODO figure what is in the javascript run but not the original HTML
TEST_STR_2 = TEST_STR_1

def main():
    # print(argv)

    parser = ArgumentParser()
    parser.add_argument("-u", "--user", help="Input your user name. If none is entered, a ranking of five users is displayed instead")
    parser.add_argument("-r", "--ranking", help="Type of ranking to display. (Default=Overall)")
    parser.add_argument("-t", "--ranking-type", help="Further specify the ranking to display. This is dependent on the ranking selected using -r (e.g. -r world -t elysium)")
    parser.add_argument("--region", help="Specify between North America and Europe {na, eu}. (Default=na)")
    parser.add_argument("--reboot", help="Specify {reboot, nonreboot, both} (Default=both)")
    parser.add_argument("-i", "--index", type=int, help="Displays the top five players beginning from the rank specified. (Default=1)")
    args = parser.parse_args()

    print(args)

    chrome_args = []
    # These options may or may not help speed this process up
    # chrome_args.append("--disable-gpu")
    # chrome_args.append("--ignore-certificate-errors")
    # chrome_args.append("--no-sandbox")
    # chrome_args.append("--disable-dev-shm-usage")
    # chrome_args.append("--disable-extensions")
    # chrome_args.append("--disable-images")
    # chrome_args.append("--disable-css")

    url = parse_input(args)
    soup = get_html(url, chrome_args)
    if not verify_html(soup):
        print('Something happend')
    info = parse_html(soup, args)
    
    return 0


#%%
def parse_input(args):
    """
    Parse the command line arguments
    Return a valid URL to ping Nexon for the rankings
    """
    if args['user'] is not None and args['index'] is not None:
        print("Both user and index were entered. The user ranking will be displayed")
    
    # Defaults
    if args['ranking'] is None:
        args['ranking'] = "overall-ranking"
    if args['ranking_type'] is None:
        # TODO the default value should be different based on the ranking specified
        args['ranking_type'] = "legendary"
    if args['region'] is None:
        args['region'] = "na"
    if args['reboot'] is None:
        args['reboot'] = "both"
    if args['index'] is None:
        args['index'] = 1

    # TODO add function here to parse the inputs even further
    # Should be some conversion between human-readable and direct input to URL
    #   e.g. reboot = both -> 2
    #   e.g. ranking type = reboot na -> reboot-(na)
    # It should also handle the different possible ranking types

    if args['reboot'] == "reboot":
        reboot = 1
    if args['reboot'] == "notreboot":
        reboot = 0
    else:
        reboot = 2

    if args['user'] is None:
        user_arg = ''
        index_arg = "&page_index=%d" % args['index']
    else:
        user_arg = "&character_name=%s" % args['user']
        index_arg = ''
    
    
    url_nexon = URL_BASE + "%s/%s/?region=%s&rebootIndex=%s%s%s" %\
        (args['ranking'], args['ranking_type'], args['region'], reboot, user_arg, index_arg)
    return url_nexon
    



#%%
def get_html(url, chrome_args=[]):
    """
    Retrieve the html corresponding to the given url, converted to BeautifulSoup.
    A headless chrome browser is used in order for javascript to run and generate the actual site
    
    Parameters
    ----------
    url : str
        The url to retrieve the html from.
    chrome_args : list, optional
        A list of arguments to pass to the chrome driver.
    
    Returns
    -------
    html: BeautifulSoup
        The html retrieved from the url.
    
    """
    chrome_options = Options()

    # Make sure the browser is headless
    chrome_args.append("--headless")
    for arg in chrome_args:
        chrome_options.add_argument(arg)

    # Create a headless browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source.encode("utf-8"), 'html.parser')
    driver.quit()

    return soup




#%%
def verify_html(soup):
    """
    Verify that the html retrieved from the url is valid.
    The html should contain the string "Rankings"
    If the Javascript ran correctly (using the headless browser), the character name should also be found
    """
    if TEST_STR_1 not in soup.get_text():
        print("HTML test failed")
        return False
    if TEST_STR_2 not in soup.get_text():
        print("Selenium test failed")
        return False
    
    return True



#%%
def parse_html(soup, args):
    # Find all table rows
    # There should only be two: the table column names and the character data
    table_rows_all = soup.find_all(class_="c-rank-list__table-row")
    
    # If a user was passed in args (not None), then only one row is expected (besides header)
    # If not, then five rows are expected
    # TODO perform some check for this ^^ (look in args)

    # Get the table header
    table_headers = [cell.get_text() for cell in table_rows_all[0].find_all(class_="c-rank-list__table-cell-text")]
    table_rows = table_rows_all[1:]

    rankings = []
    for row in table_rows:
        table_cells = table_rows[0].find_all(class_="c-rank-list__table-cell-text")
        rankings.append( parse_rows(table_headers, table_cells) )

    return rankings

def parse_rows(table_headers, table_cells):
    # First, let's check that we have the same number of headers as cells
    if len(table_headers) != len(table_cells):
        print("Something happend")

    # Generate dictionary containing the rank information for this character
    ranking = {}
    # value: str
    # Next, let's loop through the headers and print corresponding output from the cells based on each header
    for header, cell in zip(table_headers, table_cells):
        header_name = header

        if header == "Rank":
            value = cell.get_text()
            # If the rank was not found, it may have been an image 
            #   (literal image of a 1st/2nd/3rd place medal)
            if not value:
                # Find the <img> element within the Tag, then get its source
                rank_img = cell.find('img').get('src')
                # Look for the medalX.png part
                rank_medal_regex = re.search(r'medal\d\.png', rank_img)
                if rank_medal_regex:
                    rank_medal = rank_medal_regex.group()
                    value = rank_medal[5:6]
                else:
                    value = ''
        
        
        elif header == "Character":
            header_name = "Character Img"
            value = cell.find("img")["src"]
        elif header == "Character Name":
            value = cell.get_text()
        elif header == "World":
            value = cell.find("a")["class"][1]
        elif header == "Job":
            value = cell.find("img")["title"]
        elif header == "Exp Gained":
            value = cell.get_text()
        elif header == "Level/Move": 
            value = {}
            # This div contains three elements, as well as a class indicating rank up/down/draw
            text_elements = [elem.get_text() for elem in cell.find_all(string=True)]
            rank_dir = cell.find('div').get('class')[0]

            # Handle neutral case
            if text_elements[2] == "-": 
                text_elements[2] = '0'

            # Parse the rank direction
            # Remove redundant "rank" text
            rank_dir = rank_dir.replace("rank-", "")

            value["Level"] = text_elements[0]
            # Only experience gained during this level
            value["Level Exp"] = text_elements[1]
            value["Rank Change"] = text_elements[2]
            value["Rank Direction"] = rank_dir

        else: 
            print("Invalid header: %s" % header)
            value = cell

        ranking[header_name] = value



# %%
if __name__ == "__main__":
    main()
# %%
