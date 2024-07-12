from langchain_community.agents.openai_assistant import OpenAIAssistantV2Runnable
from langchain.memory import ChatMessageHistory
from langchain.agents import AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory

instructions_function = '''Você é um assistante profissional em O2C e vai chamar a function O2C.
Não responda todos os campos de uma vez, Faça perguntas em uma conversa discreta e amigavel para preencher todos os campos.

As datas todas são de 2023
'''

tools = [
   {
      "type":"function",
      "function":{
         "name":"O2C",
         "description":"Modelo de payload",
         "parameters":{
            "type":"object",
            "properties":{
               "agci":{
                  "type":"object",
                  "properties":{
                     "type":{
                        "type":"string",
                        "description":"Tipo de análise",
                        "enum":[
                           "agci"
                        ]
                     },
                     "context_name":{
                        "type":"string",
                        "description":"Nome do contexto",
                        "enum":[
                           "O2C"
                        ]
                     },
                     "dashboard":{
                        "type":"string",
                        "description":"Nome do dashboard",
                        "enum":[
                           "Visão Geral",
                           "Análise do Ciclo da Ordem de Venda",
                           "Análise de Recebimento de pagamentos",
                           "Ordem de Venda Perfeita (Perfect SO)",
                           "Envios no prazo (“on-time shipment”)",
                           "Operação contas a receber",
                           "Análise de automação",
                           "Impacto na Receita"
                        ]
                     },
                     "main_keywords":{
                        "type":"array",
                        "items":{
                           "type":"string"
                        },
                        "description":"Principais palavras-chave"
                     },
                     "user_requested_unit":{
                        "type":"string",
                        "description":"Unidade solicitada pelo usuário",
                        "enum":[
                           "porcentagem"
                        ]
                     }
                  },
                  "required":[
                     "type",
                     "context_name",
                     "dashboard",
                     "main_keywords",
                     "user_requested_unit"
                  ]
               },
               "tempo":{
                  "type":"object",
                  "properties":{
                     "type":{
                        "type":"string",
                        "description":"Tipo de análise de tempo",
                        "enum":[
                           "tempo"
                        ]
                     },
                     "mode":{
                        "type":"string",
                        "description":"Modo de análise"
                     },
                     "DATE":{
                        "type":"string",
                        "description":"Intervalo de datas no formato DD/MM/AAAA-DD/MM/AAAA"
                     },
                     "start_date":{
                        "type":"string",
                        "format":"date",
                        "description":"Data de início no formato AAAA-MM-DD"
                     },
                     "end_date":{
                        "type":"string",
                        "format":"date",
                        "description":"Data de término no formato AAAA-MM-DD"
                     }
                  },
                  "required":[
                     "type",
                     "mode",
                     "DATE",
                     "start_date",
                     "end_date"
                  ]
               }
            },
            "required":[
               "agci",
               "tempo"
            ]
         }
      }
   }
]

class AssistantScopeManager:
     def __init__(self):
        self.assistant = OpenAIAssistantV2Runnable.create_assistant(
            name="langchain assistant-0",
            instructions=instructions_function,
            tools=tools,
            model="gpt-3.5-turbo",
            as_agent=True,
        )

        self.assistant_executor = AgentExecutor(
            agent=self.assistant,
            tools=tools,
            return_intermediate_steps=True,
            verbose=True
        )

     async def execute(self, query: str):
        return await self.assistant_executor.ainvoke({"input": query},
                                                         config={"configurable": {"session_id": "<foo>"}})