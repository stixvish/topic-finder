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
		topics = find_topics(text[year])
		if topics:
			topics = json.loads(topics)
		else:
			continue
		records[year] = topics

	with open('output.json', 'w', encoding='utf-8') as f:
		json.dump(records, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
	main()