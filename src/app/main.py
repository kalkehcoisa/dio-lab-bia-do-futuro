from dotenv import load_dotenv
load_dotenv()

import gradio as gr

from agent import FinancialAgent

agent = FinancialAgent()


def chat_handler(message, history):
    llm_answer = agent.process_message(
        user_message=message,
        history=history
    )
    return llm_answer


# Interface Gradio
with gr.Blocks(title="Assessor Financeiro Pessoal") as app:
    chatbot = gr.Chatbot(
        height=400,
        value=[{
                "role": "assistant",
                "content": agent.welcome_message()
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
        fn=chat_handler,
        save_history=True,
    )


if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        show_error=True,
    )
