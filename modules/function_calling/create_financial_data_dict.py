# Function calling用関数のクラスを定義
class CreateFinancialDataDict:
    metadata = {
        "name": "create_financial_data_dict",
        "description": "会社の財務データを格納する辞書を作成する関数",
        "parameters": {
            "type": "object",
            "properties": {
                "会社名": {
                    "type": "string",
                    "description": "会社の名前"
                },
                "決算期": {
                    "type": "string",
                    "description": "会社の決算期"
                },
                "売上高": {
                    "type": "number",
                    "description": "会社の売上高"
                },
                "売上原価": {
                    "type": "number",
                    "description": "会社の売上原価"
                },
                "販管費": {
                    "type": "number",
                    "description": "会社の販管費"
                },
                "経常利益": {
                    "type": "number",
                    "description": "会社の経常利益"
                },
                "流動資産合計": {
                    "type": "number",
                    "description": "会社の流動資産合計"
                },
                "固定資産合計": {
                    "type": "number",
                    "description": "会社の固定資産合計"
                },
                "流動負債合計": {
                    "type": "number",
                    "description": "会社の流動負債合計"
                },
                "固定負債合計": {
                    "type": "number",
                    "description": "会社の固定負債合計"
                },
                "純資産合計": {
                    "type": "number",
                    "description": "会社の純資産合計"
                },
                "営業活動キャッシュフロー": {
                    "type": ["number", "null"],
                    "description": "会社の営業活動キャッシュフロー"
                },
                "投資活動キャッシュフロー": {
                    "type": ["number", "null"],
                    "description": "会社の投資活動キャッシュフロー"
                },
                "財務活動キャッシュフロー": {
                    "type": ["number", "null"],
                    "description": "会社の財務活動キャッシュフロー"
                },
                "株式分割の有無": {
                    "type": "string",
                    "enum": ["有", "無"],
                    "description": "株式分割の有無"
                },
                "予想修正の有無": {
                    "type": "string",
                    "enum": ["有", "無"],
                    "description": "予想修正の有無"
                }
            },
            "required": [
                "会社名", 
                "決算期", 
                "売上高", 
                "売上原価", 
                "販管費", 
                "経常利益", 
                "流動資産合計", 
                "固定資産合計", 
                "流動負債合計", 
                "固定負債合計", 
                "純資産合計", 
                "株式分割の有無",
                "予想修正の有無"
            ]
        }
    }