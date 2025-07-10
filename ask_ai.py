import os, re, json
from dotenv import load_dotenv
from openai import OpenAI

def find_topics(speech: str) -> str:
	'''
	feeds LLM a large text and asks it to find the main topics from an article
	'''
	# prepare client
	load_dotenv()
	client = OpenAI(
		api_key=os.getenv("OPENAI_API_KEY")
	)
	# prepare prompts
	system_prompt = (
		"You are an expert analyst of technical speeches. Given a speech transcript, "
		"extract a list of major technical or thematic topics covered in the speech. "
		"For each topic, provide a short title (1-3 words), a 1-sentence description, "
		"and a confidence score from 1-10 based on how central it is to the speech. "
		"Respond in JSON format."
	)
	user_prompt = f"Here's the speech: {speech}"
	# fetch LLM response
	response = client.chat.completions.create(
		model="gpt-4o",
		messages=[
			{"role": "system", "content": system_prompt},
			{"role": "user", "content": user_prompt},
		],
		temperature=0.3
	)
	# parse response
	topics = response.choices[0].message.content
	if topics is None:
		raise ValueError("LLM response had no content")
	output = re.search(r"```json\s*(.*?)```", topics, re.S)
	if not output:
		output = ""
	else:
		output = output.group(1)
	return output