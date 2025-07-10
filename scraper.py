import cloudscraper
from bs4 import BeautifulSoup

def scrape_journal(url: str) -> str:
	'''
	method that fetches and cleans the text.
	'''
	# create scraper
	scraper = cloudscraper.create_scraper(
		browser = {
			'browser': 'chrome',
			'platform': 'windows',
			'mobile': False
		}
	)
	# fetch the data
	response = scraper.get(url)
	if response.status_code != 200:
		raise Exception(f"Failed to fetch page {url}: {response.status_code}")
	scraper.close()
	# parse the response
	soup = BeautifulSoup(response.text, 'html.parser')
	for ack in soup.find_all('section', id='acknowledgments'):
		ack.decompose()
	section = soup.select_one('section#bodymatter[property="articleBody"]')
	if not section:
		raise Exception(f"Section 'bodymatter' not found on page {url}")
	target_div = section.select_one('div.core-container')
	if not target_div:
		raise Exception(f"Div 'core-container' not found within section on page {url}")
	for a in target_div.find_all('a'):
		a.decompose()
	for fig in target_div.find_all('figure'):
		fig.decompose()
	for ack in target_div.find_all('section', id='acknowledgments'):
		ack.decompose()
	raw_text = target_div.get_text(strip=True)
	return raw_text