import streamlit as st
import pandas as pd
import openpyxl
news = pd.read_csv("news_labeled.csv",encoding = "UTF-8")
sentences = pd.read_excel("sentences_labeled_v3.xlsx")
custom_css = """
body {
    background-color: lightgray;
}
"""
st.write('<style>{}</style>'.format(custom_css), unsafe_allow_html=True)

news_data = []
for i in range(len(news)):
    news_data.append(f"News {i + 1}")

st.title("보도 준칙 기반 기사 첨삭 서비스 준킴이")

if st.button("준킴이가 궁금하신가요?"):
     st.text("🔍 준킴이는 '한국 기자 협회'에서 제시한 분야별 보도 준칙에 의거해 작성된 기사의 적합성을 판단합니다.")
     st.text("🔍 준킴이는 기사의 문장을 점수화해 특정 점수 이하일 경우 점수 산정 근거와 표현에 대한 피드백을 제공합니다.")

# 뉴스 선택 드롭다운 목록
selected_news = st.selectbox("뉴스 선택", news_data)

# 선택한 뉴스 번호 추출
selected_news_number = int(selected_news.split()[1])

# 선택한 뉴스 번호에 해당하는 데이터 추출
selected_news_data = news[news["news_id"] == selected_news_number]
selected_sentences_data = sentences[sentences["news_id"] == selected_news_number]

# "News 1"이 선택된 경우에만 아래 코드가 실행됩니다.
# 텍스트 입력 상자 생성
article = st.text_area("기사를 입력하세요", value=selected_news_data["main_text"].values[0])

# 기사 첨삭 결과 표시
if st.button("첨삭하기"):
    st.text_area("전체적인 기사의 피드백입니다", value=selected_sentences_data["news_expert_opinion"].values[0])
    st.subheader("첨삭된 기사")
    for i in range(len(selected_sentences_data)):
        data = selected_sentences_data["sentence"].values[i]
        widget_key = f"text_area_{i}_2"
        if (selected_sentences_data["score_1"].values[i] + selected_sentences_data["score_2"].values[i] +
            selected_sentences_data["score_3"].values[i] + selected_sentences_data["score_4"].values[i] <= 9):
            st.write(f'<span style="color:red">{data}</span>', unsafe_allow_html=True)
            st.text_area("이렇게 바꿔보세요", value=selected_sentences_data["alternative"].values[i], key=widget_key)
        else:
            st.write(data)
    

