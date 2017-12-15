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
# Category Index
categoryIndex = []


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



# Find the category ( to many nested loop! break this into multiple functions to make the code easier to read) 
def findCategoryIndex(paragraphs):
	global categoryIndex
	# local variables for the class selectors
	pClass = ['ParaOverride-4']
	spanClass = ['Section-Opener-Header', 'CharOverride-2'] # if either of these classm es shows up we are good

	# can this all go into its own function?
	for p in range(len(paragraphs)):
		classes = paragraphs[p].attrs['class'] # pull classes for each paragraph
		for item in classes:
			if item in pClass:   # see if the paragraph contains the targeted class
				nestedSpans = paragraphs[p].find_all('span')  # pull all nested spans
				for span in nestedSpans:
					nestedClasses = span.attrs['class']  # get the classes of the nested spans
					for spanItem in nestedClasses:
						if spanItem in spanClass:  # see if the span contains the targeted class

							#this part is unique to this function
							if p not in categoryIndex: # see if this category has already been found
								categoryIndex.append(p) # append the new category to the found categories
								return p  # return the index of this category




# Find the index at which to start populating data. First product is always before the categegory index.
def findCategoryBeginning(paragraphs, categoryIndex):
	# local variables for the class selectors
	pClass = ['Product-Name']
	spanClass = ['_1_Product-Header']

	# This counts down instead of up
	for p in range(categoryIndex,0,-1):  #start at the category index and go backwards to find the product name index
		classes = paragraphs[p].attrs['class'] # pull the classes for each paragraph
		for item in classes:
			if item in pClass: # see if the paragraph contains the targeted class
				nestedSpans = paragraphs[p].find_all('span') # pull all the nested spans
				for span in nestedSpans:
					nestedClasses = span.attrs['class']
					for spanItem in nestedClasses:
						if spanItem in spanClass: # see if the span contains the targeted class
							return p # return the index of this product name


# Functions to check Data Type
def isProductCategory(data):
	# local variables for the class selectors
	pClass = ['ParaOverride-4']
	spanClass = ['Section-Opener-Header', 'CharOverride-2']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpans = data.find_all('span')
			for span in nestedSpans:
				nestedClasses = span.attrs['class']
				for spanItem in nestedClasses:
					if spanItem in spanClass:
						return True
	return False

def isProductName(data):
	# local variables for the class selectors
	pClass = ['Product-Name']
	spanClass = ['_1_Product-Header']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpans = data.find_all('span')
			for span in nestedSpans:
				nestedClasses = span.attrs['class']
				for spanItem in nestedClasses:
					if spanItem in spanClass:
						return True
	return False

def isProductDescription(data):
	# local variables for the class selectors
	pClass = ['ParaOverride-3']
	spanClass = ['_2_Product-Description']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpans = data.find_all('span')
			for span in nestedSpans:
				nestedClasses = span.attrs['class']
				for spanItem in nestedClasses:
					if spanItem in spanClass:
						return True
	return False


def isProductFeature(data):
	# local variables for the class selectors
	pClass = ['Bullets', 'ParaOverride-3']  #this one needs a different function so that it includes both of these classes
	spanClass = ['_2_Product-Description']
	classes = data.attrs['class']
	if classes == pClass:
		nestedSpans = data.find_all('span')
		for span in nestedSpans:
			nestedClasses = span.attrs['class']
			for spanItem in nestedClasses:
				if spanItem in spanClass:
					return True
	return False


def isProductNote(data):
	# local variables for the class selectors
	pClass = ['ParaOverride-3']
	spanClass = ['_3_Style-Numbers']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpans = data.find_all('span')
			for span in nestedSpans:
				nestedClasses = span.attrs['class']
				for spanItem in nestedClasses:
					if spanItem in spanClass:
						return True
	return False

def findDataType(data):
	if isProductCategory(data):
		return 'product_category'
	elif isProductName(data):
		return 'product_name'
	elif isProductFeature(data):  # Order of operations matter due to class sharing
		return 'product_feature'
	elif isProductDescription(data):
		return 'product_description'
	elif isProductNote(data):
		return 'product_note'	
	else:
		return ''

def populateDataType(data):
	item = [data.text]
	item.append(findDataType(data))
	return item

sortedParagraphs = list(map(populateDataType, paragraphs))

for p in sortedParagraphs:
	print(p)




# ------- TO DO --------
# How to loop over this code so that each all individual parts can be linked to one dictionary (item)
# Where is the start and end point for each loop so that all features get included, the m number, etc.
# due to the layout of the HTML , the climbing category usually comes after the first item in the category

# some product notes are showing up as product descriptions
# EXAMPLE
# ['Delivery date for Slate and Curry: 3/15/18', 'product_description']
#  