import streamlit as st
import pandas as pd
from database import engine, SessionLocal
from models import Base, Tarefa, Usuario
from datetime import datetime

Base.metadata.create_all(bind=engine)

session = SessionLocal()


st.set_page_config(
    page_title="Pauta - M&E",
    page_icon="logo.png",
    layout="wide"
)

# ===== ESTILO VISUAL PROFISSIONAL =====
st.markdown("""
<style>

/* Fundo geral */
body {
    background: #0B1120;
}

/* Container principal */
.block-container {
    padding-top: 1.3rem;
}

/* Títulos */
h1 {
    font-size: 34px;
    font-weight: 700;
}
h2, h3 {
    color: #E5E7EB;
}

/* Cards (KPIs estilo painel - igual print 2) */
div[data-testid="metric-container"] {
    background-color: #1F2937;
    padding: 18px 20px;
    border-radius: 14px;
    border: 1px solid #374151;
    box-shadow: none;
    backdrop-filter: none;
    transition: none;
}

/* Remover efeito hover */
div[data-testid="metric-container"]:hover {
    transform: none;
    box-shadow: none;
}

/* Ajuste do texto */
div[data-testid="metric-container"] label {
    font-size: 13px;
    color: #9CA3AF;
}

div[data-testid="metric-container"] div {
    font-size: 26px;
    font-weight: 600;
    color: #F3F4F6;
}

/* Botões */
.stButton {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 1rem;
}

/* Garante que o container interno do Streamlit também centralize */
div[data-testid="stVerticalBlock"] > div.stButton {
    display: flex;
    justify-content: center;
}


.stButton>button {
    border-radius: 10px;
    background: linear-gradient(90deg, #2563EB, #1D4ED8);
    color: white;
    font-weight: 600;
    border: none;
    padding: 10px 24px;
    width: auto;
    display: block;
    margin: 0 auto;
}
.stButton>button:hover {
    transform: scale(1.03);
    background: linear-gradient(90deg, #1D4ED8, #1E40AF);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #0B1120);
}

/* Inputs */
input, textarea, .stSelectbox div {
    border-radius: 8px !important;
}

/* Tabela */
div[data-testid="stDataEditor"] {
    border-radius: 12px;
    border: 1px solid #374151;
    background-color: #020617;
}

/* Destaque hover linhas */
[data-testid="stDataEditor"] div[role="row"]:hover {
    background-color: #111827 !important;
}

/* Mensagens */
.stAlert {
    border-radius: 10px;
}

/* ===== CARDS CUSTOM (igual print 2) ===== */
.card {
    background-color: #1F2937;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #374151;
}

.card-title {
    font-size: 13px;
    color: #9CA3AF;
    margin-bottom: 6px;
    text-align: center;
}

.card-value {
    font-size: 28px;
    font-weight: 600;
    color: #F3F4F6;
    text-align: center;
}

/* Botão centralizado dentro do card */
.login-card .stButton button {
    display: block;
    margin: 20px auto 0 auto;
    width: 60%;
}

/* ===== LAYOUT LOGIN FINAL CORRIGIDO (CANTO ESQUERDO) ===== */
.login-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url("sua_imagem.jpeg") no-repeat center center;
    background-size: cover;
    opacity: 0.3;
    z-index: -1;
}

/* Estilo do Card (Formulário) */
[data-testid="stForm"] {
    background-color: rgba(31, 41, 55, 0.95) !important;
    padding: 40px !important;
    border-radius: 16px !important;
    border: 1px solid #374151 !important;
    backdrop-filter: blur(6px) !important;
}

/* CORREÇÃO DE VISIBILIDADE: Campos Brancos e Texto Escuro */
[data-testid="stWidgetLabel"] p {
    color: #E5E7EB !important;
}

/* Inputs padronizados (TODAS as telas) */
input, textarea, select {
    background-color: #1F2937 !important;
    color: #F3F4F6 !important;
    border: 1px solid #374151 !important;
}

/* Selectbox (dropdown) */
[data-baseweb="select"] > div {
    background-color: #1F2937 !important;
    color: #F3F4F6 !important;
    border: 1px solid #374151 !important;
}

/* Campo de texto interno (Streamlit wrapper) */
[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextArea"] textarea {
    background-color: #1F2937 !important;
    color: #F3F4F6 !important;
}

/* CORREÇÃO DO OLHINHO (Ícone de Senha) */
[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #FFFFFF !important;
    border-radius: 8px !important;
}

[data-testid="stTextInput"] button {
    background-color: transparent !important;
    border: none !important;
    color: #4B5563 !important;
    margin-right: 5px !important;
    z-index: 10 !important;
}

[data-testid="stTextInput"] svg {
    fill: #4B5563 !important;
}

/* Estilo do botão 'Entrar' */
[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    background: linear-gradient(90deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    border: none !important;
    padding: 10px !important;
    border-radius: 10px !important;
}

/* ===== CORREÇÃO SELECTBOX (remove borda estranha) ===== */
[data-baseweb="select"] > div {
    background-color: #1F2937 !important;
    color: #F3F4F6 !important;
    border: 1px solid #374151 !important;
    box-shadow: none !important;   /* remove sombra */
    outline: none !important;      /* remove contorno */
}

/* Remove efeito ao clicar */
[data-baseweb="select"] > div:focus,
[data-baseweb="select"] > div:active {
    box-shadow: none !important;
    outline: none !important;
    border: 1px solid #374151 !important;
}

/* Texto interno */
[data-baseweb="select"] span {
    color: #F3F4F6 !important;
}
</style>
""", unsafe_allow_html=True)

if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "lista"
if "tarefa_edicao_id" not in st.session_state:
    st.session_state.tarefa_edicao_id = None

# ===== BYPASS LOGIN: USUÁRIO FAKE ADMIN =====
class UsuarioFake:
    def __init__(self):
        self.nome = "Admin"
        self.perfil = "admin"

st.session_state.usuario = UsuarioFake()


usuario = st.session_state.usuario

st.sidebar.header("Menu")

if st.sidebar.button("Nova tarefa"):
    st.session_state.pagina = "nova"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Filtros")

if st.session_state.pagina == "lista":
    st.markdown("## 📊 Painel de Monitoramento de Atividades")
    st.caption("Acompanhe, edite e gerencie as tarefas em tempo real")

    col1, col2, col3, col4 = st.columns(4, gap="large")

    tarefas = session.query(Tarefa).all()
    df = pd.DataFrame([t.__dict__ for t in tarefas])

    if not df.empty:
        df = df.drop(columns=["_sa_instance_state"])

    if not df.empty:
        total = len(df)
        concluidas = len(df[df["status"] == "Concluído"])
        andamento = len(df[df["status"] == "Em andamento"])

        # cálculo automático de atrasadas (prazo vencido e não concluído)
        hoje = datetime.now().date()
        df["prazo_data"] = pd.to_datetime(df["prazo"], errors="coerce").dt.date
        atrasadas = len(df[(df["prazo_data"] < hoje) & (df["status"] != "Concluído")])

        # ===== CARDS CUSTOMIZADOS =====
        col1, col2, col3, col4 = st.columns(4, gap="large")

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📌 Total</div>
                <div class="card-value">{total}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">✅ Concluídas</div>
                <div class="card-value">{concluidas}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🚧 Em andamento</div>
                <div class="card-value">{andamento}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">⚠️ Atrasadas</div>
                <div class="card-value">{atrasadas}</div>
            </div>
            """, unsafe_allow_html=True)

    status_filtro = st.sidebar.multiselect(
        "Status",
        ["Em andamento", "Concluído", "Atrasado"],
        placeholder="Selecione"
    )

    responsavel_filtro = st.sidebar.multiselect(
        "Responsável",
        df["responsavel"].unique() if not df.empty else [],
        placeholder="Selecione"
    )

    df_filtrado = df.copy()

    if status_filtro:
        df_filtrado = df_filtrado[df_filtrado["status"].isin(status_filtro)]

    if responsavel_filtro:
        df_filtrado = df_filtrado[df_filtrado["responsavel"].isin(responsavel_filtro)]

    st.markdown("### 📋 Lista de Atividades")

    if not df_filtrado.empty:
        # ===== STATUS VISUAL =====
        def status_visual(valor):
            if valor == "Em andamento":
                return "🟡 Em andamento"
            elif valor == "Concluído":
                return "🟢 Concluído"
            elif valor == "Atrasado":
                return "🔴 Atrasado"
            else:
                return "🟡 Em andamento"

        df_filtrado["status_visual"] = df_filtrado["status"].apply(status_visual)

        # Definir ordem das colunas
        colunas_ordem = [
            "id",
            "status_visual",
            "prioridade",
            "assunto",
            "acao",
            "descricao",
            "responsavel",
            "envolvidos",
            "prazo",
            "ultima_atualizacao",
            "observacoes",
            "data_criacao"
        ]

        # Reorganizar dataframe conforme ordem definida (somente colunas existentes)
        colunas_existentes = [col for col in colunas_ordem if col in df_filtrado.columns]
        df_filtrado = df_filtrado[colunas_existentes]

        # Converter coluna prazo para datetime (necessário para o editor de data)
        if "prazo" in df_filtrado.columns:
            df_filtrado["prazo"] = pd.to_datetime(df_filtrado["prazo"], errors="coerce")

        # ===== COLUNA DE AÇÃO (EDITAR) =====
        df_filtrado["editar"] = False
        df_filtrado["excluir"] = False

        edited_df = st.data_editor(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "status_visual": st.column_config.TextColumn(
                    "Status",
                    disabled=True
                ),
                "prioridade": st.column_config.SelectboxColumn(
                    "Prioridade",
                    options=["Baixa", "Média", "Alta"]
                ),
                "prazo": st.column_config.DateColumn(
                    "Prazo"
                ),
                "ultima_atualizacao": st.column_config.DatetimeColumn(
                    "Última Atualização",
                    disabled=True
                ),
                "data_criacao": st.column_config.DatetimeColumn(
                    "Data Criação",
                    disabled=True
                ),
                "id": st.column_config.NumberColumn(
                    "ID",
                    disabled=True
                ),
                "editar": st.column_config.CheckboxColumn(
                    "Editar",
                    help="Marque para editar"
                ),
                "excluir": st.column_config.CheckboxColumn(
                    "Excluir",
                    help="Marque para excluir"
                ),
            }
        )

        # Detectar seleção de edição (checkbox)
        if edited_df is not None:
            for i, row in edited_df.iterrows():
                if row.get("editar") is True:
                    st.session_state.tarefa_edicao_id = int(row["id"])
                    st.session_state.pagina = "editar"
                    st.rerun()

        if usuario.perfil in ["admin", "editor"]:
            if st.button("Salvar alterações"):
                for _, row in edited_df.iterrows():
                    tarefa = session.query(Tarefa).get(row["id"])
                    for col in df.columns:
                        if col in row and col not in ["editar", "excluir"]:
                            valor = row[col]

                            # Converter prazo de volta para string antes de salvar
                            if col == "prazo" and pd.notnull(valor):
                                valor = str(valor.date())

                            setattr(tarefa, col, valor)
                    tarefa.ultima_atualizacao = datetime.now()
                session.commit()
                st.success("Atualizado")

            if st.button("Excluir tarefas selecionadas"):
                ids_excluir = edited_df[edited_df["excluir"] == True]["id"].tolist()

                if ids_excluir:
                    for tarefa_id in ids_excluir:
                        tarefa = session.query(Tarefa).get(tarefa_id)
                        if tarefa:
                            session.delete(tarefa)

                    session.commit()
                    st.success("Tarefa(s) excluída(s) com sucesso!")
                    st.rerun()
                else:
                    st.warning("Nenhuma tarefa selecionada para exclusão.")

if st.session_state.pagina == "editar" and usuario.perfil in ["admin", "editor"]:
    st.title("Editar tarefa")

    tarefa = session.query(Tarefa).get(st.session_state.tarefa_edicao_id)

    if not tarefa:
        st.error("Tarefa não encontrada")
    else:
        with st.form("editar_tarefa"):
            assunto = st.text_input("Assunto", value=tarefa.assunto)
            descricao = st.text_area("Descrição", value=tarefa.descricao)
            acao = st.text_input("Ação", value=tarefa.acao)
            
            lista_responsaveis = [
                "Casagrande",
                "João Martins",
                "Luciano",
                "Paulo Arieiro",
                "Sigmar"
            ]

            responsavel = st.selectbox(
                "Responsável",
                lista_responsaveis,
                index=lista_responsaveis.index(tarefa.responsavel) if tarefa.responsavel in lista_responsaveis else 0
            )
            
            envolvidos = st.text_input("Envolvidos", value=tarefa.envolvidos)
            observacoes = st.text_area("Observações", value=tarefa.observacoes)

            status = st.selectbox(
                "Status",
                ["Em andamento", "Concluído", "Atrasado"],
                index=["Em andamento", "Concluído", "Atrasado"].index(tarefa.status if tarefa.status != "Novo" else "Em andamento")
            )

            prioridade = st.selectbox(
                "Prioridade",
                ["Baixa", "Média", "Alta"],
                index=["Baixa", "Média", "Alta"].index(tarefa.prioridade)
            )

            prazo = st.date_input("Prazo", value=pd.to_datetime(tarefa.prazo))

            submitted = st.form_submit_button("Salvar alterações")

            if submitted:
                tarefa.assunto = assunto
                tarefa.descricao = descricao
                tarefa.acao = acao
                tarefa.responsavel = responsavel
                tarefa.envolvidos = envolvidos
                tarefa.observacoes = observacoes
                tarefa.status = status
                tarefa.prioridade = prioridade
                tarefa.prazo = str(prazo)
                tarefa.ultima_atualizacao = datetime.now()

                session.commit()

                st.success("Tarefa atualizada")

                st.session_state.pagina = "lista"
                st.rerun()

if st.session_state.pagina == "nova" and usuario.perfil in ["admin", "editor"]:
    st.title("Nova tarefa")

    with st.form("nova_tarefa"):
        assunto = st.text_input("Assunto")
        descricao = st.text_area("Descrição")
        acao = st.text_input("Ação")
        responsavel = st.selectbox(
            "Responsável",
            [
                "Casagrande",
                "João Martins",
                "Luciano",
                "Paulo Arieiro",
                "Sigmar"
            ]
        )
        envolvidos = st.text_input("Envolvidos (separar por vírgula)")
        observacoes = st.text_area("Observações")

        prioridade = st.selectbox(
            "Prioridade",
            ["Baixa", "Média", "Alta"]
        )

        prazo = st.date_input("Prazo")

        submitted = st.form_submit_button("Criar")

        if submitted:
            nova = Tarefa(
                assunto=assunto,
                descricao=descricao,
                acao=acao,
                envolvidos=envolvidos,
                responsavel=responsavel,
                prazo=str(prazo),
                observacoes=observacoes,
                status="Em andamento",
                prioridade=prioridade,
            )
            session.add(nova)
            session.commit()
            st.success("Tarefa criada")

            st.session_state.pagina = "lista"
            st.rerun()

if st.sidebar.button("Sair"):
    st.session_state.usuario = None
    st.rerun()

# ================= FOOTER =================
st.markdown(
    '<div style="text-align:center;color:#9CA3AF;font-size:0.8rem;margin-top:1rem;">Desenvolvido por Casagrande para M&E Engenharia • 2026</div>',
    unsafe_allow_html=True
)
