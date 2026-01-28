from dotenv import load_dotenv
load_dotenv()

import gradio as gr

from agent import FinancialAgent

agent = FinancialAgent()


def render_user_data(show: bool, user: dict):
    show = not show
    btn_label = "❌ Ocultar dados" if show else "📄 Mostrar meus dados"
    if not show:
        return (
            show,
            user,
            gr.update(visible=show),
            btn_label
        )

    if not user:
        return (
            show,
            user,
            gr.update(visible=show),
            btn_label
        )

    lines = ["### 📋 Dados do Usuário\n"]
    print(user)
    for key, value in user.items():
        if key == "metas" and isinstance(value, list):
            lines.append("**Metas:**")
            for i, meta in enumerate(value, 1):
                desc = meta.get("meta", "Meta")
                val = meta.get("valor_necessario")
                prazo = meta.get("prazo")

                line = f"- {i}. {desc}"
                if val:
                    line += f" — R$ {val:,.2f}"
                if prazo:
                    line += f" (até {prazo})"
                lines.append(line)
        else:
            lines.append(f"**{key.replace('_', ' ').title()}**: {value}")

    return (
        show,
        user,
        gr.update(visible=show, value="\n\n".join(lines)),
        btn_label
    )


def chat_handler(message, history, user_state):
    llm_answer = agent.process_message(
        user_message=message,
        history=history,
    )
    return llm_answer, agent.user.copy()


# Interface Gradio
with gr.Blocks(title="Assessor Financeiro Pessoal") as app:
    user_state = gr.State(agent.user)

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
        additional_inputs=[user_state],
        additional_outputs=[user_state],
    )

    with gr.Group():
        toggle_data_state = gr.State(False)
        with gr.Row():
            gr.Column(scale=2)
            with gr.Column(scale=1):
                toggle_data = gr.Button("📄 Mostrar dados")
            gr.Column(scale=2)

        with gr.Row():
            with gr.Column(scale=3):
                user_data_box = gr.Markdown()

        toggle_data.click(
            fn=render_user_data,
            inputs=(toggle_data_state, user_state),
            outputs=(toggle_data_state, user_state, user_data_box, toggle_data),
        )

if __name__ == "__main__":
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        debug=True,
        show_error=True,
    )
