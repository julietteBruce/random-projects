from bs4 import BeautifulSoup
import requests
import re 

def get_webpage(url):
	req = requests.get(url)
	return BeautifulSoup(req.content, 'html.parser')

def get_href_links(url):
	""" Returns list with all href links on page from URL."""
	soup = get_webpage(url)
	all_links = soup.find_all("a")
	return [link.get('href') for link in all_links]

# print(get_href_links('https://www.quantamagazine.org/archive/'))

def elmements_with_substring(list,string):
	"""Returns a list of elements from a list with a given substring."""
	return [elm for elm in list if string in elm]


def has_substring_from_list(string,list_of_substrings):
	for substring in list_of_substrings:
		if substring in string:
			return True
	return False

def elements_without_substrings(list_of_links,unwanted_substrings):
	links_to_return = []
	for link in list_of_links:
		if not has_substring_from_list(link,unwanted_substrings):
			links_to_return.append(link)
	return links_to_return

def get_quanta_links_from_archive_page(base_url,page_number):
	list_of_links = get_href_links(base_url + 'page/' + str(page_number))
	unwanted_substrings = ['/tag', '/authors/', 'http', '/privacy-policy', '/physics/', '/mathematics/', '/biology/', 
							'/computer-science/', '/topics', '/archive/', '/topics','/about/', '/archive', '/contact-us/', 
							'/terms-conditions/', '#newsletter', '/privacy-policy/', '/qa/', '/#comments']
	wanted_links = elements_without_substrings(list_of_links,unwanted_substrings)
	return list(set(wanted_links))

# test = get_quanta_links_from_archive_page('https://www.quantamagazine.org/archive/',1)
# print(test)
# print(len(test))

def get_quanta_links_from_archive(base_url,last_page_number):
	links_to_return = []
	for page_number in range(1,last_page_number+1):
		links_to_return += get_quanta_links_from_archive_page(base_url,page_number)
	return list(set(links_to_return))

# test = get_quanta_links_from_archive('https://www.quantamagazine.org/archive/',182)
# print(test)
# print(len(test))

def get_certain_links(url,string):
	"""Returns a list of href links on the page from URL with given substring."""
	href_links = get_href_links(url)
	return elmements_with_substring(href_links,string)

# print(get_certain_links('https://www.quantamagazine.org/new-proof-shows-when-structure-must-emerge-in-graphs-20220623/','arxiv'))

def get_MSC_from_arxiv(url):
	soup = get_webpage(url)
	msc_tbs = soup.find_all("td", {"class": "msc-classes"})
	return [elm.getText() for elm in msc_tbs]

print(get_MSC_from_arxiv('https://arxiv.org/abs/2212.11097'))

def split_MSC_from_arxiv(url):
	msc_dictionary = {}
	string_MSC = get_MSC_from_arxiv(url)[0]
	split_MSC = string_MSC.split(' (primary), ')
	msc_dictionary['primary'] = split_MSC[0]
	if len(split_MSC) > 1:
		msc_dictionary['secondary'] = split_MSC[1][:-12].split(', ')
	return msc_dictionary

print(split_MSC_from_arxiv('https://arxiv.org/abs/2212.11097'))

def get_primarySubject_from_arxiv(url):
	soup = get_webpage(url)
	sub_tbs = soup.find_all("span", {"class": "primary-subject"})
	return [elm.getText() for elm in sub_tbs]

# print(get_primarySubject_from_arxiv('https://arxiv.org/abs/2212.11097'))


def get_subjects_from_arxiv(url):
	soup = get_webpage(url)
	sub_tbs = soup.find_all("td", {"class": "subjects"})
	#return msc_tbs
	subs_unformated = [elm.getText() for elm in sub_tbs][0].split("; ")
	return [elm.lstrip() for elm in subs_unformated]

# print(get_subjects_from_arxiv('https://arxiv.org/abs/2212.11097'))

def get_secondarySubjects_from_arxiv(url):
	primary_subject = get_primarySubject_from_arxiv(url)
	all_subjects = get_subjects_from_arxiv(url)
	all_subjects.remove(primary_subject[0])
	return all_subjects

# print(get_secondarySubjects_from_arxiv('https://arxiv.org/abs/2212.11097'))

# test1 = ['Commutative Algebra (math.AC)']
# test2 = ['Commutative Algebra (math.AC)', 'Algebraic Geometry (math.AG)']
# print(test1[0])
# print(test1[0] in test2)
# test1 = [1,2,3,'apple']
# print(test1.remove(1))
# # def get_certain_links(url,string):
# # 	href_links = get_href_links(url)
# # 	for link
# url = 'https://arxiv.org/abs/2104.14598'
# req = requests.get(url)
# soup = BeautifulSoup(req.content, 'html.parser')
# #print(soup.prettify())
# print(soup.find_all("td",{"class":"msc-classes"}))

# print(get_webpage('https://www.quantamagazine.org/new-proof-shows-when-structure-must-emerge-in-graphs-20220623/'))
# test = soup.find_all("td",{"class":"msc-classes"})
# for elm in test:
# 	print(elm.getText())
# # all_links = soup.find_all("a")
# # href_links = [link.get('href') for link in all_links]
# # print(href_links)
# # ##print(all_links[0])

# # for link in href_links:
# # 	if 'arxiv' in link:
# # 		print(link)
# # #for link in all_links:
# # #  print(link.get_text())	# this will prints all text
# # #  print(link.get('href'))