# Aurik Sarker
# 16 October 2023

# This module will attempt to take in input arguments from the command line
# It compartmentalizes parts of the code into functions
#   Parse user input 
#     In this script, they are command line arguments
#     but they will be changed to work with a discord bot later

#%% Imports
# from sys import argv
from argparse import ArgumentParser
import re
from json import dumps
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

def main(args=None):
    # For debugging purposes, the user may pass in a dictionary
    if args is None:
        # Otherwise, pass in command line arguments
        args = parse_args()
    
    print(args)
    chrome_args = ["--headless"]

    url = parse_input(args)
    soup = get_html(url, chrome_args)
    if not verify_html(soup):
        print('Something happened')
    # This is a list of rankings
    info = parse_html(soup, args)

    for i, ranking in enumerate(info):
        print('Ranking player %d of %d:' % (i+1, len(info)))
        print('URL: %s' % url)
        print( dumps(ranking, indent=4) )

    return info


#%%
def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-u", "--user", help="Input your user name. If none is entered, a ranking of five users is displayed instead")
    parser.add_argument("-r", "--ranking", help="Type of ranking to display. (Default=Overall)")
    parser.add_argument("-t", "--ranking-type", help="Further specify the ranking to display. This is dependent on the ranking selected using -r (e.g. -r world -t elysium)")
    parser.add_argument("--region", help="Specify between North America and Europe {na, eu}. (Default=na)")
    parser.add_argument("--reboot", help="Specify {reboot, nonreboot, both} (Default=both)")
    parser.add_argument("-i", "--index", type=int, help="Displays the top five players beginning from the rank specified. (Default=1)")
    args = parser.parse_args()
    # Return a dictionary instead of a Namespace
    #   this plays well with python subscripting
    return vars(args)


#%%
def parse_input(args):
    """
    Parse the command line arguments
    Return a valid URL to ping Nexon for the rankings
    """
    if not args['user'] and not args['index']:
        print("Both user and index were entered. The user ranking will be displayed")

    # Defaults
    if not args['ranking']:
        args['ranking'] = "overall-ranking"
    if not args['ranking_type']:
        # TODO the default value should be different based on the ranking specified
        args['ranking_type'] = "legendary"
    if not args['region']:
        args['region'] = "na"
    if not args['reboot']:
        args['reboot'] = "both"
    if not args['index']:
        args['index'] = 1

    # TODO add function here to parse the inputs even further
    # Should be some conversion between human-readable and direct input to URL
    #   e.g. reboot = both -> 2
    #   e.g. ranking type = reboot na -> reboot-(na)
    # It should also handle the different possible ranking types
    
    if args['reboot'] == "reboot":
        reboot = 1
    if args['reboot'] == "notreboot":
        reboot = 2
    else:
        reboot = 0
    
    # Convert the input args into strings to append to the end of the URL
    search_arg = region_arg = ''

    # If a user was specified, then prioritize searching for that user
    if args['user']:
        search_arg = "character_name=%s" % args['user']
    else:
        search_arg = "page_index=%d" % args['index']
    
    # The other args are appended to the search arg, so prepend a '&'
    reboot_arg = "&rebootIndex=%s" % reboot

    if args['region'] != 'na':
        # Legion rankings dont work if the region is given
        if args['ranking'] != "legion":
            region_arg = "&region=%s" % args['region']
    
    url_nexon = URL_BASE + "%s/%s/?%s%s%s" %\
        (args['ranking'], args['ranking_type'], search_arg, reboot_arg, region_arg)
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
    # Use other options to reduce startup time
    chrome_args.append("--ignore-certificate-errors")
    chrome_args.append("--disable-css")
    chrome_args.append("--disable-extensions")
    chrome_args.append("--disable-gpu")
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
# FOR DEBUGGING
def parse_html_(soup):
    table_rows_all = soup.find_all(class_="c-rank-list__table-row")
    
    # Get the table header
    table_headers = [cell.get_text() for cell in table_rows_all[0].find_all(class_="c-rank-list__table-cell-text")]
    table_rows = table_rows_all[1:]

    cells = []
    # Parse each row in the table separately
    #   Each row typically corresponds to a different character
    for row in table_rows:
        table_cells = row.find_all(class_="c-rank-list__table-cell-text")
        cells.append( table_cells )

    return table_headers, cells

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
    # Parse each row in the table separately
    #   Each row typically corresponds to a different character
    for row in table_rows:
        table_cells = row.find_all(class_="c-rank-list__table-cell-text")
        rankings.append( parse_rows(table_headers, table_cells) )

    return rankings



#%%
def parse_rows(table_headers, table_cells):
    # First, let's check that we have the same number of headers as cells
    if len(table_headers) != len(table_cells):
        print("Something happend")

    # Generate dictionary containing the rank information for this character
    ranking = {}
    # Loop through the cells found and process each individually then storing into the ranking dictionary
    for header, cell in zip(table_headers, table_cells):
        header_name, cell_value = parse_cell(header, cell)
        ranking[header_name] = cell_value
    
    return ranking


#%%

def parse_cell(header, cell):
    # This is the key name which will be passed to the parent function
    # By default, it is the same as the header parsed from the html, 
    #   but it may be changed below 
    header_name = header

    if header == "Rank":
        cell_value = cell.get_text()
        # If the rank was not found, it may have been an image 
        #   (literal image of a 1st/2nd/3rd place medal)
        if not cell_value:
            # Find the <img> element within the Tag, then get its source
            rank_img = cell.find('img').get('src')
            # Look for the medalX.png part
            rank_medal_regex = re.search(r'medal\d\.png', rank_img)
            if rank_medal_regex:
                rank_medal = rank_medal_regex.group()
                cell_value = rank_medal[5:6]
            else:
                cell_value = None


    elif header == "Character":
        header_name = "Character Img"
        cell_value = cell.find("img")["src"]
    elif header == "Character Name":
        cell_value = cell.get_text()
    elif header == "World":
        cell_value = cell.find("a")["class"][1]
    elif header == "Job":
        cell_value = cell.find("img")["title"]
    elif header == "Exp Gained":
        cell_value = cell.get_text()
    elif header == "Level/Move": 
        # This div contains three elements, as well as a class indicating rank up/down/draw
        text_elements = [elem.get_text() for elem in cell.find_all(string=True)]
        rank_dir = cell.find('div').get('class')[0]

        # Handle neutral case
        if text_elements[2] == "-": 
            text_elements[2] = '0'

        # Parse the rank direction
        # Remove redundant "rank" text
        rank_dir = rank_dir.replace("rank-", "")

        cell_value = {}
        cell_value["Level"] = text_elements[0]
        # Only experience gained during this level
        cell_value["Level Exp"] = text_elements[1]
        cell_value["Rank Change"] = text_elements[2]
        cell_value["Rank Direction"] = rank_dir

    elif header == "Tier":
        cell_value = cell.get_text()
        # If the rank was not found, it may have been an image 
        #   (literal image of a 1st/2nd/3rd place medal)
        if not cell_value:
            # Find the <img> element within the Tag, then get its source
            tier_img = cell.find('img').get('src')
            # Look for the medalX.png part
            tier_medal_regex = re.search(r'tier\/.+\.png', tier_img)
            if tier_medal_regex:
                tier_medal = tier_medal_regex.group()
                cell_value = tier_medal[5:-4]
            else:
                cell_value = None
    elif header == "Score":
        cell_value = cell.get_text()

    elif header == "Fame Gained":
        cell_value = cell.get_text()
    elif header == "Total Fame":
        cell_value = cell.get_text()

    elif header == "Legion Level":
        cell_value = cell.get_text()
    elif header == "Raid Power":
        cell_value = cell.get_text()

    elif header == "Stars/Stage/Time": 
        # Extract the text, exclude the <br/> Tags
        text_elements = [item for item in cell.contents if isinstance(item, str)]

        cell_value = {}
        cell_value["Stars"] = text_elements[0]
        # Only experience gained during this level
        cell_value["Stage"] = text_elements[1]
        cell_value["Time"] = text_elements[2]

    else: 
        print("Invalid header: %s" % header)
        cell_value = cell
    return header_name, cell_value

# %%
if __name__ == "__main__":
    main()
# %%
