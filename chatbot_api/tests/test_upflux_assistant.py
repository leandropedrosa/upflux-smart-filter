import unittest
import os
from unittest.mock import patch

from chatbot_api.src.service.orchestrator_service import AssistantService
from chatbot_api.src.service.bi_upflux_conector_service import UpFluxAPIConnector


class TestUpFluxAssistant(unittest.TestCase):

    def setUp(self):
        self.bi_upflux = UpFluxAPIConnector(
            url=None,
            bearer=None,
            group_id="71df2074-7237-46e7-834d-ee9872f50dd6",
            mode="get_request_specific_component"
        )
        self.assistant = AssistantService(self.bi_upflux, 'production')

    @patch('os.getenv', return_value='fake_bearer_token')
    def test_get_context_filters(self, mock_getenv):
        context = "O2C"
        filters_api_upflux = [
            {
                "type": "tempo",
                "mode": "casos interligados",
                "start_date": "2023-01-01",
                "end_date": "2023-06-30",
            }
        ]
        context_filters, context_informations = self.assistant._get_context_filters(context, filters_api_upflux)

        self.assertEqual(context_informations["itens_number"], "199433")
        self.assertEqual(context_filters[0]["context_name"], "O2C")

    @patch('os.getenv', return_value='fake_bearer_token')
    def test_ask_assistants(self, mock_getenv):
        messages = ["Hello"]
        previous_scope = {
            "context_filters": [
                {
                    "type": "agci",
                    "context_name": "O2C",
                },
                {
                    "type": "tempo",
                    "mode": "casos interligados",
                    "start_date": "2023-01-01",
                    "end_date": "2023-06-30",
                },
            ]
        }
        upflux_api_access_token = 'fake_bearer_token'

        with patch.object(self.assistant, 'assistant_translator',
                          return_value={"choices": [{"message": {"content": "Translated message"}}]}):
            with patch.object(self.assistant, '_assistant_payload_param', return_value=("json_answer", previous_scope)):
                answer, current_scope = self.assistant.ask_assistants(messages, previous_scope, upflux_api_access_token)
                self.assertEqual(answer, "Translated message")
                self.assertEqual(current_scope, previous_scope)

    def test_execute(self):
        user_messages = ["Trocar para o Contexto O2C"]
        execute(user_messages, dump=True)


if __name__ == '__main__':
    unittest.main()