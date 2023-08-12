import os
import re
from dotenv import load_dotenv
import openai

from .prompts import CODE_PROMPT

class OpenAIClient:
    def __init__(self) -> None:
        load_dotenv()
        openai.api_type = "azure"
        openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
        openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

    def generate_code(self, user_input: str) -> str:
        # OpenAI APIで送信するメッセージを作成
        messages = [
            {"role": "system", "content": "あなたは優秀なコード生成アシスタントです。"},
            {"role": "user", "content": CODE_PROMPT.format(user_input)},
        ]
        
        # OpenAI APIを叩き生成処理を実行
        response = openai.ChatCompletion.create(
            engine=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            messages=messages,
            max_tokens=os.getenv("MAX_TOKENS"),
            temperature=0.5,
            top_p=1,
            stop=None,
            frequency_penalty=1,
            presence_penalty=1,
        )

        # トリプルバッククォートで囲まれたコードを抽出して返す
        return self._extract_code(response.choices[0].message.content)
    
    def _extract_code(self, text:str) -> str:
        try:
            triple_match = re.search(r'```(?:\w+\n)?(.+?)```', text, re.DOTALL)
            return triple_match.group(1).strip()
        except:
            return "No code found."
    

if __name__ == "__main__":
    test = OpenAIClient()
    print(test.generate_code("バブルソートしたい。"))