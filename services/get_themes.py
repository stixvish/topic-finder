import json
from openai import OpenAI

def find_themes(client: OpenAI, topics_by_year: dict[str, list[dict[str, str | int]]]):
  # prepare topics
  summary_lines = []
  for year, topics in topics_by_year.items():
    summary_lines.append(f"\n{year}")
    for topic in topics:
      name = topic.get('name', 'Unknown')
      confidence = topic.get('confidence', 0.0)
      description = topic.get('description', '')
      summary_lines.append(f"• {name} (conf: {confidence}) - {description}")
  # prepare prompts
  prompt = f"""
    Analyze ALL topics across ALL years to identify exactly 7 overarching themes that best represent the major conceptual areas in this dataset.
          
    Requirements:
    - Themes should be broad enough to encompass multiple related topics across different years
    - Focus on themes that appear consistently or show clear evolution over time
    - Themes should be meaningful for academic/research analysis
    - Name themes clearly and concisely (2-4 words each)
          
    Here's the complete topic data:
    {"\n".join(summary_lines)}
          
    Return ONLY a JSON array with exactly 7 themes:
    [
      {{"name": "Theme Name 1", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 2", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 3", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 4", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 5", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 6", "description": "What this theme encompasses"}},
      {{"name": "Theme Name 7", "description": "What this theme encompasses"}}
    ]
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