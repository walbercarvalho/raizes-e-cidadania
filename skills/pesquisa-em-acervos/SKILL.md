---
name: pesquisa-em-acervos
description: Planeja e conduz buscas de registros de antepassados em acervos online e físicos, como FamilySearch, arquivos distritais portugueses (Digitarq), Antenati na Itália, PARES e arquivos diocesanos na Espanha, Arquivo Nacional, arquivos estaduais e listas de imigração no Brasil, jornais antigos, cemitérios e cartórios. Use quando a pessoa quiser achar o nascimento, batismo, casamento, óbito, chegada ao Brasil ou a cidade de origem de um antepassado, quando não souber onde procurar, quando uma busca não deu resultado ou quando quiser saber o que dá para fazer de graça antes de pagar certidões ou pesquisadores.
---

# Pesquisa em acervos

A busca boa começa do presente para o passado e documenta cada geração antes de pular para a anterior. O que costuma destravar um antepassado imigrante não é o registro dele, e sim o dos filhos, do casamento ou do óbito no Brasil, que dizem a cidade de origem, os pais ou a idade.

## Antes de procurar

1. Leia o `pessoas.json` e as pesquisas já feitas em `pesquisas/` (skill `arvore-documental`), para não repetir buscas.
2. Liste o que se sabe da pessoa-alvo com o status de cada dado e todas as variantes de nome já vistas.
3. Defina a pergunta: "onde nasceu Manuel?" é melhor que "achar tudo sobre Manuel".
4. Pergunte à pessoa se ela quer só caminhos gratuitos ou aceita gastar, e quanto. Sempre ofereça primeiro o que é de graça.

## Estratégia

- **Escada de documentos do imigrante no Brasil**, do mais recente ao mais antigo: óbito (dá idade, naturalidade, pais, às vezes cônjuge e filhos), casamento civil (naturalidade e pais dos noivos), nascimentos dos filhos (naturalidade dos pais; avós), batismos dos filhos (padrinhos e moradia), registro de estrangeiro e carteira modelo 19 (anos 1930 e 1940: data de chegada, navio, pais), listas de passageiros e hospedarias de imigrantes, passaporte no país de origem.
- **Do outro lado do oceano**, o objetivo é a freguesia, comune ou município. Sem ele, a busca é em dezenas de paróquias. Com ele, vai direto ao livro.
- **Variantes:** grafias diferentes (Manoel/Manuel, Joaquim/Joaq.m, Giuseppe/José, Gómez/Gomes), sobrenome que some ou aparece, nome religioso (Maria Anna Rosa, Anna Maria), apelido, sobrenome do marido. Busque também sem o prenome, só pelos pais, e com coringas quando o site aceitar.
- **Índice não é tudo.** Muitos livros estão digitalizados sem índice. Quando a busca por nome não acha, vá ao catálogo, ache o livro certo (lugar, tipo, período) e folheie as imagens. Estime o intervalo de imagens antes, a partir de datas conhecidas.
- **Parentes e vizinhos.** Irmãos, padrinhos, testemunhas e vizinhos de rua costumam vir da mesma aldeia. Um registro de irmão às vezes dá o que falta.
- **Imagem com restrição** no FamilySearch: algumas coleções só abrem num Centro de História da Família (FamilySearch Center) ou biblioteca afiliada. É gratuito; ajude a pessoa a anotar filme, grupo de imagens (DGS) e intervalo de imagens antes de ir.
- **Login.** Sites como FamilySearch exigem conta gratuita. Quem entra é a pessoa, no navegador; nunca digite senha por ela nem crie contas em nome dela.

## Registro de cada busca

Anote em `pesquisas/AAAA-MM-DD-assunto.md`: site ou arquivo, coleção, termos e variantes, filtros de lugar e data, quantos resultados ou imagens conferiu, o que achou (com link, filme, imagem, cota) e o que ficou de fora. Resultado negativo também é resultado: diga exatamente o que foi coberto, para não ser confundido com "não existe".

## Onde procurar

Fontes por país, com endereços e o que cada uma tem: `references/acervos.md`. Leia só a seção do país da busca.

## Antes de pagar

Quando o próximo passo for pago (certidão, cópia de arquivo, pesquisador local, busca em cartório), diga o custo estimado, o que se espera achar e se há alternativa gratuita. Pedidos por e-mail a cartórios, comuni e arquivos ficam como rascunho para a pessoa enviar; nunca envie mensagens em nome dela sem pedido explícito. Primeiro pergunte se o registro existe e em que livro está (isso costuma ser gratuito), e só depois peça a certidão.

## Achou

Copie o documento para o núcleo documental, transcreva (skill `transcricao-registros-antigos`), cadastre no `pessoas.json` e registre divergências. Conte à pessoa o que mudou na árvore e qual é o próximo passo que esse achado abre.
