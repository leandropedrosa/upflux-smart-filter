from langchain_community.agents.openai_assistant import OpenAIAssistantV2Runnable
from langchain.agents import AgentExecutor
from langchain.tools import DuckDuckGoSearchRun, Tool
import json

Dados_treinamento_input = {"input": [{

    "main_keywords": ["distribuição", "Order Cycle Time"],
    "DATE": '01/04/2023-30/04/2023',
    "user_requested_unit": "porcentagem",
    "processed_answer": [
        {'Count': 22269, 'MaxInclusive': False, 'Range': {'Min': 0.0, 'Max': 10.0},
         'RepresentativeValue': 0.26429224177832633},
        {'Count': 35047, 'MaxInclusive': False, 'Range': {'Min': 10.0, 'Max': 20.0},
         'RepresentativeValue': 0.41594369740917886},
        {'Count': 12413, 'MaxInclusive': False, 'Range': {'Min': 20.0, 'Max': 30.0},
         'RepresentativeValue': 0.14731957417011832},
        {'Count': 12091, 'MaxInclusive': False, 'Range': {'Min': 30.0, 'Max': 60.0},
         'RepresentativeValue': 0.1434980239499638},
        {'Count': 1932, 'MaxInclusive': False, 'Range': {'Min': 60.0, 'Max': 90.0},
         'RepresentativeValue': 0.02292930132092714},
        {'Count': 383, 'MaxInclusive': False, 'Range': {'Min': 90.0, 'Max': 120.0},
         'RepresentativeValue': 0.00454550849167448},
        {'Count': 124, 'MaxInclusive': False, 'Range': {'Min': 120.0, 'Max': 195.0115277777778},
         'RepresentativeValue': 0.0014716528798110588},
        {'Total_Values': 84259}
    ],

    "main_keywords": ["taxa", "envios atrasados", "itens de vendas", "Grupo de cliente"],
    "DATE": '01/01/2023-30/06/2023',
    "user_requested_unit": "porcentagem",
    "processed_answer": {
        'Total de itens': 227763.0,
        'Por categorias': {
            'Distr. Industrial': '222549 itens (97,71% do total de itens). A porcentagem de atraso nesses items é de 17,51% (38976.00000000001 itens).',
            'Distr. Varejo': '3684 itens (1,62% do total de itens). A porcentagem de atraso nesses items é de 14,25% (525.0 itens).',
            'Orgão Público': '1515 itens (0,67% do total de itens). A porcentagem de atraso nesses items é de 43,43% (658.0 itens).',
            'Distrib Geral': '15 itens (0,01% do total de itens). A porcentagem de atraso nesses items é de 0,0% (0.0 itens).'
        }
    },

    "main_keywords": ["valor", "Impacto Financeiro das devoluções"],
    "DATE": '01/03/2023-31/05/2023',
    "user_requested_unit": "reais",
    "processed_answer": [
        ['02/2023', 1069401.6199999999],
        ['03/2023', 3462697.5800000024],
        ['04/2023', 2291557.879999999],
        ['05/2023', 5158524.110000006],
        ['06/2023', 1265188.389999998],
        ['07/2023', 398559.9999999999]
    ],

    "main_keywords": ["número de itens", "ordens de vendas", "pagamento", "atrasado"],
    "DATE": '01/01/2023-30/06/2023',
    "user_requested_unit": "unidades",
    "processed_answer": [
        ['01/2023', 15.350877192982457],
        ['02/2023', 37.84490270113273],
        ['03/2023', 42.19795702712222],
        ['04/2023', 44.99871827736478],
        ['05/2023', 53.56542352325037],
        ['06/2023', 58.85613703236654]
    ]}]}

Dados_treinamento_output = {"expected answer": [
    "A distribuição do tempo do ciclo de pedidos em abril de 2023 é a seguinte:"

    "- 26,43% dos pedidos têm um tempo de ciclo entre 0 e 10 dias."
    "- 41,59% dos pedidos têm um tempo de ciclo entre 10 e 20 dias."
    "- 14,73% dos pedidos têm um tempo de ciclo entre 20 e 30 dias."
    "- 14,35% dos pedidos têm um tempo de ciclo entre 30 e 60 dias."
    "- 2,29% dos pedidos têm um tempo de ciclo entre 60 e 90 dias."
    "- 0,45% dos pedidos têm um tempo de ciclo entre 90 e 120 dias."
    "- 0,15% dos pedidos têm um tempo de ciclo entre 120 e 195 dias."

    "Esses valores são baseados em uma amostra de 84.259 pedidos",

    "Durante o período de 01/01/2023 a 30/06/2023, a taxa de envios atrasados de itens de vendas por Grupo de cliente é a seguinte:"

    "- Grupo de cliente Distr. Industrial: Dos 222.549 itens de vendas nessa categoria (97,71% do total de itens), 38.976 itens (17,51%) foram enviados com atraso."
    "- Grupo de cliente Distr. Varejo: Dos 3.684 itens de vendas nessa categoria (1,62% do total de itens), 525 itens (14,25%) foram enviados com atraso."
    "- Grupo de cliente Orgão Público: Dos 1.515 itens de vendas nessa categoria (0,67% do total de itens), 658 itens (43,43%) foram enviados com atraso."
    "- Grupo de cliente Distr. Geral: Dos 15 itens de vendas nessa categoria (0,01% do total de itens), nenhum item foi enviado com atraso."

    "Esses números são baseados em um total de 227.763 itens de vendas analisados durante o período mencionado.",

    "A soma total do Impacto Financeiro das devoluções por mês entre março e maio de 2023 é a seguinte:"

    "- Março de 2023: R$ 3.462.697,58"
    "- Abril de 2023: R$ 2.291.557,88"
    "- Maio de 2023: R$ 5.158.524,11"

    "Esses valores estão em reais (R$).",

    "Durante o período de 01/01/2023 a 30/06/2023, o número de itens de ordens de venda com pagamento atrasado por mês é o seguinte:"

    "- Janeiro de 2023: 15.350 itens (15,35% do total de itens)"
    "- Fevereiro de 2023: 37.845 itens (37,84% do total de itens)"
    "- Março de 2023: 42.198 itens (42,20% do total de itens)"
    "- Abril de 2023: 44.999 itens (45,00% do total de itens)"
    "- Maio de 2023: 53.565 itens (53,57% do total de itens)"
    "- Junho de 2023: 58.856 itens (58,86% do total de itens)"

    "Esses números representam a porcentagem de itens de ordens de venda com pagamento atrasado em relação ao total de itens durante cada mês."
]}

Dados_treinamento_input = json.dumps(Dados_treinamento_input, ensure_ascii=False, indent=4)

Dados_treinamento_output = json.dumps(Dados_treinamento_output, ensure_ascii=False, indent=4)

instructions = f"""Você é um profissional em questões de Order to Cash e analisa o contexto fornecido, 
                        Crie respostas curtas que somente respondam ao que foi pedido diretamente somente 
                        informando os valores dentro do intervalo de meses passado, mas contendo todas as 
                        informações fornecidas e perguntadas, não se limite a somente um formato de resposta, 
                        responda de acordo com o tipo de input
                        Por Exemplo, input: {Dados_treinamento_input}, output: {Dados_treinamento_output}
                        Substitua a resposta por Não Sei caso vc não saiba"""


def create_prompt(answer_plus_info):
    main_keywords = ', '.join(answer_plus_info["main_keywords"])
    date_range = answer_plus_info["DATE"]
    user_requested_unit = answer_plus_info["user_requested_unit"]

    # Processed answer formatting
    if isinstance(answer_plus_info["processed_answer"], dict):
        processed_answer = '\n'.join(
            [f"{key}: {value}" for key, value in answer_plus_info["processed_answer"].items()]
        )
    else:
        if isinstance(answer_plus_info["processed_answer"][0], dict):
            processed_answer = '\n'.join(
                [f"{key}: {value}" for item in answer_plus_info["processed_answer"] for key, value in item.items()]

            )
        elif len(answer_plus_info["processed_answer"][0]) > 1:
            processed_answer = '\n'.join(
                [f"{item[0]}: {item[1]}" for item in answer_plus_info["processed_answer"]]
            )
        else:
            processed_answer = '\n'.join(
                [f"{item[0]}" for item in answer_plus_info["processed_answer"]]
            )

    # Construir o prompt com as informações fornecidas
    prompt = (
        f"Análise:\n"
        f"Palavras-chave principais: {main_keywords}\n"
        f"Período de análise: {date_range}\n"
        f"Unidade solicitada pelo usuário: {user_requested_unit}\n"
        f"Resposta processada:\n{processed_answer}\n\n"
        f"Com base nas informações acima, forneça uma resposta detalhada ao usuário."
    )
    prompt = json.dumps(prompt, ensure_ascii=False, indent=4)

    return prompt


tools = Tool(
    name="BI response Preprocessing",
    func=create_prompt,
    description="Creates a pattern for the assistant to respond to the user's query, by receiving the query provided by the user and the response of a diffentent assistants"
)


class AssistantResponseManager:
    """
        Uma classe para gerenciar um assistente OpenAI usando OpenAIAssistantV2Runnable e AgentExecutor.

        Atributos:
        ----------
        tools : list
            Uma lista de ferramentas a serem usadas pelo assistente.
        model : str
            O modelo a ser usado pelo assistente.
        instructions : str
            O template de instruções para o assistente.
        assistant : OpenAIAssistantV2Runnable
            O assistente inicializado.
        create_assistant_executor : AgentExecutor
            O executor para rodar o assistente com as ferramentas e configurações definidas.

        Métodos:
        -------
        execute(query: str)
            Executa uma consulta usando o executor do assistente e retorna o resultado.
    """

    def __init__(self):
        self.tools = tools
        self.model = "gpt-3.5-turbo"
        self.instructions = instructions

        self.assistant = OpenAIAssistantV2Runnable.create_assistant(
            name="langchain assistant-3",
            instructions=self.instructions,
            tools=self.tools,
            model=self.model,
            as_agent=True
        )

        self.create_assistant_executor = AgentExecutor(
            agent=self.assistant,
            tools=self.tools,
            return_intermediate_steps=True,
            verbose=True
        )

    async def execute(self, query: str):
        return await self.create_assistant_executor.ainvoke({"content": query})