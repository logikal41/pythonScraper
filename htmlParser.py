from lxml import html
from bs4 import BeautifulSoup

with open("P:\QA\Berry\S18\Section_2.html","r", encoding="utf8") as f:
	soup = BeautifulSoup(f, 'lxml')

#             ----- GLOBAL VARIABLES ------
# All products will be stored in this global variable
products = []
# pull all of the paragraphs in the soup
paragraphs = soup.find_all('p')


# Find the category indexs 
def findCategoryIndex(paragraphs):
	index = []

	for p in range(len(paragraphs)):
		if paragraphs[p][1] == "product_category":
			if p not in index:
				index.append(p) # append the new category to the found categories
	index.append(len(paragraphs)) #this will be a stop point for loops
	return index  # return the list of category indexes


# Find the index at which to start populating data. First product is always before the categegory index.
def findCategoryBeginning(paragraphs, categoryIndex):
	# This counts down instead of up
	for p in range(categoryIndex,-1,-1):  #start at the category index and go backwards to find the product name index
		if paragraphs[p][1] == "product_name":
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
			return True
			# nestedSpans = data.find_all('span')
			# for span in nestedSpans:
			# 	nestedClasses = span.attrs['class']
			# 	for spanItem in nestedClasses:
			# 		if spanItem in spanClass:
			# 			return True
	return False

def isProductDescription(data):
	# local variables for the class selectors
	pClass = ['ParaOverride-3']
	spanClass = ['_2_Product-Description']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpan = data.find('span')
			nestedClass = nestedSpan.attrs['class']
			if nestedClass[0] in spanClass:
				return True
	return False


def isProductFeature(data):
	# local variables for the class selectors
	pClass = ['Bullets', 'ParaOverride-3']  #must include both classes
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
			nestedSpan = data.find('span')
			nestedClass = nestedSpan.attrs['class']
			if nestedClass[0] in spanClass:
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
		return 'na'

def populateDataType(data):
	item = [data.text]
	item.append(findDataType(data))
	return item

def filterParagraphs(data):
	if data[1] != 'na':
		return True
	return False

def populateProduct(paragraphs,category,startIndex,endIndex):
	#Initialize item dictionary
	item = {'product_category': '', 'product_name': '', 'product_description': '', 'features': [], \
	'm_number': '', 'size': '', 'color': '', 'notes': []}

	item['product_category'] = category

	for i in range(startIndex,endIndex,1):
		if paragraphs[i][1] == "product_name":
			item['product_name'] = paragraphs[i][0]
		elif paragraphs[i][1] == "product_description":
			item['product_description'] = paragraphs[i][0]
		elif paragraphs[i][1] == "product_feature":
			item['features'].append(paragraphs[i][0])
		elif paragraphs[i][1] == "product_note":
			item['notes'].append(paragraphs[i][0])

	# item['m_number'] = item['notes'].pop(0) dealign with m number
	return item


def categoryLoop(paragraphs,firstProduct,nextCategory):
	productIndex = []
	for i in range(firstProduct,nextCategory,1):
		if paragraphs[i][1] == "product_name":
			productIndex.append(i)
	productIndex.append(nextCategory)
	return productIndex

def documentLoop(paragraphs):
	products = []
	categoryIndex = findCategoryIndex(filteredParagraphs)

	for i in range(len(categoryIndex)-1):
		categoryStart = findCategoryBeginning(paragraphs, categoryIndex[i])
		productsIndex = categoryLoop(paragraphs,categoryStart,categoryIndex[i+1])
		for x in range(len(productsIndex)-1):
			info = populateProduct(paragraphs,paragraphs[categoryIndex[i]][0],productsIndex[x],productsIndex[x+1])
			if len(products) == 0:
				products.append(info)
			elif products[len(products)-1]['product_name'] == info['product_name']:
				del products[len(products)-1]
				products.append(info)
			else:
				products.append(info)
	return products















# ------- body of script -------


sortedParagraphs = list(map(populateDataType, paragraphs))
filteredParagraphs = list(filter(filterParagraphs, sortedParagraphs))

# Category Indexes
categoryIndex = findCategoryIndex(filteredParagraphs)



# product = populateProduct(filteredParagraphs,'shoes',0,11)
# print(product)

products = documentLoop(filteredParagraphs)
for x in products:
	print(x)
	print('\n')


# ------- TO DO --------
# Seperate the M number out of the notes section
	# M number has 6 digits and is sometimes combined with other information. Use the regex to grab the number.
# Only populate products that are "NEW" (they have the new image next to the product)

