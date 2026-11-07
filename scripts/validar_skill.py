#!/usr/bin/env python3
"""Valida estrutura, contrato e documentação da skill, sem rede, dependências ou mutações."""

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gerar_documentos import divergencias  # noqa: E402

NOME = "skill-saas-billing-mf"
VERSAO = "1.0.0"
OBRIGATORIOS = """
SKILL.md README.md CHANGELOG.md agents/openai.yaml
contracts/schema-manifest.yaml contracts/catalogo-tabelas.md contracts/dicionario-dados.md
contracts/relacionamentos.md contracts/indices-restricoes.md contracts/estados-assinatura.md
contracts/regras-financeiras.md contracts/eventos-dominio.md contracts/api-publica-openapi.yaml
contracts/contratos-compatibilidade.md
references/arquitetura-modular.md references/instalacao-projeto-novo.md references/adequacao-projeto-existente.md
references/isolamentos-tenants.md references/provedores-pagamento.md references/seguranca-lgpd.md
references/fluxo-consultivo.md references/criterios-aceitacao.md references/trilha-modulos.md
templates/adr-modulo.md templates/matriz-aderencia.md templates/plano-migracao.md templates/checklist-review.md
templates/seed-planos-exemplo.md templates/evidencias-testes.md templates/registro-aplicacao.yaml
templates/mapeamento-compatibilidade.yaml
tests/test_schema_manifest.py tests/test_references.py tests/test_laboratorio_sqlite.py
tests/fixtures/esquema-esperado.json tests/fixtures/projetos-exemplo.md
scripts/validar_skill.py scripts/gerar_documentos.py
docs/revisao-prompt.md docs/relatorio-entrega-1.0.0.md
""".split()

TABELAS = """planos planos_versoes planos_precos funcionalidades planos_funcionalidades planos_limites
assinaturas assinaturas_itens assinaturas_consumos provedores_pagamento faturas pagamentos adicionais cupons
cupons_utilizacoes faturas_itens assinaturas_historicos assinaturas_alteracoes pagamentos_eventos
pagamentos_reembolsos consumos_eventos tenants_beneficios planos_adicionais planos_precos_provedores""".split()

# Requisitos do contrato, mantidos aqui de propósito para o manifesto não validar a si mesmo.
COLUNAS_ESSENCIAIS = {
    "planos": "nome slug publico ativo deleted_at",
    "planos_versoes": "plano_id numero_versao status trial_dias",
    "planos_precos": "plano_versao_id periodicidade moeda valor",
    "funcionalidades": "codigo nome",
    "planos_funcionalidades": "plano_versao_id funcionalidade_id habilitado",
    "planos_limites": "plano_versao_id recurso limite periodicidade",
    "assinaturas": "tenant_id plano_versao_id plano_preco_id status valor_contratado moeda periodo_inicio periodo_fim",
    "assinaturas_itens": "tenant_id assinatura_id adicional_id quantidade valor_unitario valor_total",
    "assinaturas_consumos": "tenant_id assinatura_id recurso periodo_inicio periodo_fim quantidade_utilizada",
    "provedores_pagamento": "nome codigo ambiente ativo",
    "faturas": "tenant_id assinatura_id numero competencia vencimento valor_total moeda status",
    "pagamentos": "tenant_id fatura_id provedor_pagamento_id chave_idempotencia valor moeda status",
    "adicionais": "codigo recurso quantidade_recurso valor periodicidade",
    "cupons": "codigo tipo_desconto valor_desconto valido_inicio valido_fim",
    "cupons_utilizacoes": "cupom_id tenant_id assinatura_id valor_desconto_aplicado",
    "faturas_itens": "tenant_id fatura_id tipo_item valor_total moeda",
    "assinaturas_historicos": "tenant_id assinatura_id tipo_evento ocorrido_em",
    "assinaturas_alteracoes": "tenant_id assinatura_id tipo_alteracao status solicitado_em",
    "pagamentos_eventos": "provedor_pagamento_id tenant_id chave_deduplicacao tipo recebido_em status_processamento tentativas",
    "pagamentos_reembolsos": "tenant_id pagamento_id valor moeda status",
    "consumos_eventos": "tenant_id assinatura_id recurso quantidade ocorrido_em chave_idempotencia",
    "tenants_beneficios": "tenant_id tipo_beneficio inicio justificativa",
    "planos_adicionais": "plano_versao_id adicional_id habilitado",
    "planos_precos_provedores": "plano_preco_id provedor_pagamento_id preco_externo_id status",
}
UNICOS_ESSENCIAIS = {
    "planos": [["slug"]],
    "planos_versoes": [["plano_id", "numero_versao"]],
    "planos_precos": [["plano_versao_id", "periodicidade", "moeda"]],
    "funcionalidades": [["codigo"]],
    "planos_funcionalidades": [["plano_versao_id", "funcionalidade_id"]],
    "planos_limites": [["plano_versao_id", "recurso", "periodicidade"]],
    "assinaturas_consumos": [["assinatura_id", "recurso", "periodo_inicio", "periodo_fim"]],
    "provedores_pagamento": [["codigo", "ambiente"]],
    "faturas": [["numero"]],
    "pagamentos": [["chave_idempotencia"]],
    "adicionais": [["codigo"]],
    "cupons": [["codigo"]],
    "pagamentos_eventos": [["provedor_pagamento_id", "chave_deduplicacao"]],
    "consumos_eventos": [["tenant_id", "chave_idempotencia"]],
    "planos_adicionais": [["plano_versao_id", "adicional_id"]],
    "planos_precos_provedores": [["provedor_pagamento_id", "preco_externo_id"]],
}
STATUS_ASSINATURA = {"pendente", "trial", "ativa", "inadimplente", "suspensa", "cancelamento_agendado", "cancelada", "expirada"}
SECOES_ADR = ["Problema", "Alternativas", "Decisão recomendada", "Impacto nas 24 entidades", "Rollback", "Contratos", "Segurança", "Migração", "Testes", "Evidências de aprovação"]
PROIBIDOS_API = ["tenant_id", "plano_id", "plano_versao_id", "preco_externo_id", "configuracao_referencia", "provedor_pagamento_id", "assinatura_externa_id"]
NOMES_DE_PROJETO = ["MindFlow", "app-mind-flow", "Pipefy"]
PALAVRAS_DINHEIRO = ("valor", "subtotal", "desconto", "prorrateamento")


def validar_manifesto(m):
    erros = []
    if not re.fullmatch(r"\d+\.\d+\.\d+", str(m.get("schema_version", ""))):
        erros.append("schema_version semântico ausente")
    tabelas = m.get("tabelas", [])
    nomes = [t.get("nome") for t in tabelas]
    if len(tabelas) != 24:
        erros.append(f"Manifesto deve ter 24 tabelas; encontradas {len(tabelas)}")
    for nome in sorted({n for n in nomes if nomes.count(n) > 1}):
        erros.append(f"Tabela duplicada: {nome}")
    for nome in TABELAS:
        if nome not in nomes:
            erros.append(f"Tabela obrigatória ausente: {nome}")
    if sum(t.get("natureza") == "nuclear" for t in tabelas) != 15 or sum(t.get("natureza") == "complementar" for t in tabelas) != 9:
        erros.append("Devem existir 15 tabelas nucleares e 9 complementares")

    enums = m.get("enumeracoes", {})
    faltantes = STATUS_ASSINATURA - set(enums.get("status_assinatura", []))
    if faltantes:
        erros.append(f"Status de assinatura ausente: {', '.join(sorted(faltantes))}")
    externas = set(m.get("tabelas_externas", []))
    fase_de = {t.get("nome"): t.get("fase") for t in tabelas}
    fases = m.get("fases", [])
    codigos = [f.get("codigo") for f in fases]
    if codigos != [f"{i:02d}" for i in range(8)]:
        erros.append("Fases devem ser 00 a 07, em ordem")
    for f in fases:
        for campo in ("modulo", "pre_condicoes", "gate"):
            if not f.get(campo):
                erros.append(f"Fase {f.get('codigo')} sem {campo}")
        if sorted(f.get("tabelas", [])) != sorted(n for n, x in fase_de.items() if x == f.get("codigo")):
            erros.append(f"Fase {f.get('codigo')} diverge das tabelas")

    for t in tabelas:
        nome = t.get("nome")
        colunas = {c.get("nome"): c for c in t.get("colunas", [])}
        if len(colunas) != len(t.get("colunas", [])):
            erros.append(f"{nome}: coluna duplicada")
        if colunas.get("id", {}).get("tipo") != "bigint" or colunas.get("id", {}).get("nulo") is not False:
            erros.append(f"{nome}: PK id ausente ou inválida")
        if "created_at" not in colunas:
            erros.append(f"{nome}: created_at ausente")
        if "updated_at" not in colunas and not t.get("excecao_timestamps"):
            erros.append(f"{nome}: updated_at ausente sem exceção justificada")
        if "deleted_at" in colunas and t.get("nome") != "planos":
            erros.append(f"{nome}: soft delete sem justificativa no contrato")
        for essencial in COLUNAS_ESSENCIAIS.get(nome, "").split():
            if essencial not in colunas:
                erros.append(f"{nome}: coluna essencial ausente: {essencial}")
        pares = [u.get("colunas") for u in t.get("unicos", [])]
        for par in UNICOS_ESSENCIAIS.get(nome, []):
            if par not in pares:
                erros.append(f"{nome}: unicidade ausente: {', '.join(par)}")
        if t.get("escopo") in ("tenant", "tenant_opcional") and "tenant_id" not in colunas:
            erros.append(f"{nome}: escopo por tenant sem tenant_id")
        for u in t.get("unicos", []) + t.get("indices", []):
            for c in u.get("colunas", []):
                if c not in colunas:
                    erros.append(f"{nome}: {u.get('nome')} usa coluna inexistente: {c}")
        for coluna, c in colunas.items():
            tipo = str(c.get("tipo", "")).lower()
            if "float" in tipo or "double" in tipo or tipo == "real":
                erros.append(f"{nome}.{coluna}: dinheiro ou número em ponto flutuante é proibido")
            eh_data = "date" in tipo or "timestamp" in tipo
            eh_flag = tipo == "boolean" or coluna.startswith("tipo_")
            if any(p in coluna for p in PALAVRAS_DINHEIRO) and not (eh_data or eh_flag) and tipo != "decimal(12,2)":
                erros.append(f"{nome}.{coluna}: valor monetário deve ser decimal(12,2)")
            if "enum" in c and c["enum"] not in enums:
                erros.append(f"{nome}.{coluna}: enumeração inexistente: {c['enum']}")
            if "fk" in c:
                alvo = c["fk"].get("tabela")
                if alvo not in fase_de and alvo not in externas:
                    erros.append(f"{nome}.{coluna}: FK para tabela inexistente: {alvo}")
                if alvo in fase_de and str(fase_de[alvo]) > str(t.get("fase")):
                    erros.append(f"{nome}.{coluna}: FK para tabela de fase posterior: {alvo}")
                for acao in ("on_delete", "on_update"):
                    if not c["fk"].get(acao):
                        erros.append(f"{nome}.{coluna}: FK sem {acao}")

    q = m.get("maquina_estados_assinatura", {})
    conhecidos = set(enums.get("status_assinatura", []))
    alcancados = set(q.get("iniciais", []))
    for tr in q.get("transicoes", []):
        if tr.get("de") not in conhecidos or tr.get("para") not in conhecidos:
            erros.append(f"Transição com status desconhecido: {tr.get('de')} -> {tr.get('para')}")
        if tr.get("de") in q.get("terminais", []):
            erros.append(f"Estado terminal com saída: {tr.get('de')}")
        alcancados.add(tr.get("para"))
    for estado in conhecidos:
        if estado not in alcancados:
            erros.append(f"Estado inalcançável: {estado}")
        if estado not in q.get("efeitos_acesso", {}):
            erros.append(f"Estado sem efeito de acesso: {estado}")
    return erros


def checksum_manifesto(raiz):
    conteudo = (Path(raiz) / "contracts/schema-manifest.yaml").read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(conteudo).hexdigest()


def validar_referencias(raiz):
    erros = []
    raiz = Path(raiz)
    for nome in OBRIGATORIOS:
        if not (raiz / nome).is_file():
            erros.append(f"Arquivo ausente: {nome}")
    for arquivo in raiz.rglob("*.md"):
        if ".git" in arquivo.parts:
            continue
        texto = arquivo.read_text(encoding="utf-8")
        for link in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", texto):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                continue
            caminho = (arquivo.parent / link.split("#", 1)[0]).resolve()
            if not caminho.is_relative_to(raiz.resolve()) or not caminho.exists():
                erros.append(f"Referência local inválida em {arquivo.relative_to(raiz)}: {link}")
    return erros


def validar_textos(raiz, m):
    erros = []
    raiz = Path(raiz)
    entrada = raiz / "SKILL.md"
    if entrada.is_file():
        cabecalho = re.match(r"\A---\n(.*?)\n---\n", entrada.read_text(encoding="utf-8"), re.DOTALL)
        if not cabecalho:
            erros.append("Frontmatter ausente ou inválido em SKILL.md")
        else:
            if not re.search(rf"^name: {NOME}$", cabecalho[1], re.MULTILINE):
                erros.append("Nome da skill divergente em SKILL.md")
            if not re.search(r"^description: \S.+$", cabecalho[1], re.MULTILINE):
                erros.append("Descrição ausente em SKILL.md")
            if f'version: "{VERSAO}"' not in cabecalho[1]:
                erros.append("Versão divergente em SKILL.md")
    adr = raiz / "templates/adr-modulo.md"
    if adr.is_file():
        texto = adr.read_text(encoding="utf-8")
        for secao in SECOES_ADR:
            if f"## {secao}" not in texto:
                erros.append(f"Modelo de ADR sem seção: {secao}")
    trilha = raiz / "references/trilha-modulos.md"
    if trilha.is_file():
        texto = trilha.read_text(encoding="utf-8")
        for f in m.get("fases", []):
            if f"## Fase {f.get('codigo')}" not in texto:
                erros.append(f"Trilha sem a fase {f.get('codigo')}")
    matriz = raiz / "templates/matriz-aderencia.md"
    if matriz.is_file():
        texto = matriz.read_text(encoding="utf-8")
        for t in m.get("tabelas", []):
            if f"`{t.get('nome')}`" not in texto:
                erros.append(f"Matriz de aderência sem a tabela: {t.get('nome')}")
    seed = raiz / "templates/seed-planos-exemplo.md"
    if seed.is_file() and "EXEMPLO COMERCIAL" not in seed.read_text(encoding="utf-8"):
        erros.append("Seed sem a marcação EXEMPLO COMERCIAL")
    api = raiz / "contracts/api-publica-openapi.yaml"
    if api.is_file():
        texto = api.read_text(encoding="utf-8")
        for termo in ["openapi:", "/api/v1/public/plans:", "Cache-Control"]:
            if termo not in texto:
                erros.append(f"OpenAPI sem: {termo}")
        for termo in PROIBIDOS_API:
            if re.search(rf"^\s*{termo}:", texto, re.MULTILINE):
                erros.append(f"OpenAPI expõe campo interno: {termo}")
    nucleo = [entrada] + [p for pasta in ("contracts", "references", "templates") for p in (raiz / pasta).glob("*") if p.is_file()]
    for arquivo in nucleo:
        if arquivo.is_file():
            texto = arquivo.read_text(encoding="utf-8")
            for termo in NOMES_DE_PROJETO:
                if termo in texto:
                    erros.append(f"Nome de projeto no núcleo: {termo} em {arquivo.relative_to(raiz)}")
    changelog = raiz / "CHANGELOG.md"
    if changelog.is_file() and f"## {VERSAO}" not in changelog.read_text(encoding="utf-8"):
        erros.append("CHANGELOG sem a versão atual")
    return erros


def validar_fixture(raiz, m):
    erros = []
    caminho = Path(raiz) / "tests/fixtures/esquema-esperado.json"
    if not caminho.is_file():
        return erros
    esperado = json.loads(caminho.read_text(encoding="utf-8"))
    if esperado.get("schema_version") != m.get("schema_version"):
        erros.append("Fixture e manifesto têm versões diferentes")
    atuais = {t.get("nome"): t for t in m.get("tabelas", [])}
    for nome, e in esperado.get("tabelas", {}).items():
        t = atuais.get(nome)
        if not t:
            erros.append(f"Fixture: tabela ausente no manifesto: {nome}")
            continue
        if [c.get("nome") for c in t.get("colunas", [])] != e["colunas"]:
            erros.append(f"Fixture: colunas divergentes em {nome}")
        if [u.get("colunas") for u in t.get("unicos", [])] != e["unicos"]:
            erros.append(f"Fixture: unicidades divergentes em {nome}")
        if t.get("fase") != e["fase"]:
            erros.append(f"Fixture: fase divergente em {nome}")
    return erros


def validar(raiz):
    raiz = Path(raiz)
    erros = validar_referencias(raiz)
    caminho = raiz / "contracts/schema-manifest.yaml"
    if not caminho.is_file():
        return erros
    try:
        m = json.loads(caminho.read_text(encoding="utf-8"))
    except ValueError as erro:
        return erros + [f"Manifesto ilegível: {erro}"]
    erros += validar_manifesto(m)
    erros += validar_textos(raiz, m)
    erros += validar_fixture(raiz, m)
    erros += [f"Documento fora de sincronia com o manifesto: {d}" for d in divergencias(raiz, m)]
    return erros


if __name__ == "__main__":
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    raiz = Path(argumentos[0]).resolve() if argumentos else Path(__file__).resolve().parents[1]
    if "--checksum" in sys.argv:
        print(checksum_manifesto(raiz))
        sys.exit(0)
    erros = validar(raiz)
    for erro in erros:
        print(f"ERRO: {erro}")
    if erros:
        sys.exit(1)
    print(f"OK: {NOME} {VERSAO}; manifesto sha256 {checksum_manifesto(raiz)}")
