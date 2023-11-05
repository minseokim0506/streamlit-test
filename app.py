import streamlit as st
import pandas as pd
import openpyxl
news = pd.read_csv("news_labeled.csv",encoding = "UTF-8")
sentences = pd.read_excel("sentences_labeled_v3.xlsx")

news_data = []
for i in range(len(news)):
    news_data.append(f"News {i + 1}")

st.title("보도 준칙 기반 기사 첨삭 서비스 준킴이")

if st.button("준킴이가 궁금하신가요?"):
     st.text("🔍 준킴이는 '한국 기자 협회'에서 제시한 분야별 보도 준칙에 의거해 작성된 기사의 적합성을 판단합니다.")
     st.text("🔍 준킴이는 기사의 문장을 점수화해 특정 점수 이하일 경우 점수 산정 근거와 표현에 대한 피드백을 제공합니다.")

# 뉴스 선택 드롭다운 목록
selected_news = st.selectbox("뉴스 선택", news_data)

if selected_news == "News 1":
    # "News 1"이 선택된 경우에만 아래 코드가 실행됩니다.
    # 텍스트 입력 상자 생성
    article = st.text_area("기사를 입력하세요", value=news[news["news_id"]==1]["main_text"].values)

news1 = sentences[sentences["news_id"]==1]
for i in range(len(news1)):
    print(news1["sentence"][i])

# 기사 첨삭 결과 표시
if st.button("첨삭하기"):
        st.subheader("첨삭된 기사")
        for i in range(len(news1)):
              data = news1["sentence"][i]
              widget_key_1 = f"text_area_{i}_1"
              widget_key_2 = f"text_area_{i}_2"
              if (news1["score_1"][i]+news1["score_2"][i]+news1["score_3"][i]+news1["score_4"][i]<=7):
                   st.write(f'<span style="color:red">{data}</span>', unsafe_allow_html=True)
                   st.text_area("이점을 참고해보세요", value = news1["news_expert_opinion"][i],key=widget_key_1)
                   st.text_area("이렇게 바꿔보세요", value =news1["alternative"][i], key =widget_key_2)
              else:
                   st.write(news1["sentence"][i])
    


