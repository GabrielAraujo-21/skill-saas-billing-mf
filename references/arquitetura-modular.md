# Arquitetura modular

O módulo é um contexto próprio dentro do monólito modular, salvo decisão diferente do projeto. Siga a estrutura de pastas do projeto e de `skill-backend-mf`; nada aqui obriga a criar serviço separado.

## Submódulos

| Submódulo | Responde por | Não faz |
|---|---|---|
| Catálogo | Planos, versões, preços, publicação | Conhecer tenant |
| Direitos | Resolver direitos e limites efetivos | Decidir permissão de usuário |
| Assinaturas | Máquina de estados e alterações | Chamar provedor diretamente |
| Consumo | Registrar e reconciliar uso | Cobrar |
| Financeiro | Faturas, pagamentos e reembolsos | Mudar status sem evento verificado |
| Provedores | Adaptadores e webhooks | Conter regra comercial |
| Promoções | Adicionais e cupons | Alterar preço de catálogo |

## Fronteiras

- Outros módulos consultam um único serviço de direitos, nunca as tabelas comerciais. Assim, um `if plano == 'x'` não se espalha pelo código.
- Controller não contém regra comercial. Mudança de status passa por um único serviço, que valida a transição, grava o histórico e publica o evento na mesma unidade de trabalho.
- Provedores ficam atrás de contratos por capacidade (criar cobrança, cancelar, consultar, validar webhook), não de uma interface gigante. Um provedor sem certa capacidade declara isso, e o fluxo trata o caso.
- O adaptador de webhook converte a requisição em um objeto simples; o serviço não recebe `Request`.

## Fluxo de ativação paga

1. O checkout cria a assinatura em `pendente` e a chave de idempotência.
2. O navegador retorna, e a tela mostra "aguardando confirmação".
3. O webhook é autenticado, gravado e respondido.
4. Um job processa o evento e, se preciso, consulta o provedor.
5. O serviço de assinaturas move para `ativa`, registra o histórico e publica o evento.
6. A reconciliação cobre o caso de o webhook nunca chegar.
