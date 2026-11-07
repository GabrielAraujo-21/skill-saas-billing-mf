"""Testes de arquivos, links e correspondência entre documentos, em cópias temporárias."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from validar_skill import validar  # noqa: E402


class ReferenciasTest(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.copia = Path(self.pasta.name) / "skill"
        shutil.copytree(RAIZ, self.copia, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self):
        self.pasta.cleanup()

    def assertReprova(self, trecho):
        erros = validar(self.copia)
        self.assertTrue(any(trecho in e for e in erros), f"Esperava '{trecho}' em {erros}")

    def alterar(self, relativo, antes, depois):
        caminho = self.copia / relativo
        texto = caminho.read_text(encoding="utf-8")
        self.assertIn(antes, texto)
        caminho.write_text(texto.replace(antes, depois, 1), encoding="utf-8", newline="\n")

    def test_skill_valida(self):
        self.assertEqual(validar(RAIZ), [])

    def test_arquivo_ausente(self):
        (self.copia / "references/seguranca-lgpd.md").unlink()
        self.assertReprova("Arquivo ausente: references/seguranca-lgpd.md")

    def test_link_quebrado(self):
        with (self.copia / "README.md").open("a", encoding="utf-8") as saida:
            saida.write("\n[quebrado](references/nao-existe.md)\n")
        self.assertReprova("Referência local inválida")

    def test_nome_da_skill(self):
        self.alterar("SKILL.md", "name: skill-saas-billing-mf", "name: outro-nome")
        self.assertReprova("Nome da skill divergente")

    def test_documento_gerado_fora_de_sincronia(self):
        with (self.copia / "contracts/dicionario-dados.md").open("a", encoding="utf-8") as saida:
            saida.write("\nedição manual\n")
        self.assertReprova("fora de sincronia")

    def test_manifesto_alterado_sem_regenerar(self):
        self.alterar("contracts/schema-manifest.yaml", '"fase": "06"', '"fase": "07"')
        self.assertReprova("fora de sincronia")

    def test_seed_sem_marcacao(self):
        self.alterar("templates/seed-planos-exemplo.md", "EXEMPLO COMERCIAL", "exemplo")
        self.assertReprova("EXEMPLO COMERCIAL")

    def test_adr_sem_secao(self):
        self.alterar("templates/adr-modulo.md", "## Rollback", "## Reversão")
        self.assertReprova("Modelo de ADR sem seção: Rollback")

    def test_trilha_sem_fase(self):
        self.alterar("references/trilha-modulos.md", "## Fase 04", "## Etapa 04")
        self.assertReprova("Trilha sem a fase 04")

    def test_api_expoe_campo_interno(self):
        with (self.copia / "contracts/api-publica-openapi.yaml").open("a", encoding="utf-8") as saida:
            saida.write("\n        tenant_id:\n          type: integer\n")
        self.assertReprova("OpenAPI expõe campo interno: tenant_id")

    def test_nome_de_projeto_no_nucleo(self):
        with (self.copia / "references/arquitetura-modular.md").open("a", encoding="utf-8") as saida:
            saida.write("\nMindFlow\n")
        self.assertReprova("Nome de projeto no núcleo")


if __name__ == "__main__":
    unittest.main()
