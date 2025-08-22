import json
from openai import OpenAI

def match_topics(client: OpenAI, topics_by_year: dict[str, list[dict[str, str | int]]], themes: list[dict[str, str | int]]):
  # prepare topics
  summary_lines = []
  for year, topics in topics_by_year.items():
    summary_lines.append(f"\n{year}")
    for topic in topics:
      name = topic.get('name', 'Unknown')
      confidence = topic.get('confidence', 0.0)
      description = topic.get('description', '')
      summary_lines.append(f"• {name} (conf: {confidence}) - {description}")
  theme_names = [theme['name'] for theme in themes]
  themes_description = "\n".join([f"- {theme['name']}: {theme['description']}" for theme in themes])
  # prepare prompt
  prompt = f"""
    You have these 7 themes:
    {themes_description}
          
    For each year below, assign topics to themes and calculate total confidence scores.
          
    Rules:
    - A topic can contribute to multiple themes if it genuinely fits
    - Only assign topics that clearly belong to a theme - don't force poor matches
    - Sum the confidence scores of all topics assigned to each theme
    - If a theme has no topics in a year, its score is 0
    - Be consistent with theme names (use exact names from the list above)
          
    Years and topics:
    {"\n".join(summary_lines)}
          
    Return JSON format with ALL 7 themes for each year:
    {{
      "YEAR1": {{"{theme_names[0]}": 0.0, "{theme_names[1]}": 0.0, "{theme_names[2]}": 0.0, "{theme_names[3]}": 0.0, "{theme_names[4]}": 0.0, "{theme_names[5]}": 0.0, "{theme_names[6]}": 0.0}},
      "YEAR2": {{"{theme_names[0]}": 0.0, "{theme_names[1]}": 0.0, "{theme_names[2]}": 0.0, "{theme_names[3]}": 0.0, "{theme_names[4]}": 0.0, "{theme_names[5]}": 0.0, "{theme_names[6]}": 0.0}},
      ...
    }}
          
    Replace YEAR1, YEAR2 with actual years and 0.0 with calculated confidence sums. Include all years present in the data.
  """
	# fetch LLM response
  response = client.responses.create(
		model="gpt-5",
		input=prompt,
		reasoning={"effort": "high"},
		text={"verbosity": "medium"}
	)
  # Parse JSON response
  themes_data = json.loads(response.output_text.strip())
  return themes_data