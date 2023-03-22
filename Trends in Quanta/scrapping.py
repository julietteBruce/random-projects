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

# Test with not MSC
# webpage_soup = get_webpage('https://arxiv.org/abs/2303.11723')
# print(get_MSC_from_arxiv(webpage_soup))

def get_MSC_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return get_MSC_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_MSC_from_arxiv_url(url))

# Test with not MSC
# url = 'https://arxiv.org/abs/2303.11723'
# print(get_MSC_from_arxiv_url(url))

def split_MSC_from_arxiv(webpage_soup):
	dictionary_MSC = {}
	list_MSC = get_MSC_from_arxiv(webpage_soup)
	if list_MSC:
		string_MSC = list_MSC[0]
		split_MSC = string_MSC.split(' (primary), ')
		dictionary_MSC['primary'] = split_MSC[0]
		if len(split_MSC) > 1:
			dictionary_MSC['secondary'] = split_MSC[1][:-12].split(', ')
	return dictionary_MSC

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(split_MSC_from_arxiv(webpage_soup))

# Test with not MSC
# webpage_soup = get_webpage('https://arxiv.org/abs/2303.11723')
# print(split_MSC_from_arxiv(webpage_soup))

def split_MSC_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return split_MSC_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(split_MSC_from_arxiv_url(url))

# Test with not MSC
# url = 'https://arxiv.org/abs/2303.11723'
# print(split_MSC_from_arxiv_url(url))

def get_primarySubject_from_arxiv(webpage_soup):
	sub_tbs = webpage_soup.find_all("span", {"class": "primary-subject"})
	return [elm.getText() for elm in sub_tbs]

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_primarySubject_from_arxiv(webpage_soup))

def get_primarySubject_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return get_primarySubject_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_primarySubject_from_arxiv_url(url))

def get_subjects_from_arxiv(webpage_soup):
	sub_tbs = webpage_soup.find_all("td", {"class": "subjects"})
	subs_unformated = [elm.getText() for elm in sub_tbs][0].split("; ")
	return [elm.lstrip() for elm in subs_unformated]

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_primarySubject_from_arxiv(webpage_soup))

def get_subjects_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return get_subjects_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_primarySubject_from_arxiv_url(url))

def get_secondary_subjects_from_arxiv(webpage_soup):
	primary_subject = get_primarySubject_from_arxiv(webpage_soup)
	all_subjects = get_subjects_from_arxiv(webpage_soup)
	all_subjects.remove(primary_subject[0])
	return all_subjects

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_secondary_subjects_from_arxiv(webpage_soup))

def get_secondary_subjects_from_arxiv_url(url):
	webpage_soup = get_webpage(url)
	return get_secondary_subjects_from_arxiv(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_secondary_subjects_from_arxiv_url(url))


# print(get_secondary_subjects_from_arxiv('https://arxiv.org/abs/2303.11428'))
# print(get_secondarySubjects_from_arxiv('https://arxiv.org/abs/2212.11097'))

def get_author_quanta_article(webpage_soup):
	author_div = webpage_soup.find_all("div", {"class": "h3t mv05"})
	list_of_authors = unique_elements([elm.getText() for elm in author_div])
	return [author.replace('By ', '') for author in list_of_authors]

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(get_author_quanta_article(webpage_soup))

def get_author_quanta_article_url(url):
	webpage_soup = get_webpage(url)
	return get_author_quanta_article(webpage_soup)

# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(get_author_quanta_article_url(url))

def get_pub_date_quanta_article(webpage_soup):
	date_element = (webpage_soup.find_all("meta", {"property": "article:published_time"}))[0]
	pub_data_time = date_element['content']
	return pub_data_time[:10]

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(get_pub_date_quanta_article(webpage_soup))

def get_pub_date_quanta_article_url(url):
	webpage_soup = get_webpage(url)
	return get_pub_date_quanta_article(webpage_soup)

# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(get_pub_date_quanta_article_url(url))

def get_title_quanta_article(webpage_soup):
	title_element = (webpage_soup.find_all("meta", {"property": "og:title"}))[0]
	title_with_branding = title_element['content']
	title = (title_with_branding.split(" | "))[0]
	return title

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(get_title_quanta_article(webpage_soup))

def get_title_quanta_article_url(url):
	webpage_soup = get_webpage(url)
	return get_title_quanta_article(webpage_soup)

# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(get_title_quanta_article_url(url))

def get_author_arxiv_listing(webpage_soup):
	author_div = webpage_soup.find_all("meta", {"name": "citation_author"})
	list_of_authors = unique_elements([author['content'] for author in author_div])
	return list_of_authors

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_author_arxiv_listing(webpage_soup))

def get_author_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_author_arxiv_listing(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_author_arxiv_listing_url(url))

def get_title_arxiv_listing(webpage_soup):
	title_div = (webpage_soup.find_all("meta", {"name": "citation_title"}))[0]
	return title_div['content']

webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
print(get_title_arxiv_listing(webpage_soup))

def get_title_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_title_arxiv_listing(webpage_soup)

url = 'https://arxiv.org/abs/2212.11097'
print(get_title_arxiv_listing_url(url))


def process_arxiv_listing(url):
	webpage_soup = get_webpage(url)
	output_dictionary = {
	'title' : get_title_arxiv_listing(webpage_soup),
	'authors': get_author_arxiv_listing(webpage_soup),
	'original_submission_date': NEED,
	'most_recent_update_date': NEED,
	'primary_subject': get_primarySubject_from_arxiv(webpage_soup),
	'secondary_subject': get_secondary_subjects_from_arxiv(webpage_soup),
	'primary-MSC': split_MSC_from_arxiv(webpage_soup)[0],
	'secondary_MSC': NEED
	}
	return output_dictionary

def quanta_article_overview(webpage_soup):
	output_dictionary = {
	'quanta_author' : get_author_quanta_article(webpage_soup),
	'quanta_pub_date': get_pub_date_quanta_article(webpage_soup),
	'quanta_title': get_title_quanta_article(webpage_soup)
	}
	return output_dictionary

# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(quanta_article_overview(webpage_soup))

def quanta_article_overview_url(url):
	webpage_soup = get_webpage(url)
	return quanta_article_overview(webpage_soup)

# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(quanta_article_overview_url(url))

def process_quanta_article(url):
	webpage_soup = get_webpage(url)
	quanta_article_dictionary = quanta_article_overview(webpage_soup)
	arxiv_links = get_certain_links(webpage_soup,'arxiv')
	output_list = []
	for link in arxiv_links:
		arxiv_dictionary = process_arxiv_listing(url)
		joint_arxiv_quanta_dictionary = quanta_article_dictionary|arxiv_dictionary
		output_list.append(joint_arxiv_quanta_dictionary)
	return output_list


print(get_webpage('https://arxiv.org/abs/2012.02892'))

<meta content="2020/12/04" name="citation_date"/>
<meta content="2022/12/05" name="citation_online_date"/>
<meta content="https://arxiv.org/pdf/2012.02892" name="citation_pdf_url"/>
<meta content="2012.02892" name="citation_arxiv_id"/>





