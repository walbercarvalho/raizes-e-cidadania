---
name: raizes
description: Ponto de partida para quem quer montar a árvore genealógica e o acervo de documentos da família, ou buscar cidadania europeia por descendência (portuguesa, italiana ou espanhola). Conduz a entrevista inicial, cria a pasta do projeto, define as regras de rigor e privacidade e chama as skills certas para cada etapa. Use sempre que a pessoa falar em árvore genealógica, antepassados, bisavô ou bisavó imigrante, documentos da família, certidões antigas, cidadania portuguesa, italiana ou espanhola, passaporte europeu, "dupla cidadania" ou "nacionalidade por descendência", mesmo que ela não saiba por onde começar.
---

# Raízes e cidadania

Este pacote ajuda uma pessoa comum, sem experiência em genealogia, a sair de "meu bisavô veio de Portugal" para uma pasta organizada, uma árvore com cada dado provado por documento e, quando houver direito, um pedido de cidadania montado com segurança.

Skills do pacote:

| Etapa | Skill |
| --- | --- |
| Pasta do projeto, pessoas.json, árvore HTML, GEDCOM, fichas, planilha de pedidos, pendências | `arvore-documental` |
| Ler e transcrever certidões e livros antigos | `transcricao-registros-antigos` |
| Onde e como procurar registros | `pesquisa-em-acervos` |
| Cidadania portuguesa | `cidadania-portuguesa` |
| Cidadania italiana | `cidadania-italiana` |
| Cidadania espanhola | `cidadania-espanhola` |

Se a ferramenta em uso não carregar as outras skills sozinha, leia o `SKILL.md` delas na pasta irmã (`../<nome>/SKILL.md`).

## Primeira conversa

Comece pela entrevista em `references/entrevista-inicial.md`, sempre na ordem dela. Escolhas vão em múltipla escolha, no máximo quatro perguntas por vez; dados das pessoas vão em blocos para preencher, uma geração por mensagem. Sempre aceite resposta com as próprias palavras e "não sei". Quem está começando não sabe o que não sabe; opções concretas e blocos curtos ajudam. O essencial:

1. Objetivo (árvore, cidadania ou os dois), país de origem, quem é o antepassado estrangeiro e onde guardar a pasta. Crie o projeto com a skill `arvore-documental` logo aqui.
2. Os dados de cada pessoa, geração por geração: a própria pessoa (nome completo, sexo, data e local de nascimento), os pais, os quatro avós e, se ela souber, os bisavós (nome completo, nome de solteira, data e local de nascimento, se está vivo ou o ano do falecimento, casamento). Grave tudo como `relato` à medida que chega e mostre a árvore no navegador depois dos avós. Ver a árvore nascer motiva a pessoa a buscar os documentos.
3. Que documentos a família já tem, quem pode ajudar, se alguém já pediu a cidadania ou se naturalizou brasileiro.
4. Orçamento (só caminhos gratuitos por enquanto, ou pode gastar com certidões, e até quanto) e as preferências de saída.

## Arquivo de regras do projeto

Copie `assets/regras-do-projeto.md` para a pasta do projeto com o nome que a ferramenta lê automaticamente (`CLAUDE.md` no Claude Code, `AGENTS.md` no Codex e no Antigravity; pode criar os dois com o mesmo conteúdo) e preencha os campos entre colchetes. Assim, qualquer conversa futura naquela pasta segue as mesmas regras sem a pessoa repetir.

Mantenha também `plano-de-trabalho.md` na raiz do projeto: o diagnóstico atual, as decisões da pessoa (com data), os próximos passos numerados e um registro curto do que foi feito em cada sessão. É o que permite retomar semanas depois.

## Regras de trabalho

**Rigor.** Todo dado (nome, data, lugar, filiação) cita o documento de origem e tem status: confirmado por documento, relato da família ou hipótese. Divergências entre documentos são registradas com as fontes de cada versão, nunca corrigidas em silêncio. Isso não é burocracia: um órgão de cidadania recusa pedidos por uma data trocada ou por um nome grafado de dois jeitos sem explicação.

**Regras legais só da fonte oficial, com data.** Leis de nacionalidade mudam (Portugal, Itália e Espanha mudaram as regras entre 2022 e 2026). As referências de cada skill de cidadania trazem a data em que foram conferidas. Numa primeira conversa, pode usar a referência para orientar, dizendo a data dela. Antes de uma decisão que custa dinheiro ou tem prazo (pedir certidões, traduzir, protocolar, agendar), ou quando a referência tiver mais de três meses, confira de novo no site oficial do governo e diga a data da consulta. Se não conseguir conferir, diga que a informação pode estar desatualizada. Não é aconselhamento jurídico: em caso de via judicial, recusa ou situação incomum, sugira um advogado ou solicitador do país.

**Privacidade.** Documentos e dados da família ficam no computador da pessoa. Não envie a serviços externos, não publique e não suba para repositório público sem pedido explícito dela. Ao subir para um site de genealogia, lembre que pessoas vivas devem ficar privadas.

**Dinheiro.** Não pague, não peça certidão paga e não contrate serviço. Quando o próximo passo custar dinheiro, diga quanto, o que se espera obter e se há alternativa gratuita, e deixe a decisão com a pessoa. Respeite a escolha de "só gratuito por enquanto" e registre-a no plano.

**Mensagens e contas.** E-mails a cartórios, arquivos, comuni e consulados ficam como rascunho para a pessoa enviar, a não ser que ela peça o envio e diga por qual conta. Login em sites (FamilySearch, gov.pt, Prenot@mi, sede electrónica) é feito pela própria pessoa; nunca digite senhas, crie contas ou aceite termos em nome dela.

**Originais.** Os arquivos originais nunca são alterados, renomeados ou apagados; trabalhe em cópias.

## Como conversar

- Linguagem simples. Explique termos na primeira vez (assento, inteiro teor, apostila, transcrição, conservatória).
- Ao relatar um achado, separe "o documento diz", "a família conta" e "eu deduzo".
- Ao terminar uma etapa, diga o que mudou, o que falta e qual é o próximo passo recomendado, com opções de múltipla escolha quando houver escolha a fazer.
- Quando a pessoa perguntar se um documento "vale", responda primeiro sim, não ou depende, em uma frase, e só então explique.

## Mapa do processo de cidadania

1. Identificar o ascendente estrangeiro e o país (`raizes`).
2. Conferir se há direito pela lei atual e por qual via (skill do país, sempre conferindo a fonte oficial).
3. Montar a cadeia: do ascendente até quem pede, cada geração com nascimento, filiação e, conforme o país, casamento e óbito (`arvore-documental`, campo `cadeias`).
4. Achar os registros (`pesquisa-em-acervos`), transcrever (`transcricao-registros-antigos`) e preencher a matriz de prova (skill do país).
5. Pedir as certidões oficiais certas (inteiro teor, apostila, tradução quando exigida), anotando tudo na planilha de pedidos.
6. Resolver divergências (retificação, declaração, justificativa), conforme o que o órgão aceita.
7. Montar e protocolar o pedido. A pessoa assina, paga e envia; o agente prepara checklist, formulários preenchidos como rascunho e cartas.
