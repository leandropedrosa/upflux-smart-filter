import json
import os

from chatbot_api.src.service.orchestrator_service import AssistantService

interface_format_msg_list = [
    {
        "message_text": "Bom dia! Eu sou o UpBot e estou aqui para ajudar com "
                        "as suas perguntas sobre O2C (Order to Cash). "
                        f"O meu foco de análise padrão é o período entre {'2023-01-01'} e {'2023-06-30'}, "
                        "abordando casos interligados no contexto ´Visão Geral´. "
                        "Se desejar alterar o período, basta digitar  "
                        "´trocar para período de XX até XX´. "
                        "Para mudar o contexto, digite "
                        "´Trocar para o Contexto [XX]´. "
                        "Como posso ajudar você hoje?",
        "usertype": "assistant",
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
        ],
        "context_informations": {
            "itens_number": "199433",
        },
    },
]


def get_interface_style_user_msg(
        text,
        context_filters,
        context_informations=[],
        user_api_token=os.getenv("UPFLUX_API_BEARER"),
):
    message_new = {
        "message_text": text,
        "usertype": "user",
        "context_filters": context_filters,
        "context_informations": context_informations,
        "upflux_api_access_token": user_api_token,
    }
    return message_new


def get_interface_style_gpt_msg(
        text,
        context_filters,
        context_informations=[],
):
    message_new = {
        "message_text": text,
        "usertype": "assistant",
        "context_filters": context_filters,
        "context_informations": context_informations,
    }
    return message_new


def get_gpt_style_msg(role, content):
    message_new = {
        "role": role,
        "content": content
    }
    return message_new


def get_main_filters_from_context_filters(context_filters):
    # Find context
    context = [filter_obj["context_name"] for filter_obj in context_filters if filter_obj["type"] == "agci"]
    if len(context) == 1:
        context = context[0]
    else:
        print("[error] type = agci não foi encontrado ou existem muitos, porém é mandatório")

    # Find time filters
    time_filter = [filter_obj for filter_obj in context_filters if filter_obj["type"] == "tempo"]
    if len(time_filter) >= 1:
        time_filter = time_filter[0]
    else:
        print("[error] type = tempo não foi encontrado, porém é mandatório")

    return context, time_filter


def execute(user_messages: list, dump=False):
    """
     Conversation simulation:
       > Test message flow (Question-Answer).
       > It updates filters automatically.
       
    """
    upflux_api_access_token = os.getenv("UPFLUX_API_BEARER")
    question_id = "Unknown"
    context_informations_new = {"itens_number": "199433"}

    gpt_format_msg_list = []
    interface_format_UpBot_intro = interface_format_msg_list[0]
    gpt_format_UpBot_intro = get_gpt_style_msg(interface_format_UpBot_intro["usertype"], interface_format_UpBot_intro["message_text"])
    gpt_format_msg_list.append(gpt_format_UpBot_intro) # [UpBot_0]
    
    up_agent = AssistantService()
    for i, user_msg in enumerate(user_messages):
        # --- Getting scope from last message (i.e. mandatory filters; e.g. context and period)
        last_scope = interface_format_msg_list[-1]["context_filters"]
        
        # --- Dealing with user message
        question = user_msg

        question_interface_format = get_interface_style_user_msg(question, last_scope, context_informations=[])
        interface_format_msg_list.append(question_interface_format)

        msg_gpt_format = get_gpt_style_msg(question_interface_format['usertype'], question_interface_format['message_text'])
        gpt_format_msg_list.append(msg_gpt_format) # thread msgs

        # --- Dealing with UpBot message
        answer, scope, context_informations_new = up_agent.ask_assistants(gpt_format_msg_list, last_scope, upflux_api_access_token)

        answer_interface_format = get_interface_style_gpt_msg(answer, scope, context_informations_new)
        interface_format_msg_list.append(answer_interface_format)

        answer_gpt_format = get_gpt_style_msg(answer_interface_format['usertype'], answer_interface_format['message_text'])
        gpt_format_msg_list.append(answer_gpt_format)
        
        # --- Terminal visualization
        print("\n\n" + "=" * 80)
        print(f"Q{i+1} - {question}")
        if dump:
            print(f"Dump: {json.dumps(question_interface_format, indent=2, ensure_ascii=False)}")

        print(f"R{i+1} - {answer}")
        if dump:
            print(f"Dump: {json.dumps(answer_interface_format, indent=2, ensure_ascii=False)}")
        
        

    print("\n\n================================ Simulação da Conversa =============================")
    for i, msg in enumerate(interface_format_msg_list):
        print(i+1, msg["usertype"], ":")
        print(i+1, msg["message_text"])
        print("\n")
