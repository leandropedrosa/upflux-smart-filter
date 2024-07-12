from langchain.agents import Tool
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings
from src.client.atlas_client import AtlasClient
from src.utils.async_utils import url_to_vector
from src.utils.documents import docs
import os

INDEX_NAME = os.getenv('ATLAS_INDEX_NAME')


class ToolDefinition:
    """
    Uma classe para definir ferramentas usadas em agentes LangChain.

    Métodos:
    -------
    create_json_retriever(json_path: str) -> Tool
        Cria uma ferramenta de recuperação de JSON para o caminho especificado.
    create_page_retriever(page_url: str) -> Tool
        Cria uma ferramenta de recuperação de página para a URL especificada.
    """

    def create_json_retriever(self, json_path: str, name: str, description: str) -> Tool:
        """
        Cria uma ferramenta de recuperação de JSON para o caminho especificado.

        Parâmetros:
        ----------
        json_path : str
            O caminho para o arquivo JSON.

        Retorna:
        -------
        Tool
            A ferramenta configurada para recuperar dados do arquivo JSON.
        """
        retriever_json = url_to_vector(file_name=json_path)
        return Tool(
            func=retriever_json.invoke,
            name=name,
            description=description
        )

    def create_page_retriever(self, page_url: str) -> Tool:
        """
        Cria uma ferramenta de recuperação de página para a URL especificada.

        Parâmetros:
        ----------
        page_url : str
            A URL da página web.

        Retorna:
        -------
        Tool
            A ferramenta configurada para recuperar dados da página web.
        """
        retriever_page = url_to_vector(url=page_url)
        return Tool(
            func=retriever_page.invoke,
            name="lcel_text",
            description="Use esta ferramenta para obter os termos referentes aos conhecimentos da página web."
        )


    def create_mongo_retriever(self) -> Tool:
        """
        Cria uma ferramenta de recuperação de JSON para o caminho especificado.

        Parâmetros:
        ----------
        json_path : str
            O caminho para o arquivo JSON.

        Retorna:
        -------
        Tool
            A ferramenta configurada para recuperar dados do arquivo JSON.
        """
        client = AtlasClient()

        vector_search = MongoDBAtlasVectorSearch.from_documents(
            documents=docs,
            embedding=OpenAIEmbeddings(),
            collection=client.get_collection(),
            index_name=INDEX_NAME
        )
        retriever = vector_search.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return Tool(
            func=retriever.invoke,
            name="lcel_mongo_json",
            description="Use esta ferramenta para obter os termos que estão no arquivo JSON."
        )