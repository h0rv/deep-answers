import streamlit as st

import model


def wrap_text(st, text: str):
    st.markdown(
        f'<span style="word-wrap:break-word;">{text}</span>', unsafe_allow_html=True
    )


def main():
    st.markdown("# Get <u>Answers</u> to your _Deep Questions_", unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Enter prompt"):
        st.chat_message("user").markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        resp = model.prompt(prompt)

        st.session_state.messages.append({"role": "assistant", "content": resp})

        st.chat_message("assistant").markdown(resp)


if __name__ == "__main__":
    main()
