import gradio as gr

import data
import extraction
import llm
import validation


# Estado inicial
usuario = gr.State(data.carregar_usuario())
pendente_confirmacao = gr.State(None)


def eh_confirmacao(texto: str) -> bool:
    texto = texto.lower().strip()
    return texto in {"sim", "confirmo", "ok", "pode salvar", "pode"}


def formatar_confirmacao(dados: dict) -> str:
    linhas = ["Identifiquei as seguintes informações:"]
    for k, v in dados.items():
        linhas.append(f"- {k}: {v}")
    linhas.append("\nPosso salvar isso? (sim / não)")
    return "\n".join(linhas)


# Lógica principal
def chat_handler(mensagem, historico, usuario, pendente_confirmacao):
    # 1. Se há confirmação pendente
    if pendente_confirmacao:
        if eh_confirmacao(mensagem):
            novos_dados = pendente_confirmacao
            usuario = data.aplicar_atualizacoes(usuario, novos_dados)
            data.salvar_usuario(usuario)
            pendente_confirmacao = None

            fatos = extraction.extrair_fatos_permitidos(usuario)
            resposta_llm = llm.gerar_resposta(mensagem, fatos)

            historico.append(
                (mensagem, "Dados confirmados e salvos.\n\n" + data.resumo_usuario(usuario))
            )
        else:
            pendente_confirmacao = None
            historico.append(
                (mensagem, "Ok, não salvei nenhuma informação.")
            )
        return historico, usuario, pendente_confirmacao

    # 2. Detectar novos dados
    novos_dados = extraction.detectar_novos_dados(mensagem)

    if novos_dados:
        valido, erro = validation.validar_resposta(novos_dados, mensagem_original=mensagem)
        if not valido:
            historico.append((mensagem, f"{erro}"))
            return historico, usuario, pendente_confirmacao

        pendente_confirmacao = novos_dados
        historico.append(
            (mensagem, formatar_confirmacao(novos_dados))
        )
        return historico, usuario, pendente_confirmacao

    # 3. Apenas conversa (sem persistência)
    fatos = extraction.extrair_fatos_permitidos(usuario)
    resposta_llm = llm.gerar_resposta(mensagem, fatos)

    historico.append((mensagem, resposta_llm))
    return historico, usuario, pendente_confirmacao



# Interface Gradio
with gr.Blocks(title="Assessor Financeiro Pessoal") as app:
    gr.Markdown("#Assessor Financeiro Pessoal")
    gr.Markdown(
        "O agente identifica novos dados, valida e atualiza seu perfil com segurança."
    )

    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(
        label="Mensagem",
        placeholder="Ex: minha renda mensal agora é 6500 reais"
    )

    msg.submit(
        chat_handler,
        inputs=[msg, chatbot, usuario, pendente_confirmacao],
        outputs=[chatbot, usuario, pendente_confirmacao]
    )



if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)
