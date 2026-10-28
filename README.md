# Raízes e cidadania

Skills para Claude Code, Codex e Antigravity que ajudam qualquer pessoa a montar a árvore genealógica da família com cada dado provado por documento e, se houver direito, a preparar o pedido de cidadania portuguesa, italiana ou espanhola por descendência.

Nasceu de um trabalho real de pesquisa familiar e de preparação de um pedido de cidadania. O que funcionou nesse processo virou regra aqui: guardar os originais intocados, citar a fonte de cada dado, separar o que é documento do que é história de família, registrar as divergências entre certidões e conferir a lei no site oficial antes de afirmar qualquer coisa.

## O que fica pronto

O agente cria uma pasta para a família, com os documentos originais guardados como chegaram, cópias renomeadas por data, tipo e pessoa, e um índice em planilha.

Os dados de todos os parentes ficam num único arquivo, o `pessoas.json`. Dele saem a árvore em HTML, que abre em qualquer navegador e funciona sem internet, uma ficha em Markdown por pessoa (dá para abrir no Obsidian) e um arquivo GEDCOM para levar a árvore ao FamilySearch, MyHeritage, Ancestry ou Gramps. Na árvore, cada fato traz o documento de onde veio e um selo: confirmado, relato da família ou hipótese. Ao lado de cada nome aparece o ícone do país, reino ou povo de nascimento na época (Reino de Portugal, Império do Brasil, Reino de Itália e assim por diante), e uma estrela marca quem foi figura conhecida na história, com um resumo e o link da fonte. A estrela só entra depois de você autorizar a pesquisa e quando os documentos da família mostram que se trata da mesma pessoa, e não de um homônimo.

Documentos antigos, como batismos, registros civis, passaportes e listas de navio, são transcritos com as dúvidas marcadas. As skills leem português, italiano, espanhol e latim.

Para achar o que falta, há um roteiro de busca por país. Ele cobre FamilySearch, Digitarq, Antenati, PARES, Arquivo Nacional, Museu da Imigração, jornais antigos e cartórios, e sempre começa pelo que é gratuito.

Para a cidadania, o agente monta uma matriz de prova: em cada geração, o documento que prova o vínculo, o trecho exato e o que ainda falta. Um relatório de pendências e uma planilha de pedidos de certidões, com custos e prazos, acompanham o andamento.

## As skills

| Skill | Para que serve |
| --- | --- |
| `raizes` | Porta de entrada: entrevista inicial, regras do projeto e escolha das outras skills |
| `arvore-documental` | Pasta do projeto, `pessoas.json`, árvore HTML, GEDCOM, fichas, índice e pendências |
| `transcricao-registros-antigos` | Leitura e transcrição de registros manuscritos |
| `pesquisa-em-acervos` | Onde e como procurar registros de antepassados |
| `cidadania-portuguesa` | Via de filho, neto e cadeia de gerações para a nacionalidade portuguesa |
| `cidadania-italiana` | Reconhecimento iure sanguinis e as mudanças de 2025 |
| `cidadania-espanhola` | Opção, residência e o que restou da Lei de Memória Democrática |

## Instalação

Você precisa de uma destas ferramentas instalada: [Claude Code](https://claude.com/claude-code), [Codex](https://developers.openai.com/codex) ou Antigravity. Para gerar a árvore, também do [Python](https://www.python.org/downloads/) 3.8 ou mais novo (no Windows: `winget install Python.Python.3.12`).

### Windows

Baixe o repositório (botão **Code > Download ZIP** no GitHub, ou `git clone`), abra o PowerShell dentro da pasta e rode:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Isso copia as skills para as três ferramentas. Para instalar em só uma: `-Destino Claude`, `-Destino Codex` ou `-Destino Antigravity`.

### macOS ou Linux

```bash
git clone https://github.com/walbercarvalho/raizes-e-cidadania.git
cd raizes-e-cidadania
sh install.sh
```

### Claude Code como plugin

Dentro do Claude Code:

```
/plugin marketplace add walbercarvalho/raizes-e-cidadania
/plugin install raizes-e-cidadania@raizes-e-cidadania
```

### Onde as skills ficam

| Ferramenta | Pasta das skills do usuário | Pasta só de um projeto |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Antigravity | `~/.gemini/antigravity/skills/` | `.agent/skills/` |

## Como começar

1. Crie uma pasta vazia para a família (por exemplo `Documentos/Familia-Silva`).
2. Abra essa pasta no Claude Code, Codex ou Antigravity.
3. Diga algo como: *"Quero montar a árvore da minha família e ver se tenho direito à cidadania portuguesa. Meu bisavô veio do Porto."*
4. Responda às perguntas. Primeiro vêm algumas escolhas rápidas (objetivo, país, pasta); depois o agente pede, uma geração por vez, os dados que você souber: seu nome, data e local de nascimento, e os dos seus pais, avós e, se souber, bisavós. Ele grava tudo no seu computador e mostra a árvore se formando.
5. Vá entregando os documentos (fotos ou PDFs) conforme encontrar. Cada um é transcrito, cadastrado e conferido com os outros.

Quer ver antes de começar? Rode o exemplo fictício:

```bash
python skills/arvore-documental/scripts/arvore.py iniciar exemplo-teste
cp skills/arvore-documental/assets/exemplo/pessoas.json exemplo-teste/
python skills/arvore-documental/scripts/arvore.py tudo exemplo-teste/pessoas.json
```

e abra `exemplo-teste/arvore.html` no navegador.

## Privacidade

Seus documentos e os dados da sua família ficam no seu computador. As skills instruem o agente a não enviar nada a serviços externos, não publicar e não subir para repositórios sem o seu pedido. A pasta criada já vem com um `.gitignore` que bloqueia fotos e PDFs. Logins em sites são sempre feitos por você, e e-mails a cartórios ficam como rascunho para você enviar.

Lembre que o agente de IA que você usa lê os documentos que você mostra a ele. Confira a política de dados da ferramenta antes de compartilhar documentos sensíveis.

## Aviso importante

As leis de nacionalidade mudam. Portugal, Itália e Espanha alteraram as regras entre 2022 e 2026. As referências legais deste repositório trazem a data em que foram conferidas, e as skills mandam o agente conferir de novo no site oficial antes de afirmar qualquer coisa. Mesmo assim, isto não é aconselhamento jurídico. Em caso de via judicial, recusa ou situação fora do comum, procure um advogado ou solicitador habilitado no país.

## Contribuir

Achou um erro, uma regra que mudou ou um acervo que deveria estar aqui? Abra uma issue ou um pull request. Correções de regra legal precisam citar a fonte oficial e a data da consulta.

## Licença

MIT.
