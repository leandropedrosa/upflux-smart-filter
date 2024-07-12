import json
from src.utils.utils_text import convert_from_not_iso_to_iso
from src.utils.utils_json import json_to_obj

from src.assistants.assistant_response import AssistantResponseManager
from src.service.bi_upflux_conector_service import UpFluxAPIConnector
from src.constants.constants import BI_UPFLUX_MODE, EXECUTION_MODE


class AssistantService:
    def _get_context_filters(self, discoverred_context, discoverred_dashboard, discoverred_main_keywords,
                             discoverred_request_unit, filters_api_upflux):
        # Set context filters according to format
        context_filters = [
            {
                "type": "agci",
                "context_name": discoverred_context,
                "dashboard": discoverred_dashboard,
                "main_keywords": discoverred_main_keywords,
                "user_requested_unit": discoverred_request_unit,
                # TODO: add "after_posprocess_unit" e apropriar instruções do assistant_0 para não preencher este.
            }
        ]
        context_filters = context_filters + filters_api_upflux

        # Set fake context informations
        context_informations = {
            "itens_number": "199433",  # Fix: we should get this from ask_gpt
        }
        return context_filters, context_informations

    async def _assistant_translator(self, answer_plus_info, messages):
        manager = AssistantResponseManager()
        response = await manager.execute(messages)

        return response

    def _assistant_payload_params(self, keywords):
        """
        ===Assistant_1===
        Assistente que analisa as principais keywords inferidas pelo assistant_1
        e retorna os payload_params e a unidade de medida associada a tais keywords.
        """

        ######### SIMULATING ASSISTANT_1 OUTPUT #########
        payloadParams_and_units = [
            {"after_posprocess_unit": "porcentagem"},
            {"api_upflux_unit": "porcentagem"},
            {
                "payload_json": "2_payload_full_oct.json",
                "component_number": 8,
                "conditions": {
                    "KPI": "Order Cycle Time"
                }
            }
        ]
        assistant_1_output = json.dumps(payloadParams_and_units)
        ######### SIMULATING ASSISTANT_1 OUTPUT #########

        return assistant_1_output

    def _gather_next_assist_input(self, processed_answer, scope_dict_new):
        answer_plus_info = {
            'main_keywords': scope_dict_new[0]['main_keywords'],
            'DATE': scope_dict_new[1]['DATE'],
            'user_requested_unit': scope_dict_new[0]['user_requested_unit'],
            'processed_answer': processed_answer
        }
        return answer_plus_info

    def _get_main_filters_from_context_filters(self, scope_dict):
        # Filter context_filters to include only "agci" and "tempo" types
        filtered_context_filters = [
            filter_obj for filter_obj in scope_dict["context_filters"]
            if filter_obj["type"] in {"agci", "tempo"}
        ]

        agci_filter = [f for f in filtered_context_filters if f["type"] == "agci"]
        tempo_filter = [f for f in filtered_context_filters if f["type"] == "tempo"]

        if len(agci_filter) != 1:
            print("[error] type = agci não foi encontrado ou existem muitos, porém é mandatório")
        if len(tempo_filter) != 1:
            print("[error] type = tempo não foi encontrado, porém é mandatório")

        return {"context_filters": agci_filter + tempo_filter}

    def _assist_and_procPayload(self, scope,
                                BEARER):  # o documento do assistant payload deve associar scope com parâmetros de payload
        bi_upflux = UpFluxAPIConnector(url=None, bearer=None, group_id="71df2074-7237-46e7-834d-ee9872f50dd6",
                                       mode=BI_UPFLUX_MODE)
        bi_upflux._set_bearer(BEARER)
        if EXECUTION_MODE == 'production':
            scope_dict = json_to_obj(scope)
            main_keywords_str = f"main_keywords = {scope_dict['context_filters'][0]['main_keywords']}"

            scope_dict = self._get_main_filters_from_context_filters(scope_dict)

            payParams_and_units = self._assistant_payload_params(main_keywords_str)

            after_posprocess_unit, api_upflux_unit, mapping_params = json_to_obj(payParams_and_units)
            processed_answer, filters_definitions = bi_upflux._ask_upflux_direct_payload(mapping_params,
                                                                                         after_posprocess_unit,
                                                                                         api_upflux_unit, scope_dict)

            if filters_definitions is not None:
                scope_dict_new, context_informations = self._get_context_filters(
                    discoverred_context=scope_dict['context_filters'][0]['context_name'],
                    discoverred_dashboard=scope_dict['context_filters'][0]['dashboard'],
                    discoverred_main_keywords=scope_dict['context_filters'][0]['main_keywords'],
                    discoverred_request_unit=scope_dict['context_filters'][0]['user_requested_unit'],
                    filters_api_upflux=filters_definitions
                )
            else:  # in generic functions filters is None. In there, we reuse previously values of filters and context_informations
                context_informations_new = {
                    "itens_number": "Unknown"
                }
                # If filter is None, it means that filters do not changed, so we can use the filters used in message_new
                scope_dict_new, context_informations = scope_dict, context_informations_new

            if "DATE" in scope_dict_new[1].keys() and filters_definitions is None:
                start_date = convert_from_not_iso_to_iso(scope_dict_new[1]["DATE"].split("-")[0])
                end_date = convert_from_not_iso_to_iso(scope_dict_new[1]["DATE"].split("-")[1])
                scope_dict_new[1] = {
                    "type": "tempo",
                    "mode": scope_dict_new[1]["mode"],
                    "DATE": scope_dict_new[1]["DATE"],
                    "start_date": start_date,
                    "end_date": end_date
                }

            answer_plus_info = self._gather_next_assist_input(processed_answer, scope_dict_new)

        return answer_plus_info, scope_dict_new, context_informations

    def _assistant_scope(self, message):
        """
        ===Assistant_0===
        Assistente que analisa a mensagem do usuário e retorna escopo de filtros.
        """
        ######### SIMULATING ASSISTANT_0 OUTPUT #########
        scope = {"context_filters":
            [
                {
                    "type": "agci",
                    "context_name": "O2C",
                    "dashboard": "Análise do Ciclo da Ordem de Venda",
                    "main_keywords": ["distribuição", "ordem do tempo de ciclo"],
                    "user_requested_unit": "porcentagem",
                },
                {
                    "type": "tempo",
                    "mode": "casos interligados",
                    "DATE": "01/04/2023-30/04/2023",
                    "start_date": "2023-04-01",
                    "end_date": "2023-04-30",
                },
            ]
        }
        assistant_0_output = json.dumps(scope)
        ######### SIMULATING ASSISTANT_0 OUTPUT #########

        return assistant_0_output

    def ask_assistants(self, messages, previous_scope, upflux_api_access_token):
        current_scope = self._assistant_scope(messages[-1])

        if "Reformule sua pergunta" in current_scope:
            # send "Reformule sua pergunta" to user, also return previous_scope as scope
            answer = "Reformule sua pergunta"
            current_scope = previous_scope

        else:
            answer_plus_info, current_scope, context_informations_new = self._assist_and_procPayload(current_scope,
                                                                                                     upflux_api_access_token)
            response_dict = self._assistant_translator(answer_plus_info, messages)
            answer = response_dict  # response_dict["choices"][0]["message"]["content"]

            # response =  {
            #     "message_text": answer,
            #     "usertype": "assistant",
            #     "context_filters": current_scope,
            #     "context_informations": context_informations_new
            #     }
        return answer, current_scope, context_informations_new