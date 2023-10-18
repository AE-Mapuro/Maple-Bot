# Aurik Sarker
# 16 October 2023

# This script allows us to parse a url and load the html using functions in module_test_io
# This way we can load in the html once and perform testing ad hoc

#%%
import module_test_io
import re
import json
# from bs4 import BeautifulSoup


#%%
def get_html_(args):
    url = module_test_io.parse_input(args)
    html = module_test_io.get_html(url)
    print(url)
    assert( module_test_io.verify_html(html) )

    # For debugging
    headers, cells = module_test_io.parse_html_(html)
    # print(info)

    return (url, headers, cells)


#%%
args_empty = {}
args_empty['user'] = ''
args_empty['ranking'] = 'overall-ranking'
args_empty['ranking_type'] = 'legendary'
args_empty['region'] = ''
args_empty['reboot'] = ''
args_empty['index'] = ''

args = []

# Generate different sets of args
args_ = args_empty.copy()
args_['user'] = 'Doop70'
# Append to full list of args to pass through
# The next section will yield multiple output tables (parsed from html)
args.append(args_)

args_ = args_empty.copy()
args_['index'] = 1232
# Append to full list of args to pass through
# The next section will yield multiple output tables (parsed from html)
args.append(args_)

args_ = args_empty.copy()
args_['user'] = 'Niru'
args.append(args_)

args_ = args_empty.copy()
args_['user'] = 'ImHeroic'
args.append(args_)

args_ = args_empty.copy()
args_['user'] = 'UranoZero'
args_['ranking'] = 'fame-ranking'
args_['ranking_type'] = 'weekly'
args.append(args_)

args_ = args_empty.copy()
args_['user'] = 'UranoZero'
args_['ranking'] = 'fame-ranking'
args_['ranking_type'] = 'legendary'
args.append(args_)

# # NEED WORLD
# args_ = args_empty.copy()
# args_['ranking'] = 'guild'
# args_['ranking_type'] = 'classic'
# args.append(args_)

args_ = args_empty.copy()
args_['ranking'] = 'legion'
args_['ranking_type'] = 'bera'
args.append(args_)

# # WEIRD OUTPUT
# args_ = args_empty.copy()
# args_['ranking'] = 'legion-arena'
# args_['ranking_type'] = 'season1'
# args.append(args_)

args_ = args_empty.copy()
args_['ranking'] = 'maplerunner'
args_['ranking_type'] = ''
args.append(args_)

args_ = args_empty.copy()
args_['ranking'] = 'world-ranking'
args_['ranking_type'] = 'aurora'
args.append(args_)


# Take only a subset of args
# args = args[3:]
args = args[1:2]


#%%
tables = []
for i, args_ in enumerate(args):
    print('Processing Dataset %d of %d' % (i+1, len(args)))
    # tables.append( get_html_(args_) )
    tables.append( module_test_io.main(args_) )
print('Completed')

#%%

j = 0
i = -1

headers = tables[j][1]
cells = tables[j][2]

header = headers[i]
cell = cells[i]

print(headers)

# %%
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

elif header == "Guild Name":
    cell_value = cell.get_text()
elif header == "Guild Level":
    cell_value = cell.get_text()
elif header == "Guild Master":
    cell_value = cell.get_text()
elif header == "Honor Exp":
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

print(cell_value)

#%%




#%%
# Test timing of the headless chrome browser
# Try different startup options
raise

from time import time
url = module_test_io.parse_input(args[0])

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

for chrome_args in chrome_args_list:
    starttime = time()
    # These options may or may not help speed this process up
    # chrome_args.append("--ignore-certificate-errors")
    html = module_test_io.get_html(url, chrome_args)
    print("HTML with %s took %0.2f seconds" % (chrome_args, time() - starttime))


#%%