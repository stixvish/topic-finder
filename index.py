from ask_ai import find_topics
from scraper import scrape_journal
import json
import pandas as pd

def main():
	with open('urls.json', 'r') as f:
		urls = json.load(f)
	
	text = {}
	records = {}
	for year, url in urls.items():
		text[year] = scrape_journal(url)
	for year, url in urls.items():
		topics = find_topics(text[year])
		if topics:
			topics = json.loads(topics)
		else:
			continue
		records[year] = topics

	print(json.dumps(records, indent=2))

if __name__ == "__main__":
	main()
