import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# OpenAI APIキーの設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLMからの回答を取得する関数
def get_llm_response(input_text, expert_type):
    if expert_type == "建築基準法の専門家":
        system_message = "あなたは建築基準法の専門家です。以下の質問に専門的な観点から回答してください。"
    elif expert_type == "プログラミングの専門家":
        system_message = "あなたはプログラミングの専門家です。以下の質問に専門的な観点から回答してください。"
    else:
        system_message = "あなたは一般的な知識を持つAIです。以下の質問に回答してください。"

    # プロンプトの作成
    prompt = PromptTemplate(
        input_variables=["system_message", "user_input"],
        template="{system_message}\nユーザーの質問: {user_input}"
    )

    # LLMの初期化
    llm = OpenAI(api_key=OPENAI_API_KEY)

    # プロンプトをLLMに渡して回答を取得
    response = llm(prompt.format(system_message=system_message, user_input=input_text))
    return response

# Streamlitアプリの構築
st.title("専門家に質問できるアプリ")

# アプリの概要を表示
st.write("このアプリでは、建築基準法の専門家またはプログラミングの専門家に質問することができます。以下のフォームに質問を入力し、専門家の種類を選択して送信してください。")

# 入力フォーム
input_text = st.text_input("質問を入力してください:")

# ラジオボタンで専門家の種類を選択
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("建築基準法の専門家", "プログラミングの専門家")
)

# 送信ボタン
if st.button("送信"):
    if input_text.strip():
        # LLMからの回答を取得
        response = get_llm_response(input_text, expert_type)
        # 回答を表示
        st.subheader("回答:")
        st.write(response)
    else:
        st.error("質問を入力してください！")

