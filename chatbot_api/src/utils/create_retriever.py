import dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import WebBaseLoader, JSONLoader

REVIEWS_CSV_PATH = "data/reviews.csv"
REVIEWS_CHROMA_PATH = "chroma_data"

dotenv.load_dotenv()

loader_url = WebBaseLoader("https://blog.pedidoeletronico.com/order-to-cash/")
loader_json = JSONLoader(jq_schema=".",
                    file_path="./data/datatype_definitions.json",
                    text_content=False)

reviews_url = loader_url.load()
reviews_json = loader_url.load()
text_splitter = RecursiveCharacterTextSplitter()
documents_url = text_splitter.split_documents(reviews_url)
documents_json= text_splitter.split_documents(reviews_json)
Chroma.from_documents(
    documents_url, OpenAIEmbeddings(), persist_directory="chroma_data/"
)

Chroma.from_documents(
    documents_json, OpenAIEmbeddings(), persist_directory="chroma_data/"
)