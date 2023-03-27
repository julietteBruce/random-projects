from bs4 import BeautifulSoup
import requests
import re 
import pandas as pd

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

def remove_none_values_from_list(input_list):
	return [elm for elm in input_list if elm is not None]

# input_list = ['test', 'arxivtest', None, '2212testdog']
# print(remove_none_values_from_list(input_list))

def elmements_with_substring(input_list,desired_substring):
	"""Returns a list of elements from a list with a given substring."""
	return [elm for elm in input_list if elm is not None and desired_substring in elm]

# input_list = ['test', 'arxivtest', '2212testdog']
# desired_substring = 'arxiv'
# print(elmements_with_substring(input_list,desired_substring))

# input_list = ['test', 'arxivtest', None, '2212testdog']
# desired_substring = 'arxiv'
# print(elmements_with_substring(input_list,desired_substring))

def has_substring_from_list(input_string,list_of_substrings):
	for desired_substring in list_of_substrings:
		if input_string is not None and desired_substring in input_string:
			return True
	return False

def elements_without_substrings(list_of_links,unwanted_substrings):
	links_to_return = []
	for link in list_of_links:
		if not has_substring_from_list(link,unwanted_substrings):
			links_to_return.append(link)
	return links_to_return

def get_quanta_links_from_archive_page(base_url,page_number):
	print()
	list_of_links = get_href_links_url(base_url + 'page/' + str(page_number))
	unwanted_substrings = ['/tag', '/authors/', 'http', '/privacy-policy', '/physics/', '/mathematics/', '/biology/', 
							'/computer-science/', '/topics', '/archive/', '/topics','/about/', '/archive', '/contact-us/', 
							'/terms-conditions/', '#newsletter', '/privacy-policy/', '/qa/', '/#comments', '/puzzles/', 
							'/multimedia/', '/abstractions/']
	wanted_links = unique_elements(elements_without_substrings(list_of_links,unwanted_substrings))
	wanted_links.remove('/')
	return wanted_links

# test = get_quanta_links_from_archive_page('https://www.quantamagazine.org/archive/',1)
# print(test)
# print(len(test))

def get_quanta_links_from_archive(base_url,last_page_number):
	links_to_return = []
	for page_number in range(1,last_page_number+1):
		print(page_number)
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

def convert_arxiv_pdf_to_abs(url):
	if url[-3:] == 'pdf':
		arxiv_id = url[:-4].split('/')[-1]
		base_arxiv_url = 'https://arxiv.org/abs/'
		return base_arxiv_url + arxiv_id
	return url

# url = 'https://arxiv.org/pdf/2101.08898.pdf'
# print(convert_arxiv_pdf_to_abs(url))

# url = 'https://arxiv.org/abs/0802.3361'
# print(convert_arxiv_pdf_to_abs(url))

def get_arxiv_links(webpage_soup):
	links_containing_arxiv_substring = get_certain_links(webpage_soup,'arxiv')
	unwanted_arxiv_type_sites = ['eartharxiv','search']
	wanted_arxiv_links = elements_without_substrings(links_containing_arxiv_substring, unwanted_arxiv_type_sites)
	return [convert_arxiv_pdf_to_abs(url) for url in wanted_arxiv_links]

# # This article contains two arxiv links. 
# webpage_soup = get_webpage('https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/')
# print(get_arxiv_links(webpage_soup))

# # This article contains an eartharxiv paper, but no arxive papers. 
# webpage_soup = get_webpage('https://www.quantamagazine.org/scientists-unravel-how-the-tonga-volcano-caused-worldwide-tsunamis-20220413/')
# print(get_arxiv_links(webpage_soup))

# # This article contains two arxiv links, and one is to a pdf. 
# webpage_soup = get_webpage('https://www.quantamagazine.org/mathematicians-find-a-new-class-of-digitally-delicate-primes-20210330/')
# print(get_arxiv_links(webpage_soup))

def get_arxiv_links_url(url):
	webpage_soup = get_webpage(url)
	return get_arxiv_links(webpage_soup)

# # This article contains two arxiv links. 
# url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(get_arxiv_links_url(url))

# # This article contains an eartharxiv paper, but no arxive papers. 
# url = 'https://www.quantamagazine.org/scientists-unravel-how-the-tonga-volcano-caused-worldwide-tsunamis-20220413/'
# print(get_arxiv_links_url(url))

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
	dictionary_MSC = {'primary': [], 'secondary': []}
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

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_title_arxiv_listing(webpage_soup))

def get_title_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_title_arxiv_listing(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_title_arxiv_listing_url(url))

def get_original_date_arxiv_listing(webpage_soup):
	date_div = (webpage_soup.find_all("meta", {"name": "citation_date"}))[0]
	return date_div['content']

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_original_date_arxiv_listing(webpage_soup))

def get_original_date_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_original_date_arxiv_listing(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_original_date_arxiv_listing_url(url))

def get_recent_date_arxiv_listing(webpage_soup):
	date_div = (webpage_soup.find_all("meta", {"name": "citation_online_date"}))[0]
	return date_div['content']

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# print(get_recent_date_arxiv_listing(webpage_soup))

def get_recent_date_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_recent_date_arxiv_listing(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_recent_date_arxiv_listing_url(url))

def get_id_arxiv_listing(webpage_soup):
	id_div = (webpage_soup.find_all("meta", {"name": "citation_arxiv_id"}))[0]
	return id_div['content']

# webpage_soup = get_webpage('https://arxiv.org/abs/2212.11097')
# webpage_soup = get_webpage('https://arxiv.org/abs/1201.6644')
# print(get_id_arxiv_listing(webpage_soup))

def get_id_arxiv_listing_url(url):
	webpage_soup = get_webpage(url)
	return get_id_arxiv_listing(webpage_soup)

# url = 'https://arxiv.org/abs/2212.11097'
# print(get_id_arxiv_listing_url(url))

def process_arxiv_listing(url):
	webpage_soup = get_webpage(url)
	output_dictionary = {
	'arxiv_id': get_id_arxiv_listing(webpage_soup),
	'title' : get_title_arxiv_listing(webpage_soup),
	'authors': get_author_arxiv_listing(webpage_soup),
	'original_submission_date': get_original_date_arxiv_listing(webpage_soup),
	'most_recent_update_date': get_recent_date_arxiv_listing(webpage_soup),
	'primary_subject': get_primarySubject_from_arxiv(webpage_soup),
	'secondary_subject': get_secondary_subjects_from_arxiv(webpage_soup),
	'primary-MSC': split_MSC_from_arxiv(webpage_soup)['primary'],
	'secondary_MSC': split_MSC_from_arxiv(webpage_soup)['secondary']
	}
	return output_dictionary

# url = 'https://arxiv.org/abs/2212.11097'
# print(process_arxiv_listing(url))

# Test with not MSC
# url = 'https://arxiv.org/abs/2303.11723'
# print(process_arxiv_listing(url))

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
	arxiv_links = get_arxiv_links(webpage_soup)
	output_list = []
	for link in arxiv_links:
		print(f"{link}\n")
		arxiv_dictionary = process_arxiv_listing(link)
		joint_arxiv_quanta_dictionary = quanta_article_dictionary|arxiv_dictionary
		output_list.append(joint_arxiv_quanta_dictionary)
	return output_list

url = 'https://www.quantamagazine.org/long-sought-math-proof-unlocks-more-mysterious-modular-forms-20230309/'
# print(process_quanta_article(url))

def process_quanta_archive(base_url,page_number):
	list_of_quanta_links = get_quanta_links_from_archive(base_url,page_number)
	output_list = []
	for qaunta_link in list_of_quanta_links:
		print(f"{qaunta_link}\n")
		article_url = "https://www.quantamagazine.org" + qaunta_link
		output_list.append(process_quanta_article(article_url))
	return output_list

def process_quanta_archive_page(base_url,page_number):
	list_of_quanta_links = get_quanta_links_from_archive_page(base_url,page_number)
	output_list = []
	for qaunta_link in list_of_quanta_links:
		print(f"{qaunta_link}\n")
		article_url = "https://www.quantamagazine.org" + qaunta_link
		output_list.append(process_quanta_article(article_url))
	return output_list

# base_url = 'https://www.quantamagazine.org/archive/'
# page_number = 2
# test = process_quanta_archive(base_url,page_number)
# print(test)
# print(len(test))

def count_nonempty_lists(list_of_lists):
	running_cout_of_nonempty_lists = 0
	for list1 in list_of_lists:
		if list1:
			running_cout_of_nonempty_lists += 1
	return running_cout_of_nonempty_lists

# test = [[], [1,2], [], [2,3]]
# print(count_nonempty_lists(test))

def flatten_list(list_of_lists):
	return [elm for list1 in list_of_lists for elm in list1]

# test = [[], [1], [], [2,3]]
# print(flatten_list(test))

# base_url = 'https://www.quantamagazine.org/archive/'
# page_number = 49
# # test = get_quanta_links_from_archive_page(base_url,page_number)
# # print(test)
# test2 = process_quanta_archive_page(base_url,page_number)
# print(test2)

# base_url = 'https://www.quantamagazine.org/mathematicians-find-a-new-class-of-digitally-delicate-primes-20210330/'
# test = get_certain_links_url(base_url,'arxiv')
# print(test)

page_number = 75
base_url = 'https://www.quantamagazine.org/archive/'
# list_of_quanta_links = get_quanta_links_from_archive(base_url,page_number)

# test = [link for link in list_of_quanta_links if not link[-2].isdigit()]
# print(test)
test = process_quanta_archive(base_url,page_number)
print(count_nonempty_lists(test))
print(len(test))

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

testDF = pd.DataFrame(data=flatten_list(test))
print(testDF)

testDF.to_csv("test-75pages.csv",index=False)




# 25 pages of quanta archvie
# 93 articles with arixv link
# 225 total articles
