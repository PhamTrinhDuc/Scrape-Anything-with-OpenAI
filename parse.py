from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv

dotenv.load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = ChatOpenAI(
    model = "gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0.2,
    max_tokens=1024
)

def parse_with_openai(dom_chunks, parse_desc):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    parsed_output = []

    for i, chunk in enumerate(dom_chunks):
        # print(chunk)
        # print(parse_desc)
        # break
        response = chain.invoke(
            {"dom_content": chunk,
             "parse_description": parse_desc}
        ).content

        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_output.append(response)

    return "\n\n".join(parsed_output)