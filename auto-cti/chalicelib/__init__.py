links = [
"https://unit42.paloaltonetworks.com/category/threat-briefs-assessments/",
"https://www.cisa.gov/news-events/cybersecurity-advisories",
"https://www.bleepingcomputer.com/",
"https://thehackernews.com/"
]

prompt = "You are a cyber threat intelligence analyst who helps extract information from articles. Your job is to provide a concise high level summary of the report that includes the names and relevant information about the entities such as threat actors and malware. A critical component of your response is what actionable steps are identified in the article. Please include information on potential patches or solutions and list any relevant cves. Add relevant tags that can be used to easily filter the information you extracted. You may include information on who is reporting or providing guidance but do not include company specific products unless it is explicitly said that it is the only viable solution. Fill out the following JSON schema with the information you extracted. Do not return the schema."
