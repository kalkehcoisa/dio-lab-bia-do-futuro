"""
Gerenciamento de dados do usuário
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

import config
from exceptions import DataLoadError, DataSaveError


class DataManager:
    """Gerenciador de dados do usuário"""

    def __init__(self, usuario_file: Path = config.USUARIO_FILE):
        self.usuario_file = usuario_file

    def carregar_usuario(self) -> Dict[str, Any]:
        """
        Carrega dados do usuário do arquivo JSON.

        Returns:
            Dict com dados do usuário

        Raises:
            DataLoadError: Se houver erro ao carregar dados
        """
        try:
            if not self.usuario_file.exists():
                usuario = self.usuario_padrao()
                self.salvar_usuario(usuario)
                return usuario

            with open(self.usuario_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            raise DataLoadError(f"Erro ao carregar usuário: {e}")

    def salvar_usuario(self, usuario: Dict[str, Any]) -> None:
        """
        Salva dados do usuário no arquivo JSON.

        Args:
            usuario: Dicionário com dados do usuário

        Raises:
            DataSaveError: Se houver erro ao salvar dados
        """
        try:
            # Atualiza timestamp
            usuario["ultima_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Cria diretório se não existir
            self.usuario_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.usuario_file, "w", encoding="utf-8") as f:
                json.dump(usuario, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise DataSaveError(f"Erro ao salvar usuário: {e}")

    def aplicar_atualizacoes(self, usuario: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Aplica atualizações ao perfil do usuário de forma segura.

        Args:
            usuario: Dicionário com dados atuais
            updates: Dicionário com atualizações

        Returns:
            Dicionário atualizado
        """
        for chave, valor in updates.items():
            if chave == "perfil_investidor":
                if isinstance(valor, str):
                    usuario["perfil_investidor"] = {
                        "valor": valor,
                        "confirmado": True
                    }
                else:
                    usuario["perfil_investidor"] = valor

            elif chave == "renda_mensal":
                usuario["renda_mensal"] = float(valor)

            elif chave == "metas":
                if not isinstance(usuario.get("metas"), list):
                    usuario["metas"] = []

                # Adiciona novas metas
                if isinstance(valor, list):
                    for meta in valor:
                        # Marca como confirmada
                        if isinstance(meta, dict):
                            meta["confirmado"] = True
                        usuario["metas"].append(meta)
                else:
                    usuario["metas"].append(valor)

            elif chave == "idade":
                usuario["idade"] = int(valor)

            elif chave == "profissao":
                usuario["profissao"] = str(valor)

            elif chave == "patrimonio_total":
                usuario["patrimonio_total"] = float(valor)

            elif chave == "reserva_emergencia_atual":
                usuario["reserva_emergencia_atual"] = float(valor)
            else:
                # Campo não reconhecido, mas permite extensibilidade
                usuario[chave] = valor

        return usuario

    def usuario_padrao(self) -> Dict[str, Any]:
        """
        Retorna estrutura padrão de dados do usuário.

        Returns:
            Dicionário com estrutura padrão
        """
        return {
            "nome": None,
            "idade": None,
            "profissao": None,
            "renda_mensal": None,
            "perfil_investidor": {
                "valor": None,
                "confirmado": False
            },
            "objetivo_principal": {
                "descricao": None,
                "confirmado": False
            },
            "patrimonio_total": None,
            "reserva_emergencia_atual": None,
            "aceita_risco": False,
            "metas": [],
            "ultima_atualizacao": None
        }

    def resumo_usuario(self, usuario: Dict[str, Any]) -> str:
        """
        Gera resumo formatado dos dados do usuário.

        Args:
            usuario: Dicionário com dados do usuário

        Returns:
            String formatada com resumo
        """
        if not usuario:
            return "Perfil ainda vazio."

        linhas = ["**Resumo do seu perfil:**\n"]

        # Informações básicas
        if usuario.get("nome"):
            linhas.append(f"**Nome**: {usuario['nome']}")
        if usuario.get("idade"):
            linhas.append(f"**Idade**: {usuario['idade']} anos")
        if usuario.get("profissao"):
            linhas.append(f"💼 **Profissão**: {usuario['profissao']}")
        if usuario.get("renda_mensal"):
            linhas.append(f"**Renda Mensal**: R$ {usuario['renda_mensal']:,.2f}")

        # Perfil de investidor
        perfil = usuario.get("perfil_investidor", {})
        if isinstance(perfil, dict) and perfil.get("valor"):
            status = "✅" if perfil.get("confirmado") else "⏳"
            linhas.append(f"{status} **Perfil Investidor**: {perfil['valor'].title()}")

        # Patrimônio
        if usuario.get("patrimonio_total"):
            linhas.append(f"**Patrimônio Total**: R$ {usuario['patrimonio_total']:,.2f}")
        if usuario.get("reserva_emergencia_atual"):
            linhas.append(f"**Reserva Emergência**: R$ {usuario['reserva_emergencia_atual']:,.2f}")

        # Metas
        metas = usuario.get("metas", [])
        if metas:
            linhas.append(f"\n**Metas ({len(metas)}):**")
            for i, meta in enumerate(metas, 1):
                if isinstance(meta, dict):
                    status = "✅" if meta.get("confirmado") else "⏳"
                    descricao = meta.get("meta", "Meta sem descrição")
                    valor = meta.get("valor_necessario", 0)
                    prazo = meta.get("prazo", "Sem prazo")
                    linhas.append(f"  {status} {i}. {descricao} - R$ {valor:,.2f} até {prazo}")

        # Última atualização
        if usuario.get("ultima_atualizacao"):
            linhas.append(f"\n**Última atualização**: {usuario['ultima_atualizacao']}")

        return "\n".join(linhas)

    def salvar_interacao(self, mensagem: str, resposta: str, dados_extraidos: Optional[Dict] = None) -> None:
        """
        Salva histórico de interações.

        Args:
            mensagem: Mensagem do usuário
            resposta: Resposta do agente
            dados_extraidos: Dados extraídos (opcional)
        """
        try:
            timestamp = datetime.now()
            filename = f"{timestamp.strftime('%Y-%m-%d_%H%M%S')}.json"
            filepath = config.INTERACOES_PATH / filename

            interacao = {
                "timestamp": timestamp.isoformat(),
                "mensagem": mensagem,
                "resposta": resposta,
                "dados_extraidos": dados_extraidos
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(interacao, f, ensure_ascii=False, indent=2)
        except Exception:
            # Não falha se não conseguir salvar histórico
            pass
