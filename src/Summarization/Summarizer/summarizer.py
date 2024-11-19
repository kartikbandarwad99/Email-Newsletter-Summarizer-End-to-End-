from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

class NewsletterSummarizer:
    def __init__(self, api_key, model_name='gemini-pro'):
        self.api_key = api_key
        self.model_name = model_name
        # Initialize the Gemini model with the given API key and model name
        self.gemini_model = GoogleGenerativeAI(model=model_name, google_api_key=api_key)
        # Define the summary template
        self.template = """You are a Newsletter assistant who provides detailed and 
        concise summaries of the given email newsletters. Use bulleted points wherever necessary.
        Here's the email Newsletter:{newsletter}
        """
    
    def generate_summary(self, mail_newsletter):
        # Create a prompt with the template
        prompt = PromptTemplate(template=self.template, input_variables=['newsletter'])
        # Chain the prompt with the gemini model
        chain = prompt | self.gemini_model
        print('Generating Summary')
        # Generate the summary
        output = chain.invoke({'newsletter': mail_newsletter})
        return output
    
    def get_token_count(self, text):
        # Utility method to get the number of tokens in a given text
        return self.gemini_model.get_num_tokens(text)

