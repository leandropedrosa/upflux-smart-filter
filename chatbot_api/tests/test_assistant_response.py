# Teste a execução do agente com uma entrada de exemplo
import unittest
from dotenv import load_dotenv
import subprocess
import sys
import os

from src.assistants.assistant_response import AssistantResponseManager

sys.path.append(os.getcwd())
env_path = '../.env'
load_dotenv(env_path)
command = f'export $(grep -v "^#" {env_path} | xargs -d "\\n")'
subprocess.run(command, shell=True, executable='/bin/bash')

class TestCategorizeByAge(unittest.IsolatedAsyncioTestCase):
    async def test_assistant_exist(self):
        """
        Test Deve retornar a reposta vádida.
        """
        manager = AssistantResponseManager()
        response = await manager.execute("Olá agente?")
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main(verbosity=2)