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
def filterParagraphs(paragraphs, pClass):
	# Pull in the global variable pClass
	#global pClass
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
def filterSpans(spans,spanClass):
	# Pull in the global variable spanClass
	#global spanClass
	# local variables
	items = []

	for span in spans:
		classes = span.attrs['class']
		for item in classes:
			if item in spanClass:
				items.append(span.text)
	return items


# Function to pull out the climbing categories
def climbingCategory(paragraphs):
	# local variables for the class selectors
	pClass = ['ParaOverride-4']
	spanClass = ['Section-Opener-Header', 'CharOverride-2'] # if either of these classm es shows up we are good
	spans = filterParagraphs(paragraphs,pClass)
	return filterSpans(spans,spanClass)

# Function to pull out the product names
def productName(paragraphs):
	# local variables for the class selectors
	pClass = ['Product-Name']
	spanClass = ['_1_Product-Header']
	spans = filterParagraphs(paragraphs,pClass)
	return filterSpans(spans,spanClass)

# Function to pull out the product descriptions
def productDescription(paragraphs):
	# local variables for the class selectors
	pClass = ['ParaOverride-3']
	spanClass = ['_2_Product-Description']
	spans = filterParagraphs(paragraphs,pClass)
	return filterSpans(spans,spanClass)

# Function to pull out the product features
def productFeatures(paragraphs):
	# local variables for the class selectors
	pClass = ['Bullets', 'ParaOverride-3']  #this one needs a different function so that it includes both of these classes
	spanClass = ['_2_Product-Description']
	spans = filterParagraphs(paragraphs,pClass)
	return filterSpans(spans,spanClass)


# holds all of the spans which belong to the filtered paragraphs 
#spans = filterParagraphs(paragraphs)
categories = climbingCategory(paragraphs)
names = productName(paragraphs)
descriptions = productDescription(paragraphs)
print(categories)
print(names)
print(descriptions)


# ------- TO DO --------
# How to loop over this code so that each all individual parts can be linked to one dictionary (item)
# Where is the start and end point for each loop so that all features get included, the m number, etc.
# due to the layout of the HTML , the climbing category usually comes after the first item in the category
