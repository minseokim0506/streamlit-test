import streamlit as st
import pandas as pd
#import openpyxl
news = pd.read_csv("news_labeled.csv",encoding = "UTF-8")
sentences = pd.read_excel("sentences_labeled_v3.xlsx")

news_data = []
for i in range(len(news)):
    news_data.append(f"News {i + 1}")

st.title("기사 첨삭 서비스")

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
    


