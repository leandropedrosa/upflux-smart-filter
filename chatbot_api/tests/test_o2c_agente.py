import unittest
from dotenv import load_dotenv
import subprocess
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.agents.o2c_agente import O2CAgentManager

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
        manager = O2CAgentManager()
        response = await manager.execute("Olá agente?")
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main(verbosity=2)