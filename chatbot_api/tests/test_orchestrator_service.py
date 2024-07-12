# Teste a execução do agente com uma entrada de exemplo
import unittest
from dotenv import load_dotenv
import subprocess
import sys
import os
from test_upflux_assistants import execute

sys.path.append(os.getcwd())
env_path = '../.env'
load_dotenv(env_path)
command = f'export $(grep -v "^#" {env_path} | xargs -d "\\n")'
subprocess.run(command, shell=True, executable='/bin/bash')

class TestCategorizeByAge(unittest.TestCase):
    def test_orchestrator_exist(self):
        """
        Test Deve retornar a reposta vádida.
        """
        user_messages = [
            "Mostre a distribuição do tempo do ciclo em abril de 2023.",
        ]

        response = execute(user_messages)
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main(verbosity=2)