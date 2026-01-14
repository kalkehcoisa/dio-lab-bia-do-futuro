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

    def __init__(self, user_file: Path = config.USUARIO_FILE):
        self.user_file = user_file

    def save_interaction(self, user_message: str, answer: str, extracted_data: dict) -> None:
        """
        Salva histórico de interações.

        Args:
            user_message: Mensagem do usuário
            answer: Resposta do agente
            extracted_data: Dados extraídos (opcional)
        """
        try:
            timestamp = datetime.now()
            filename = f"{timestamp.strftime('%Y-%m-%d_%H%M%S')}.json"
            filepath = config.INTERACOES_PATH / filename

            interacao = {
                "timestamp": timestamp.isoformat(),
                "mensagem": user_message,
                "resposta": answer,
                "dados_extraidos": extracted_data
            }

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(interacao, f, ensure_ascii=False, indent=2)
        except Exception:
            # Não falha se não conseguir salvar histórico
            pass

    def default_user(self) -> dict:
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

    def load_user(self) -> dict:
        """
        Carrega dados do usuário do arquivo JSON.

        Returns:
            Dict com dados do usuário

        Raises:
            DataLoadError: Se houver erro ao carregar dados
        """
        try:
            if not self.user_file.exists():
                usuario = self.default_user()
                self.save_user(usuario)
                return usuario

            with open(self.user_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise DataLoadError(f"Erro ao decodificar JSON: {e}")
        except Exception as e:
            raise DataLoadError(f"Erro ao carregar usuário: {e}")

    def save_user(self, user: Dict[str, Any]) -> None:
        """
        Salva dados do usuário no arquivo JSON.

        Args:
            usuario: Dicionário com dados do usuário

        Raises:
            DataSaveError: Se houver erro ao salvar dados
        """
        try:
            # Atualiza timestamp
            user["ultima_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Cria diretório se não existir
            self.user_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.user_file, "w", encoding="utf-8") as f:
                json.dump(user, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise DataSaveError(f"Erro ao salvar usuário: {e}")

    def update_user(self, user: dict, extracted_data: dict) -> dict:
        """
        Atualiza o dicionário do usuário com os dados extraídos pela LLM.

        Regras:
        - Ignora campos com valor None
        - Atualiza apenas campos existentes
        - Evita duplicidade de metas (baseado no campo 'meta')
        """

        # Campos simples
        for field in (
            "renda_mensal",
            "perfil_investidor",
            "idade",
            "profissao",
            "patrimonio_total",
            "reserva_emergencia_atual",
        ):
            value = extracted_data.get(field)
            if value is not None:
                user[field] = value

        # Metas
        new_goals = extracted_data.get("metas")
        if new_goals:
            if "metas" not in user or not isinstance(user["metas"], list):
                user["metas"] = []

            existing_goals = {
                goal.get("meta", "").strip().lower(): goal
                for goal in user["metas"]
                if goal.get("meta")
            }

            for goal in new_goals:
                name = goal.get("meta")
                if not name:
                    continue

                key = name.strip().lower()

                if key not in existing_goals:
                    user["metas"].append(goal)
                else:
                    existing_goal = existing_goals[key]
                    for k, v in goal.items():
                        if v is not None:
                            existing_goal[k] = v

        return user

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
