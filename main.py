import requests
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込む
load_dotenv()


def summary_document(
    document_text: str, model: str = "claude-3-7-sonnet-20250219"
) -> str:
    """
    指定された Claude モデルを使用してドキュメントを要約します。

    引数:
        document_text: 要約するドキュメントのテキスト。
        model: 使用する Claude モデルの名前 (既定値: "claude-3-7-sonnet-20250219")。

    戻り値:
        ドキュメントの要約。モデルが利用できない場合はエラー メッセージを返します。
    """
    try:
        # Anthropic API キーを環境変数から取得
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return "Error: ANTHROPIC_API_KEY environment variable not set."

        # Anthropic の Claude API エンドポイント
        api_endpoint = "https://api.anthropic.com/v1/messages"

        # API リクエストのヘッダー
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        # API リクエストのペイロード
        payload = {
            "model": model,
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": f"以下のテキストを要約してください。重要なポイントを抽出し、簡潔にまとめてください。\n\n{document_text}",
                }
            ],
        }

        # API リクエストを送信
        response = requests.post(api_endpoint, headers=headers, json=payload)

        # レスポンスを処理
        if response.status_code == 200:
            response_data = response.json()
            summary = response_data["content"][0]["text"]
            return summary
        else:
            return f"Error: Failed to summarize document. Status code: {response.status_code}, Response: {response.text}"

    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"


# 使用例
if __name__ == "__main__":
    document = """人工知能 (AI) は、さまざまな業界や私たちの生活の側面を急速に変革しています。
    日常的なタスクの自動化から画期的な発見の実現まで、AI の可能性は無限です。
    しかし、AI の開発と展開に伴う倫理的配慮、偏見、潜在的な社会的影響に対処することが重要です。
    AI が全人類に利益をもたらすようにするには、責任ある人間中心のアプローチが不可欠です。
    より堅牢で説明可能な AI モデルの開発は、信頼を築き、説明責任を果たすために不可欠です。"""

    # 環境変数の設定方法:
    # .env ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を追加:
    # ANTHROPIC_API_KEY=your-api-key-here

    summary = summary_document(document)
    print("要約結果:")
    print(summary)
