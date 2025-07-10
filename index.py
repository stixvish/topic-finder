from ask_ai import find_topics
from scraper import scrape_journal
import json
import pandas as pd

def main():
	with open('urls.json', 'r') as f:
		urls = json.load(f)
	
	text = {}
	records = []
	for year, url in urls.items():
		text[year] = scrape_journal(url)
	for year, url in urls.items():
		topics = find_topics(text[year])
		if topics:
			topics = json.loads(topics)
		else:
			continue
		for topic in topics:
			topic['year'] = int(year)
		records.extend(topics)

	# build DataFrame
	df = pd.DataFrame(records)
	ts = df.pivot(index='year', columns='title', values='confidence')
	ts = ts.fillna(0).sort_index()

	print(json.dumps(ts.to_json(orient='index'), indent=2))

if __name__ == "__main__":
	main()
