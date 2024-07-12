import unittest
from dotenv import load_dotenv
import os
import sys

# Adicione o caminho do diretório raiz do projeto ao PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.assistants.assistant_create import AssistantCreateManager

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(dotenv_path='../.env')

class TestAssistantCreateManager(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_exist(self):
        """
        Test should return a valid response.
        """
        manager = AssistantCreateManager()
        response = await manager.execute("Informe a quantidade total de ordens de vendas nos dois meses passados?", session_id="bcd")
        print(f"Resposta {response}")
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main(verbosity=2)