from bs4 import BeautifulSoup
import requests
import re 

def get_webpage(url):
	req = requests.get(url)
	return BeautifulSoup(req.content, 'html.parser')

def unique_elements(input_list):
	return list(set(input_list)) 

def get_href_links(webpage_soup):
	""" Returns list with all href links on page from URL."""
	all_links = webpage_soup.find_all("a")
	return [link.get('href') for link in all_links]

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(get_href_links(webpage_soup))

def get_href_links_url(url):
	""" Returns list with all href links on page from URL."""
	webpage_soup = get_webpage(url)
	return get_href_links(webpage_soup)

# print(get_href_links_url('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'))

def elmements_with_substring(input_list,desired_substring):
	"""Returns a list of elements from a list with a given substring."""
	return [elm for elm in input_list if desired_substring in elm]


def has_substring_from_list(input_string,list_of_substrings):
	for desired_substring in list_of_substrings:
		if desired_substring in input_string:
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
	return unique_elements(wanted_links)

# test = get_quanta_links_from_archive_page('https://www.quantamagazine.org/archive/',1)
# print(test)
# print(len(test))

def get_quanta_links_from_archive(base_url,last_page_number):
	links_to_return = []
	for page_number in range(1,last_page_number+1):
		links_to_return += get_quanta_links_from_archive_page(base_url,page_number)
	return unique_elements(links_to_return)

# test = get_quanta_links_from_archive('https://www.quantamagazine.org/archive/',182)
# print(test)
# print(len(test))

def get_certain_links(webpage_soup,desired_substring):
	"""Returns a list of href links on the page from URL with given substring."""
	href_links = get_href_links(webpage_soup)
	return elmements_with_substring(href_links,desired_substring)

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# desired_substring = 'arxiv'
# print(get_certain_links(webpage_soup,desired_substring))

def get_certain_links_url(url,desired_substring):
	"""Returns a list of href links on the page from URL with given substring."""
	href_links = get_href_links_url(url)
	return elmements_with_substring(href_links,desired_substring)

# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# desired_substring = 'arxiv'
# print(get_certain_links_url(url,desired_substring))

def get_MSC_from_arxiv(webpage_soup):
	msc_tbs = webpage_soup.find_all("td", {"class": "msc-classes"})
	return [elm.getText() for elm in msc_tbs]

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_MSC_from_arxiv(webpage_soup))

def get_MSC_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return get_MSC_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_MSC_from_arxiv_url(url))
# print(get_MSC_from_arxiv('https://arxiv.org/abs/2212.11097'))

### LEFT OFF HERE ###

def split_MSC_from_arxiv(url):
	dictionary_MSC = {}
	string_MSC = get_MSC_from_arxiv(url)[0]
	if string_MSC:
		split_MSC = string_MSC.split(' (primary), ')
		dictionary_MSC['primary'] = split_MSC[0]
		if len(split_MSC) > 1:
			dictionary_MSC['secondary'] = split_MSC[1][:-12].split(', ')
	return dictionary_MSC

# print(split_MSC_from_arxiv('https://arxiv.org/abs/2212.11097'))

# print(get_MSC_from_arxiv('https://arxiv.org/abs/2303.11428'))
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

# print(get_subjects_from_arxiv('https://arxiv.org/abs/2303.11428'))
def get_secondary_subjects_from_arxiv(url):
	primary_subject = get_primarySubject_from_arxiv(url)
	all_subjects = get_subjects_from_arxiv(url)
	all_subjects.remove(primary_subject[0])
	return all_subjects
# print(get_secondary_subjects_from_arxiv('https://arxiv.org/abs/2303.11428'))
# print(get_secondarySubjects_from_arxiv('https://arxiv.org/abs/2212.11097'))

def get_author_quanta_article(url):
	soup = get_webpage(url)
	sub_tbs = soup.find_all("div", {"class": "h3t mv05"})
	list_of_authors = unique_elements([elm.getText() for elm in sub_tbs])
	return [author.replace('By ', '') for author in list_of_authors]



# print(get_author_quanta_article('https://www.quantamagazine.org/quantum-computing-solves-classical-problems-20121218/'))