import os
import re
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

class AzureClient():
    def __init__(self):
        # Blob Storageに接続
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)


    def upload_file(self, container_name: str, file_name: str, file_content: bytes):
        # コンテナが存在しない場合は作成
        if not self.blob_service_client.get_container_client(container_name).exists():
            self.blob_service_client.create_container(container_name)
        
        # コンテナクライアントの作成
        container_client = self.blob_service_client.get_container_client(container_name)

        # ファイルをアップロード
        blob_client = container_client.upload_blob(file_name, data=file_content, overwrite=True)
        
        # ファイルのURLを取得
        blob_path = blob_client.get_blob_properties()["name"]
        account_name = re.search("AccountName=(.*?);", self.connection_string).group(1)
        account_url = f"https://{account_name}.blob.core.windows.net"
        blob_url = f"{account_url}/{container_name}/{blob_path}"

        return blob_url
    
    def download_file(self, container_name: str, file_name: str):
        # コンテナクライアントの作成
        container_client = self.blob_service_client.get_container_client(container_name)

        # ファイルをダウンロード
        blob_client = container_client.get_blob_client(file_name)
        download_stream = blob_client.download_blob()
        content_binary = download_stream.readall()

        # バイナリデータを一時的に保存する
        tmp_file = 'workspace/tmp.pdf'
        with open(tmp_file, 'wb') as f:
            f.write(content_binary)

        return tmp_file