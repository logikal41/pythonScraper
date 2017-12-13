from lxml import html
from bs4 import BeautifulSoup

with open("P:\QA\Berry\S18\shoe_section.html","r", encoding="utf8") as f:
	soup = BeautifulSoup(f, 'lxml')

#             ----- GLOBAL VARIABLES ------
# All products will be stored in this global variable
products = []
# Paragraph classes of interest (global variable)
pClass = ['ParaOverride-3', 'ParaOverride-4', 'Product-Name']
# Span classes of interest
spanClass = ['Section-Opener-Header', 'CharOverride-2', 'Category-Introduction', \
'_1_Product-Header', '_2_Product-Description', '_3_Style-Numbers']
# pull all of the paragraphs in the soup
paragraphs = soup.find_all('p')


#Initialize item dictionary (global variable)
item = {'product category': '', 'product name': '', 'product description': '', 'features': '', \
'm number': '', 'size': '', 'color': '', 'notes': ''}


# Function to pull all the spans out of the targeted paragraphs
def filterParagraphs(paragraphs):
	# Pull in the global variable pClass
	global pClass
	# local variables
	spans = []

	for p in paragraphs:
		classes = p.attrs['class']
		for item in classes:
			if item in pClass:
				nestedSpans = p.find_all('span')
				for span in nestedSpans:
					spans.append(span)
	return spans

# Function to pull the text out of the targeted spans
def filterSpans(spans):
	# Pull in the global variable spanClass
	global spanClass
	# local variables
	items = []

	for span in spans:
		classes = span.attrs['class']
		for item in classes:
			if item in spanClass:
				items.append(span.text)
	return items



# holds all of the spans which belong to the filtered paragraphs 
spans = filterParagraphs(paragraphs)
products = filterSpans(spans)
print(products)


