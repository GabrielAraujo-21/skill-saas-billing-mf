"""Laboratório descartável: aplica o manifesto em SQLite, fase a fase, e exercita as restrições.

Valida a estrutura lógica do contrato. Não substitui os testes do módulo em Laravel no projeto consumidor.
"""

import json
import sqlite3
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
AGORA = "2026-01-01 00:00:00"
DEPOIS = "2026-02-01 00:00:00"


def ddl(t, enums):
    partes = []
    for c in t["colunas"]:
        if c["nome"] == "id":
            partes.append("id INTEGER PRIMARY KEY")
            continue
        linha = f"{c['nome']} {c['tipo']}" + ("" if c["nulo"] else " NOT NULL")
        if "padrao" in c:
            p = c["padrao"]
            linha += f" DEFAULT {int(p) if isinstance(p, bool) else (repr(p) if isinstance(p, str) else p)}"
        if "enum" in c:
            valores = ", ".join(repr(v) for v in enums[c["enum"]])
            linha += f" CHECK ({c['nome']} IN ({valores}))"
        partes.append(linha)
    partes += [f"CHECK ({x})" for x in t["checks"]]
    for c in t["colunas"]:
        if "fk" in c:
            fk = c["fk"]
            partes.append(f"FOREIGN KEY ({c['nome']}) REFERENCES {fk['tabela']}({fk['coluna']}) ON DELETE {fk['on_delete']} ON UPDATE {fk['on_update']}")
    comandos = [f"CREATE TABLE {t['nome']} ({', '.join(partes)})"]
    for u in t["unicos"]:
        condicao = f" WHERE {u['condicao']}" if "condicao" in u else ""
        comandos.append(f"CREATE UNIQUE INDEX {u['nome']} ON {t['nome']} ({', '.join(u['colunas'])}){condicao}")
    comandos += [f"CREATE INDEX {i['nome']} ON {t['nome']} ({', '.join(i['colunas'])})" for i in t["indices"]]
    return comandos


class LaboratorioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = json.loads((RAIZ / "contracts/schema-manifest.yaml").read_text(encoding="utf-8"))

    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.execute("CREATE TABLE tenants (id INTEGER PRIMARY KEY)")
        self.db.executemany("INSERT INTO tenants (id) VALUES (?)", [(1,), (2,)])
        por_nome = {t["nome"]: t for t in self.m["tabelas"]}
        for fase in self.m["fases"]:
            pendentes = [por_nome[n] for n in fase["tabelas"]]
            criadas = set()
            while pendentes:
                resto = []
                for t in pendentes:
                    alvos = {c["fk"]["tabela"] for c in t["colunas"] if "fk" in c} - {t["nome"]}
                    if alvos & {x["nome"] for x in pendentes} - criadas - {t["nome"]}:
                        resto.append(t)
                        continue
                    for comando in ddl(t, self.m["enumeracoes"]):
                        self.db.execute(comando)
                    criadas.add(t["nome"])
                self.assertLess(len(resto), len(pendentes), f"Dependência circular na fase {fase['codigo']}")
                pendentes = resto
        self.plano_base()

    def tearDown(self):
        self.db.close()

    def inserir(self, tabela, **v):
        agora = {c["nome"]: AGORA for t in self.m["tabelas"] if t["nome"] == tabela for c in t["colunas"] if c["nome"] in ("created_at", "updated_at")}
        v = {**agora, **v}
        cols = ", ".join(v)
        marcas = ", ".join("?" for _ in v)
        return self.db.execute(f"INSERT INTO {tabela} ({cols}) VALUES ({marcas})", list(v.values())).lastrowid

    def plano_base(self):
        self.plano = self.inserir("planos", nome="Base", slug="base")
        self.versao = self.inserir("planos_versoes", plano_id=self.plano, numero_versao=1, nome_versao="v1")
        self.preco = self.inserir("planos_precos", plano_versao_id=self.versao, periodicidade="mensal", moeda="BRL", valor="10.00")
        self.provedor = self.inserir("provedores_pagamento", nome="PSP", codigo="psp", ambiente="sandbox")

    def assinatura(self, tenant=1, status="ativa"):
        return self.inserir(
            "assinaturas", tenant_id=tenant, plano_versao_id=self.versao, plano_preco_id=self.preco, status=status, periodicidade="mensal",
            valor_contratado="10.00", moeda="BRL", periodo_inicio=AGORA, periodo_fim=DEPOIS,
        )

    def fatura(self, assinatura, numero="F1"):
        return self.inserir(
            "faturas", tenant_id=1, assinatura_id=assinatura, numero=numero, competencia="2026-01-01", vencimento="2026-01-10",
            subtotal="10.00", valor_total="10.00", moeda="BRL", status="aberta",
        )

    def assertViola(self, tabela, **v):
        with self.assertRaises(sqlite3.IntegrityError):
            self.inserir(tabela, **v)

    def test_todas_as_tabelas_criadas_na_ordem_das_fases(self):
        nomes = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
        self.assertEqual(nomes - {"tenants"}, {t["nome"] for t in self.m["tabelas"]})

    def test_uma_assinatura_efetiva_por_tenant(self):
        self.assinatura()
        with self.assertRaises(sqlite3.IntegrityError):
            self.assinatura(status="trial")

    def test_assinatura_terminal_libera_nova(self):
        self.assinatura(status="cancelada")
        self.assinatura(status="ativa")

    def test_tenant_inexistente_recusado(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.assinatura(tenant=99)

    def test_status_invalido_recusado(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.assinatura(status="active")

    def test_preco_sob_consulta_exige_valor_nulo(self):
        self.assertViola("planos_precos", plano_versao_id=self.versao, periodicidade="anual", moeda="BRL", modalidade_preco="sob_consulta", valor="1.00")
        self.inserir("planos_precos", plano_versao_id=self.versao, periodicidade="anual", moeda="BRL", modalidade_preco="sob_consulta")

    def test_preco_fixo_exige_valor(self):
        self.assertViola("planos_precos", plano_versao_id=self.versao, periodicidade="anual", moeda="BRL")

    def test_limite_sem_periodo_nao_duplica(self):
        self.inserir("planos_limites", plano_versao_id=self.versao, recurso="usuarios", limite=5)
        self.assertViola("planos_limites", plano_versao_id=self.versao, recurso="usuarios", limite=9)

    def test_provedor_por_ambiente(self):
        self.inserir("provedores_pagamento", nome="PSP", codigo="psp", ambiente="producao")
        self.assertViola("provedores_pagamento", nome="PSP", codigo="psp", ambiente="producao")

    def test_webhook_duplicado_recusado(self):
        v = dict(provedor_pagamento_id=self.provedor, chave_deduplicacao="e1", tipo="pagamento", recebido_em=AGORA)
        self.inserir("pagamentos_eventos", **v)
        self.assertViola("pagamentos_eventos", **v)

    def test_baixa_duplicada_recusada(self):
        f = self.fatura(self.assinatura())
        v = dict(tenant_id=1, fatura_id=f, provedor_pagamento_id=self.provedor, metodo_pagamento="pix", valor="10.00", moeda="BRL", status="confirmado")
        self.inserir("pagamentos", chave_idempotencia="k1", **v)
        self.assertViola("pagamentos", chave_idempotencia="k1", **v)

    def test_consumo_idempotente_por_tenant(self):
        a = self.assinatura()
        v = dict(tenant_id=1, assinatura_id=a, recurso="api", quantidade=1, ocorrido_em=AGORA, chave_idempotencia="c1")
        self.inserir("consumos_eventos", **v)
        self.assertViola("consumos_eventos", **v)

    def test_cupom_nao_repete_na_fatura(self):
        a = self.assinatura()
        f = self.fatura(a)
        c = self.inserir("cupons", codigo="X", tipo_desconto="percentual", valor_desconto="10.00", valido_inicio=AGORA, valido_fim=DEPOIS)
        v = dict(cupom_id=c, tenant_id=1, assinatura_id=a, fatura_id=f, valor_desconto_aplicado="1.00", utilizado_em=AGORA)
        self.inserir("cupons_utilizacoes", **v)
        self.assertViola("cupons_utilizacoes", **v)

    def test_cupom_percentual_limitado_a_cem(self):
        self.assertViola("cupons", codigo="Y", tipo_desconto="percentual", valor_desconto="101.00", valido_inicio=AGORA, valido_fim=DEPOIS)

    def test_exclusao_financeira_bloqueada(self):
        a = self.assinatura()
        self.fatura(a)
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute("DELETE FROM assinaturas WHERE id = ?", [a])

    def test_beneficio_exige_alvo(self):
        self.assertViola("tenants_beneficios", tenant_id=1, tipo_beneficio="cortesia", inicio=AGORA, justificativa="teste")


if __name__ == "__main__":
    unittest.main()
