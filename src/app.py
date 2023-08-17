import streamlit as st

import model


def wrap_text(st, text: str):
    st.markdown(
        f'<span style="word-wrap:break-word;">{text}</span>', unsafe_allow_html=True
    )


def main():
    st.markdown("# Get __Answers__ to your _Deep Questions_")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    messages = st.session_state.messages


    if prompt := st.chat_input("Enter prompt"):
        st.chat_message("user").markdown(prompt)

        resp = model.prompt(prompt)

        st.chat_message("assistant").markdown(resp)
        # wrap_text(, resp)

    # prompt = st.text_input("Enter prompt: ")
    #
    # if len(prompt) > 0:
    #     with st.spinner(text="Generating"):
    #         resp = model.prompt(prompt)
    #
    #         # st.success("")
    #         wrap_text(st, resp)
    #
    #         return


if __name__ == "__main__":
    main()
