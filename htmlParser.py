from lxml import html
from bs4 import BeautifulSoup
import re, csv


#      ----- GLOBAL VARIABLES ------
# Get the filename you want to work with
fileName = input('Please enter the name of the html file: ')

# Create the soup 
with open(("P:\QA\Berry\S18\\" + fileName + ".html"),"r", encoding="utf-8") as f:
	soup = BeautifulSoup(f, 'lxml')

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
			return p # return the index of this product name\
	return categoryIndex


# Functions to check Data Type
def isProductCategory(data):
	# local variables for the class selectors
	pClass = ['ParaOverride-4', 'ParaOverride-2']
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
	pClass = ['ParaOverride-3', 'ParaOverride-1'] 
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
	pClass = ['ParaOverride-3', 'ParaOverride-1']
	spanClass = ['_3_Style-Numbers']
	classes = data.attrs['class']
	for item in classes:
		if item in pClass:
			nestedSpan = data.find('span')
			nestedClasses = nestedSpan.attrs['class']
			for nestedClass in nestedClasses:
				if nestedClass in spanClass:
					return True
	return False

def findDataType(data):
	if isProductCategory(data):
		return 'product_category'
	elif isProductName(data):
		return 'product_name'
	elif isProductFeature(data):  # Order of operations matter due to class sharing
		return 'product_feature'
	elif isProductNote(data):
		return 'product_note'
	elif isProductDescription(data):
		return 'product_description'
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
	'm_number': [], 'notes': []}

	item['product_category'] = category


	for i in range(startIndex,endIndex,1):
		if paragraphs[i][1] == "product_name":
			item['product_name'] = paragraphs[i][0]
		elif paragraphs[i][1] == "product_description":
			if paragraphs[i-1][1] == "product_description":
				item['product_description'] = paragraphs[i-1][0] + paragraphs[i][0]
			else: 
				item['product_description'] = paragraphs[i][0]
		elif paragraphs[i][1] == "product_feature":
			item['features'].append(paragraphs[i][0])
		elif paragraphs[i][1] == "product_note":
			item['notes'].append(paragraphs[i][0])

	# Set the M Number
	if len(item['notes']) > 0:
		for note in item['notes']:
			mNumber = re.findall(r'\d+', note)
			if len(mNumber) > 0 and len(mNumber[0]) == 6:
				item['m_number'].append(mNumber[0])

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



def WriteDictToCSV(csv_file,products):
	fieldNames = ['product_category', 'product_name', 'product_description', 'features', \
	'm_number', 'notes']
	try:
		with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=fieldNames, delimiter='|')
			writer.writeheader()
			for product in products:
				writer.writerow({'product_category': product['product_category'], 'product_name': product['product_name'], \
					'product_description': product['product_description'], 'features': product['features'], 'm_number': product['m_number'], \
					'notes': product['notes']})
	except IOError:
		print("I/O error", csv_file)
	return




# ------- body of script -------


sortedParagraphs = list(map(populateDataType, paragraphs))

filteredParagraphs = list(filter(filterParagraphs, sortedParagraphs))

# Category Indexes
categoryIndex = findCategoryIndex(filteredParagraphs)

products = documentLoop(filteredParagraphs)
print('\n') # make a new line below where the script got the input for the file name
for x in products:
	print(x)
	print('\n')


WriteDictToCSV(fileName + ".csv",products)


     

# ------- TO DO --------
#
# Make sure this works with all the sections. It doesnt at this point for some reason.
	# Some sections use different class names
