# cse6242-chatbot

Edstem Chatbot which leverages RAG model to fetch best answers to students questions. Basic flow as follows:
- Scrape old thread responses and maintain parent-child relation  
- Anonymize sensitive student data by using presidio  
- Vectorize data and create langchain RAG model to fetch relevant data from query and rephrase with LLM of choice back to student giving references 
- Dockerize, host on cloud infrastructure easy with terraform 


# To Run 
- build dockerfile in chatbot/
- host image where wanted 
- entrypoint at serve.py 

