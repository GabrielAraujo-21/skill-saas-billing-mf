"""Testes do manifesto, incluindo casos negativos que devem reprovar."""

import copy
import json
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from validar_skill import validar_fixture, validar_manifesto  # noqa: E402


def tabela(m, nome):
    return next(t for t in m["tabelas"] if t["nome"] == nome)


class ManifestoTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads((RAIZ / "contracts/schema-manifest.yaml").read_text(encoding="utf-8"))

    def setUp(self):
        self.m = copy.deepcopy(self.base)

    def assertReprova(self, trecho):
        erros = validar_manifesto(self.m)
        self.assertTrue(any(trecho in e for e in erros), f"Esperava '{trecho}' em {erros}")

    def test_manifesto_valido(self):
        self.assertEqual(validar_manifesto(self.m), [])

    def test_fixture_corresponde(self):
        self.assertEqual(validar_fixture(RAIZ, self.m), [])

    def test_remover_tabela(self):
        self.m["tabelas"] = [t for t in self.m["tabelas"] if t["nome"] != "faturas"]
        self.assertReprova("Tabela obrigatória ausente: faturas")

    def test_tabela_duplicada(self):
        self.m["tabelas"].append(copy.deepcopy(tabela(self.m, "cupons")))
        self.assertReprova("Tabela duplicada: cupons")

    def test_remover_coluna_essencial(self):
        t = tabela(self.m, "pagamentos")
        t["colunas"] = [c for c in t["colunas"] if c["nome"] != "chave_idempotencia"]
        self.assertReprova("coluna essencial ausente: chave_idempotencia")

    def test_remover_fk(self):
        c = next(c for c in tabela(self.m, "faturas")["colunas"] if c["nome"] == "assinatura_id")
        c["fk"]["tabela"] = "inexistente"
        self.assertReprova("FK para tabela inexistente")

    def test_fk_para_fase_posterior(self):
        tabela(self.m, "adicionais")["fase"] = "07"
        self.assertReprova("FK para tabela de fase posterior: adicionais")

    def test_remover_status(self):
        self.m["enumeracoes"]["status_assinatura"].remove("inadimplente")
        self.assertReprova("Status de assinatura ausente: inadimplente")

    def test_remover_unicidade(self):
        tabela(self.m, "consumos_eventos")["unicos"] = []
        self.assertReprova("unicidade ausente: tenant_id, chave_idempotencia")

    def test_dinheiro_em_float(self):
        c = next(c for c in tabela(self.m, "faturas")["colunas"] if c["nome"] == "valor_total")
        c["tipo"] = "float"
        self.assertReprova("ponto flutuante")

    def test_timestamps_sem_excecao(self):
        t = tabela(self.m, "consumos_eventos")
        del t["excecao_timestamps"]
        self.assertReprova("updated_at ausente sem exceção")

    def test_soft_delete_financeiro(self):
        tabela(self.m, "faturas")["colunas"].append({"nome": "deleted_at", "tipo": "timestamp", "nulo": True})
        self.assertReprova("soft delete sem justificativa")

    def test_tenant_removido_de_filha(self):
        t = tabela(self.m, "faturas_itens")
        t["colunas"] = [c for c in t["colunas"] if c["nome"] != "tenant_id"]
        self.assertReprova("escopo por tenant sem tenant_id")

    def test_saida_de_estado_terminal(self):
        self.m["maquina_estados_assinatura"]["transicoes"].append({"de": "cancelada", "para": "ativa", "gatilho": "x"})
        self.assertReprova("Estado terminal com saída: cancelada")

    def test_fixture_detecta_deriva(self):
        t = tabela(self.m, "planos")
        t["colunas"] = [c for c in t["colunas"] if c["nome"] != "destaque"]
        self.assertTrue(validar_fixture(RAIZ, self.m))


if __name__ == "__main__":
    unittest.main()
