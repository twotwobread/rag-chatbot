import streamlit as st


def get_ai_message(): ...


st.set_page_config(page_title="저작권 챗봇")

st.title("저작권 챗봇")
st.caption("저작권에 관련된 모든 것을 답해드립니다.")

if "message_list" not in st.session_state:
    st.session_state.message_list = []

for message in st.session_state.message_list:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if user_question := st.chat_input(
    placeholder="저작권에 관련된 궁금한 내용들을 말씀해주세요!"
):
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.message_list.append(
        {"role": "user", "content": user_question}
    )

    with st.spinner("답변을 생성하는 중입니다..."):
        with st.chat_message("ai"):
            st.write("AI 응답 메시지")
        st.session_state.message_list.append(
            {"role": "ai", "content": "AI 응답 메시지"}
        )
