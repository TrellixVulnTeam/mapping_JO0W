import pprint
from bs4 import BeautifulSoup
import csv
import arc

import argparse

parser = argparse.ArgumentParser(description='Fetch data from arc and convert to csv')
parser.add_argument('-o', '--output', required=True)
parser.add_argument('-k','--keywords', nargs='+', help='<Required> Set keywords', required=True)

args = parser.parse_args()

filename = args.output
filepath = 'output/' + filename + '.csv'

print(filepath)

pp = pprint.PrettyPrinter(indent=4)

viewbox = '-74.194188332210331,40.981164736109228,-76.467791908698715,38.676157795304704'
count = 0
size = 500
frm = 0
content_elements = []

keywords = args.keywords
print(keywords)

while frm is not None:
    request_url = arc.url(size, frm, keywords)
    data = arc.request(request_url)
    content_elements.extend(data.get('content_elements',[]))
    frm = data.get('next')
    print(frm)

# pp.pprint(data)

with open(filepath, mode='w') as employee_file:

  employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  employee_writer.writerow(['identifier', 'published_at', 'title', 'content', 'viewbox', 'source_url', 'thumbnail', 'author_names'])

  for content_element in content_elements:
    # pp.pprint(content_element)

    website_url = content_element['website_url']
    source_url = 'https://www.inquirer.com' + website_url

    promo_items = content_element.get('promo_items', {})
    basic = promo_items.get('basic', {})
    additional_properties = basic.get('additional_properties', {})
    thumbnailResizeUrl = additional_properties.get('thumbnailResizeUrl')

    credits = content_element.get('credits', {})
    by = credits.get('by', {})
    authors = [k.get('name') for k in by]
    authors = "|".join(authors)

    title = content_element['headlines']['basic']
    # print(title)

    identifier = content_element['_id']
    # print(identifier)

    publish_date = content_element['publish_date']
    first_publish_date = content_element['first_publish_date']

    all_content = ""

    elements = content_element['content_elements']
    for element in elements:
      # print(element)

      content_type = element.get("type", "")

      content = element.get("content", "")
      if content_type == 'text':
        # print(content_type)
        # print(element)
        all_content += content
        all_content += " "

    soup = BeautifulSoup(all_content, features="html.parser")
    text = soup.get_text()
    
    employee_writer.writerow([identifier, first_publish_date, title, text, viewbox, source_url, thumbnailResizeUrl, authors])  
    count = count + 1
    
print(count)