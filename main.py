from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from schemas import (
    GenerateRequest,
    GenerateResponse,
    ExecCodeRequest,
    ExecCodeResponse,
)

from modules.openai_client import OpenAIClient
from modules.jupyter_kernel import (
    start_kernel,   
    execute_code,
)

openai_client = OpenAIClient()

app = Flask(__name__)
CORS(app)
api = Api(app)


class Generate(Resource):
    def post(self):
        # リクエストボディからデータを取得
        req = request.get_json()
        data = GenerateRequest(**req)

        # コード生成処理
        result = openai_client.generate_code(data.user_input)

        # レスポンスを返す
        res = GenerateResponse(
            generated_code=result
        )
        return res.model_dump()


class ExecCode(Resource):
    def post(self):
        # リクエストボディからデータを取得
        req = request.get_json()
        data = ExecCodeRequest(**req)

        # カーネル起動処理
        kernel_client = start_kernel()

        # コード実行処理
        output, message_type = execute_code(data.code, kernel_client)

        # レスポンスを返す
        res = ExecCodeResponse(
            output=output,
            message_type=message_type,
        )
        return res.model_dump()

api.add_resource(Generate, '/api/generate')
api.add_resource(ExecCode, '/api/exec-code')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')