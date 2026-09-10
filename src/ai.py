import openai
import os
from dotenv import load_dotenv

class LlmManager:
    def __init__(self):
        self.url = "https://aitta-api.csc.fi/openai/v1"
        self.model = "openai/gpt-oss-120b"
        self.prompt = "count to ten" # the file
        self.instructions = "Do everything reversed" # where the codebook goes if i understood correctly

        """saa muokata vapaasti! tää toimii tällä hetkellä, mutta aika hitaasti :D
        """

    def call_aitta(self):

        load_dotenv()

        key = os.getenv('AITTA_API_KEY')

        client = openai.OpenAI(api_key=key, base_url=self.url)
        chat_completion = client.chat.completions.create(messages=[
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": self.prompt}],
            model=self.model,
            stream=True)
        
        return chat_completion

    def change_promt(self):
        pass

    def change_codebook(self): # currently the instructions attrubute
        pass
