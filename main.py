import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from services.create_heatmap import create_heatmap
from services.get_topics import find_topics
from services.get_speeches import scrape_journal
from services.get_themes import find_themes
from services.match_topics import match_topics

def main():
	# get the content of each speech (if not already there)
  if not os.path.exists("constants/speeches.json"):
    # get all urls
    with open('constants/urls.json', 'r') as f:
      urls = json.load(f)
    speeches = {}
    for year in urls:
      content = scrape_journal(urls[year])
      speeches[year] = content
    with open("constants/speeches.json", "w") as f:
      json.dump(speeches, f, indent=2)
  else:
    with open('constants/speeches.json', 'r') as f:
      speeches = json.load(f)

	# get the api key
  load_dotenv()
  openai_key = os.getenv("OPENAI_API_KEY")
  if not openai_key:
    raise ValueError("Unable to retrieve the API key.")
  
  # feed each speech into chatgpt (if not already done)
  client = OpenAI(api_key=openai_key)
  if not os.path.exists("constants/topics.json"):
    topics = {}
    for year in speeches:
      if not speeches[year]:
        continue
      topics[year] = find_topics(client, speeches[year])
    with open("constants/topics.json", "w") as f:
      json.dump(topics, f, indent=2)
  else:
    with open('constants/topics.json', 'r') as f:
      topics = json.load(f)

	# find themes
  if not os.path.exists("constants/themes.json"):
    themes = find_themes(client, topics)
    with open("constants/themes.json", "w") as f:
      json.dump(themes, f, indent=2)
  else:
    with open('constants/themes.json', 'r') as f:
      themes = json.load(f)

  # match the smaller topics with larger themes
  if not os.path.exists("constants/matches.json"):
    matches = match_topics(client, topics, themes)
    with open("constants/matches.json", "w") as f:
      json.dump(matches, f, indent=2)
  else:
    with open('constants/matches.json', 'r') as f:
      matches = json.load(f)

  # creates the heatmap
  create_heatmap(matches)

if __name__ == "__main__":
	main()