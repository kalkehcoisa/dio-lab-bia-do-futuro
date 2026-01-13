from dotenv import load_dotenv
load_dotenv()

import gradio as gr

from data import DataManager
from extraction import DataExtractor
from llm import LLMManager
from validation import DataValidator


data_manager = DataManager()
data_extractor = DataExtractor()
data_validator = DataValidator()
llm_manager = LLMManager()


def chat_handler(message, history, historico, usuario):
    # 2. Detectar novos dados
    novos_dados = data_extractor.detectar_novos_dados(message)

    if novos_dados:
        valido, erro = data_validator.validar_resposta(novos_dados, mensagem_original=message)
        if not valido:
            historico.append((message, f"{erro}"))
        else:
            historico.append((message, novos_dados))

    # 3. Apenas conversa (sem persistência)
    fatos = data_extractor.extrair_fatos_permitidos(usuario)
    resposta_llm = llm_manager.gerar_resposta(message, fatos)

    historico.append((message, resposta_llm))
    return resposta_llm



# Interface Gradio
with gr.Blocks(title="Assessor Financeiro Pessoal") as app:
    # Estado inicial
    historico = gr.State([])
    usuario = gr.State(data_manager.carregar_usuario())

    chatbot = gr.Chatbot(
        height=400,
        value=[{
                "role": "assistant",
                "content": "Olá! 👋\nSou a BIA, sua assistente financeira.\nComo posso te ajudar hoje?"
            }]
    )
    msg = gr.Textbox(
        label="Mensagem",
        placeholder="Ex: minha renda mensal agora é 6500 reais"
    )
    gr.ChatInterface(
        chatbot=chatbot,
        title="#Assessor Financeiro Pessoal",
        description="O agente identifica novos dados, valida e atualiza seu perfil com segurança.",
        textbox=msg,
        additional_inputs=[usuario],
        fn=chat_handler,
        save_history=True,
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True
    )
