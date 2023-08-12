from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.datastructures import FileStorage

from schemas import (
    GenerateRequest,
    GenerateResponse,
    ExecCodeRequest,
    ExecCodeResponse,
    UploadFileResponse,
)

from modules.openai_client import OpenAIClient
from modules.jupyter_kernel import (
    start_kernel,   
    execute_code,
)
from modules.azure_client import AzureClient
from modules.financial_data_manager import FinancialDataManager

openai_client = OpenAIClient()
azure_client = AzureClient()
financial_data_manager = FinancialDataManager()

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

class UploadFile(Resource):
    def post(self):
        # リクエストボディからファイルを取得し、保存
        file: FileStorage = request.files['file']

        # ファイルをBlobストレージに保存
        blob_url = azure_client.upload_file(
            container_name="pdf", 
            file_name=file.filename, 
            file_content=file.read()
        )

        # ファイルを作業用に一時的に保存 
        tmp_file = azure_client.download_file(
            container_name="pdf", 
            file_name=file.filename
        )

        # テキスト抽出処理
        pdf_text = financial_data_manager.extract_text(tmp_file)

        # テキストから財務データを含む表を生成
        table_text = financial_data_manager.extract_text_and_create_table(pdf_text)

        # 財務データ抽出処理
        financial_data = financial_data_manager.extract_financial_data(table_text)

        # レスポンスを返す
        res = UploadFileResponse(
            file_name=file.filename,
            blob_url=blob_url,
            financial_data=financial_data,
        )

        return res.model_dump()
    

api.add_resource(Generate, '/api/generate')
api.add_resource(ExecCode, '/api/exec-code')
api.add_resource(UploadFile, '/api/upload-file')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')