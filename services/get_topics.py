import json
from openai import OpenAI

def find_topics(client: OpenAI, speech: str):
  '''
	feeds LLM a large text and asks it to find the main topics from an article
	'''
  # prepare prompts
  prompt = f"""
    Analyze the following speech and identify the main topics discussed. For each topic, provide:
    1. A clear, concise topic name (2-4 words)
    2. A confidence score from 0 to 10 indicating how central this topic is to the speech
    3. A brief description explaining what aspect of this topic is discussed
        
    Confidence score guidelines:
    - 10: Core theme, discussed extensively throughout the speech
    - 8-9: Major topic, significant portion of speech devoted to it
    - 6-7: Important topic, clearly present but not dominant
    - 4-5: Minor topic, mentioned but not elaborated much
    - 2-3: Tangential topic, briefly touched upon
        
    Return ONLY a valid JSON array with max 10 topics, formatted as:
    [
      {{
        "name": "Topic Name",
        "confidence": 8,
        "description": "Brief description of what's discussed",
      }}
    ]

    Speech text:
    {speech}
  """
	# fetch LLM response
  response = client.responses.create(
		model="gpt-5",
		input=prompt,
		reasoning={"effort": "high"},
		text={"verbosity": "medium"}
	)
  # Parse JSON response
  topics_data = json.loads(response.output_text.strip())
  return topics_data