import openai
import streamlit as st
from streamlit_chat import message
#import os
from PIL import Image
import requests
from translate import Translator
import re
import pandas as pd
from kiwipiepy import Kiwi
import numpy as np
#from dotenv import load_dotenv
#import plotly.figure_factory as ff

def translate_text(text, target_language='en'):
    translator = Translator(to_lang=target_language)
    translation = translator.translate(text)
    return translation
#load_dotenv()
# API 키 가져오기
api_key = st.secrets["api"]["key"]
# API 키 설정 (실제 키로 대체해야 함)
openai.api_key = api_key

st.set_page_config(
    page_title="너만의 플레이리스트 너플리",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto",
)

@st.cache_data
def openai_image(prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url

name  = st.sidebar.text_input("당신의 이름을 알려주세요")
if name:
   st.sidebar.write('반가워요',name,"님")
   # 사용자 선택에 따라 프롬프트 설정
   persona = {
      "팝송": "힙한",
      "시티팝": "센치한 말투로",
      "힙합" : "ㄴㄹㄴ",
      "재즈" : "ㄴㅇㄴㅇ"
   }
   selected_prompt = st.sidebar.multiselect('오늘 듣고 싶은 노래는?',options = list(persona.keys()))


col1, col2 =st.columns(2)

with col1:
     # Streamlit 앱 설정
     st.title('너만의 플레이리스트 너플리')
     st.text_area("너플리 가이드라인","""✨오늘 당신의 하루는 어땠나요? 
✨당신의 하루 속 여러 감정과 상황에 대해 알려주세요
✨상세하게 적어주신다면, 취향을 저격할 플레이리스트를 추천 드릴 수 있답니다. 
                  """)
     st.divider()

     conversation = [
        {"role": "assistant", "content": f"오늘 당신의 하루를 가장 잘 나타내줄 플레이리스트를 만들어줄게요"},
        #{"role": "assistant", "content": f"여러분의 플레이리스트 추천해줄게요"}  
       ]

     # 대화 표시 영역
     messages = []

     #session_state에 messages 리스트 초기화
     #if "messages" not in st.session_state:
      #st.session_state.messages = [
       #   {"role": "system", 
        #  "content": f"너는 상담가로 {selected_persona}인 상태에 있는 사람에게 응원을 해줄거야."}
      #]

     with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("You:", key="user_input")
        submitted = st.form_submit_button("Send")

     if submitted and user_input:
          conversation.append({"role": "user","content": f"""
                       Based on the main emotion that can feel in situation\
                       empathize  situation\
                       in short 2~3 sentences\
                       Next give your answer three noun\
                       which most describe the situation well\
                       In last you have to print nouns in forms of '#noun #noun #noun'\
                       This three noun will be used in recommendation of playlist\
                       All answer shoulde be provide in Korean\
                       Make answer fluently like talking to your friend\
                       situation : {user_input}
                       """})
          response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=conversation
          )
          assistant_response = response.choices[0].message["content"]
          conversation.append({"role": "assistant", "content": assistant_response})
          
    # 대화 표시
     for i, message_obj in enumerate(conversation):
         if message_obj["role"] == "user":
            message(user_input, is_user=True, key=f"user_message_{i}")
         else:
            message(message_obj["content"], key=f"assistant_message_{i}")
        
    # Save conversation in session state
     st.session_state.conversation = conversation

     # Accessing the chatbot's responses
     assistant_responses = [message_obj["content"] for message_obj in conversation if message_obj["role"] == "assistant"]

    # Storing the responses in a separate list (you can do this outside of the main code block)
    # Example: storing in a list named assistant_responses_list
     assistant_responses_list = st.session_state.get("assistant_responses_list", [])
     assistant_responses_list.extend(assistant_responses)
     st.session_state.assistant_responses_list = assistant_responses_list

with col2: 
   if user_input: 
        input_text = translate_text(user_input)
        prompt = f"""You have to make image\
                   which shows the situation.\
                   image will used as playlist cover\
                   so it has to be normal\
                   situation = {input_text}\
                   (markdown) = ![Image (https://image.pollinations.ai/prompt/description),\
        where description = {input_text},%20(adjective1),%20(charactersDetailed),%20(adjective2),%20(visualStyle1),%20visualStyle2,%20visualStyle3,%20genre,%20artistReference\
        """
        hashtags = re.findall(r'#\w+', assistant_responses[-1])
        if hashtags != []:
          tag_1 = hashtags[0] 
          tag_2 = hashtags[1] 
          tag_3 = hashtags[2] 
          #st.markdown(f"<p style='font-size:24px; color:brown; font-weight:bold;font-style:italic'>{tag_1+tag_2+tag_3}</p>", unsafe_allow_html=True) 

        # 로딩 중 메시지 표시
        with st.spinner("Loading...💫"):
            # 이미지 불러오기
            image_url = openai_image(prompt + input_text)
            image = Image.open(requests.get(image_url, stream=True).raw)
    
            st.markdown(
              f'<div style="display: flex; justify-content: center; align-items: center;">'
              f'<img src="{image_url}" alt="Generated Image" style="width: 200px;", caption = "앨범 표지" >'
              f'</div>',
              unsafe_allow_html=True,
            )

            # Text below the image, centered
            st.markdown(
                f'<p style="text-align: center; font-size: 28px; font-weight: bold;">{name}의 플레이 리스트</p>',
                unsafe_allow_html=True,
            )

            hashtags = re.findall(r'#\w+', assistant_responses[-1])
            if hashtags != []:
               tag_1 = hashtags[0] 
               tag_2 = hashtags[1] 
               tag_3 = hashtags[2] 

               st.markdown(
                  f'<p style="text-align: center; font-size: 20px; font-weight:bold; font-style:italic;">{tag_1 + tag_2 + tag_3}</p>',
                  unsafe_allow_html=True,
                )
               
               result_df = pd.read_csv("result_df.csv")
               song_cluster = pd.read_csv("song_cluster.csv")
               give_sentence = assistant_responses[-1] + " " + tag_1[1:] + " " + tag_2[1:] + " "+ tag_3[1:]
               give_temp = []
               kiwi = Kiwi()
               for i in kiwi.tokenize(give_sentence):
                        give_temp.append(i)
               # 내부 리스트들을 하나의 리스트로 평탄화
               give_flat_tokens = give_temp
               #데이터프레임 생성
               df = pd.DataFrame([{'form': token.form, 'tag': token.tag} for token in give_flat_tokens])
               selected_tags = ['XR','NNG']
               give_df = df[df['tag'].isin(selected_tags)].reset_index()
               give_df.drop(columns = ["index"], inplace = True)
               avg_lst = []
               for i in range(len(give_df)):
                    for j in range(len(result_df)):
                      if give_df["form"][i] == result_df["Word"][j]:
                           avg_lst.append(result_df["new_cluster"][j])
               give_avg = sum(avg_lst)/len(avg_lst)
               song_cluster['distance'] = song_cluster["mean_cluster"].apply(lambda row: abs(row - give_avg))
               random_state_sequence = np.arange(100)
               np.random.shuffle(random_state_sequence)
               random_rows = song_cluster.sort_values(by="distance").iloc[random_state_sequence[:10]]
               #random_rows = song_cluster.sort_values(by="distance")[:100].sample(n=10, random_state=42)
               random_rows.reset_index(drop=True, inplace=True)
               random_rows.index += 1
               df = random_rows[["Song","Singer","Tag"]]
               df['Tag'] = df['Tag'].apply(lambda x: ', '.join(np.random.choice(x.split(', '), size=2, replace=False)))
               # Styling the table using pandas
               #styled_df = df.style.set_table_styles([{'selector': 'th', 'props': [('background-color', 'lightblue')]},
                                                     #  {'selector': 'td', 'props': [('text-align', 'center')]}])
               # Display the styled table using Streamlit
               st.table(df)
            



