from googleapiclient import discovery
import json


def getTheScore(content):
	content = f"{content}"
	
	API_KEY = '' # this is the api from perpective AI, which is used for sentiment analysis. look it up if ur interested.
	client = discovery.build("commentanalyzer","v1alpha1",developerKey=API_KEY,discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",static_discovery=False,)
	
	analyze_request = {'comment': { 'text': f'{content}' },'requestedAttributes': {'TOXICITY': {}, 'FLIRTATION': {}}}
	
	response = client.comments().analyze(body=analyze_request).execute()
	
	toxic = response["attributeScores"]["TOXICITY"]["spanScores"][0]["score"]["value"]
	flirt = response["attributeScores"]["FLIRTATION"]["spanScores"][0]["score"]["value"]
	scores = {}
	scores["flirt"] = flirt*10
	scores["toxic"] = toxic*10
	return scores
	
	



