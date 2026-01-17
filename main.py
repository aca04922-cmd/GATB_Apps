import streamlit as st
from google import genai

# 1. クライアントの初期化
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

st.title("🚀 GATB数値に基づく適職診断アドバイザー")

# --- ガイダンスセクション ---
st.info("""
### 📢 はじめに
適確な診断のために、まずは厚生労働省のホームページ等を確認し、
**GATB（一般職業適性検査）**を受検することをお勧めします。
受検後、お手元のスコア（性能スコア）を以下に入力してください。
""")

# --- 入力セクション ---
st.subheader("1. GATB適性スコアの入力")
col1, col2, col3, col4 = st.columns(4)
with col1:
    g_score = st.number_input("知的能力 (G)", 0, 200, 100)
    v_score = st.number_input("言語能力 (V)", 0, 200, 100)
with col2:
    n_score = st.number_input("数理能力 (N)", 0, 200, 100)
    q_score = st.number_input("書記的知覚 (Q)", 0, 200, 100)
with col3:
    s_score = st.number_input("空間判断能力 (S)", 0, 200, 100)
    p_score = st.number_input("形態知覚 (P)", 0, 200, 100)
with col4:
    k_score = st.number_input("運動共応 (K)", 0, 200, 100)

st.subheader("2. 職業の入力")
current_job = st.text_input("現在の職業を入力")
seeking_job = st.text_input("なりたい職業を入力")

# --- 診断セクション ---
if st.button("AI適性診断を実行"):
    # スコアを文字列にまとめる
    scores_text = f"G:{g_score}, V:{v_score}, N:{n_score}, Q:{q_score}, S:{s_score}, P:{p_score}, K:{k_score}"
    
    prompt = f"""
    以下のGATB適性検査の数値に基づき、キャリアアドバイスを行ってください。
 
    【重要ルール】
        - 回答は「〜の傾向があります」「〜という考え方もあります」といった、柔軟な「提案型」の表現にしてください。
        - ユーザーの可能性を否定せず、前向きなアドバイスを心がけてください。
        - 断定的な表現（「向いていません」「不可能です」など）は避けてください。

    【適性スコア】
    {scores_text}
    
    【状況】
    現在の職業: {current_job}
    なりたい職業: {seeking_job}
    
    【依頼事項】
    1. 現在の職業に対する適性レベルを客観的に分析してください。
    2. なりたい職業（{seeking_job}）に対する適性と、不足している能力へのアドバイスを提示してください。
    3. このスコア（{scores_text}）の傾向から、特に向いていると思われる職業を3つ提案してください。
    """

    with st.spinner("AIが適性を分析中..."):
        try:
            # モデル名は確実に存在する "gemini-1.5-flash" に修正しました
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=prompt
            )
            st.success("分析が完了しました。")
            st.markdown("---")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# --- 免責事項セクション ---
st.markdown("---")
st.caption("""
**免責事項**
* **公的機関との関係性について**: 本サービスは、厚生労働省および関連する公的機関とは一切関係のない、個人の開発による実験的なツールです。
* **回答の性質**: AIによる診断結果は、一般的な統計データに基づいた「可能性の示唆」であり、医学的・心理学的な専門診断や、特定の職業への成功を保証するものではありません。
* **正確性について**: GATBの正確な判定には専門の検査官による実施と解釈が必要です。本ツールの結果はあくまで自己理解を深めるための参考情報としてご利用ください。
* **自己責任**: 本ツールの診断結果に基づいて行われた転職、退職、就職活動等のいかなる行動についても、開発者は一切の責任を負いかねます。最終的な判断は、公的な窓口（ハローワーク等）や専門のコンサルタントに相談の上、ご自身で行ってください。
""")