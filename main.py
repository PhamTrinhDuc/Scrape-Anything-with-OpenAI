import streamlit as st
from scape import (
    scape_website, 
    extract_body_content, 
    clean_body_content, 
    split_dom_content
)
from parse import parse_with_openai


st.title("AI Web Scaper")
url = st.text_input("Enter a Website URL")

if st.button("Scape Site"):
    st.write("Scaping the website")
    result = scape_website(website=url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM Content"):
        st.text_area("DOM content", cleaned_content, height=300)



if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse", height=100)

    if st.button("Parse content"):
        if parse_description:
            st.write("Parsing the content")

            dom_content = split_dom_content(st.session_state.dom_content)
            result = parse_with_openai(dom_content, parse_description)
            st.write(result)
