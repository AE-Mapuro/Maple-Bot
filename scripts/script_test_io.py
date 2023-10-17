# Aurik Sarker
# 16 October 2023

# This script allows us to parse a url and load the html using functions in module_test_io
# This way we can load in the html once and perform testing ad hoc

#%%
import module_test_io
import re
# from bs4 import BeautifulSoup


#%%
def get_html(args):
    url = module_test_io.parse_input(args)
    html = module_test_io.get_html(url)
    assert( module_test_io.verify_html(html) )
    info = module_test_io.parse_html(html, args)
    print(info) 

    return (url, html)

#%%
args = []

users = ['Doop70', 'Niru', 'ImHeroic']
users = ['Ender90']

for user in users:
    args_ = {}

    # args_['user'] = None
    args_['user'] = user
    
    args_['ranking'] = 'overall-ranking'
    args_['ranking_type'] = 'legendary'
    args_['region'] = None
    args_['reboot'] = None
    args_['index'] = None
    
    args.append(args_)

# args_ = args[1]

#%%
htmls = []
for i, args_ in enumerate(args):
    print('Processing Dataset %d of %d' % (i+1, len(args)))
    htmls.append( get_html(args_) )
print('Completed')

#%%
html = htmls[0][1]
# html = htmls[1][1]
# html = htmls[2][1]

# %%
# Find all table rows
# There should only be two: the table column names and the character data
table_rows = html.find_all(class_="c-rank-list__table-row")
# if len(table_rows) != 2:
#     print("Something happend")

# Get the table header
table_headers = [cell.get_text() for cell in table_rows[0].find_all(class_="c-rank-list__table-cell-text")]
table_cells = table_rows[1].find_all(class_="c-rank-list__table-cell-text")

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

ranking


#%%

tag = cell
# text_elements = [element.get_text() for element in tag.find_all(string=True, recursive=True)]
text_elements = [element.get_text() for element in cell.find_all(string=True)]

# Level, Exp, Rank Change, Rank Direction (rank-up, rank-down, rank-draw)

# Get the class attribute of the inner div (if present)
inner_class = cell.find('div').get('class')[0]

print("Text Elements:", text_elements)
print("Inner Div Class:", inner_class)




#%%
# Test timing of the headless chrome browser
# Try different startup options
raise
chrome_args_list = [
    [], 
    ["--disable-gpu"], 
    ["--ignore-certificate-errors"], 
    ["--no-sandbox"], 
    ["--disable-dev-shm-usage"], 
    ["--disable-extensions"], 
    ["--disable-images"], 
    ["--disable-css"]
]

chrome_args = chrome_args_list[0]
# These options may or may not help speed this process up
html = module_test_io.get_html(url, chrome_args)


#%%