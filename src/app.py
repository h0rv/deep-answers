import streamlit as st
import model

def wrap_text(st, text: str):
    st.markdown(f'<span style="word-wrap:break-word;">{text}</span>', unsafe_allow_html=True)

def main():
    st.markdown("# Get Answers to your _Deep Questions_")

    prompt = st.text_input("Enter prompt: ")

    if len(prompt) > 0:
        with st.spinner(text="Generating"):
            resp = model.prompt(prompt)

            # st.success("")
            wrap_text(st, resp)

            return


if __name__ == "__main__":
    main()
