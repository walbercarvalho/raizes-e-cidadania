---
name: arvore-documental
description: Monta e mantém o núcleo documental de uma família, com pastas organizadas, índice de documentos, pessoas.json, fichas em Markdown por pessoa, árvore genealógica em HTML interativo, exportação GEDCOM, planilha de pedidos de certidões e relatório de pendências. Use quando a pessoa quiser organizar documentos e fotos da família, cadastrar parentes, registrar nascimentos, casamentos e óbitos, gerar ou atualizar a árvore, exportar para FamilySearch, MyHeritage ou Ancestry, ou saber o que falta documentar. Use também quando ela trouxer uma certidão nova para entrar na árvore, mesmo sem dizer "árvore".
---

# Núcleo documental e árvore da família

O objetivo é que cada dado da árvore aponte para um documento, e que qualquer pessoa da família consiga abrir a pasta daqui a dez anos e entender de onde veio cada informação. A árvore bonita é consequência disso, não o ponto de partida.

## Estrutura do projeto

Crie a estrutura com o script (só precisa do Python 3.8 ou mais novo, sem instalar pacotes):

```bash
python "<pasta desta skill>/scripts/arvore.py" iniciar "<pasta do projeto>" --familia "Família Sobrenome"
```

Use sempre o caminho completo do script (a pasta onde este SKILL.md está, mais `scripts/arvore.py`) e o caminho completo do `pessoas.json`, porque um fica na pasta da skill e o outro na pasta do projeto. Nos exemplos abaixo, `arvore.py` abrevia esse caminho completo. Se não houver Python, explique como instalar (no Windows: `winget install Python.Python.3.12`, ou pelo site python.org marcando "Add to PATH") e, enquanto isso, crie as pastas à mão com a mesma estrutura.

Pastas criadas: `documentos-originais/`, `documentos-organizados/` (com `indice-dos-documentos.csv`), `transcricoes/`, `fichas/`, `cidadania/`, `pesquisas/`, `saidas/`, mais `pessoas.json`, `pedidos-de-certidoes.csv`, `LEIAME.md` e um `.gitignore` que deixa documentos e dados pessoais fora de qualquer repositório git. A pasta do projeto nunca deve virar repositório público.

## Regras que valem para todo o projeto

1. **Originais intocados.** O que a pessoa entrega vai para `documentos-originais/` do jeito que veio, com o nome que veio. Nunca renomeie, recorte, gire ou apague um original. Trabalhe sempre numa cópia.
2. **Cópia organizada com nome padrão:** `AAAA-MM-DD Tipo - Nome da Pessoa - lugar.ext`, por exemplo `1925-01-15 Nascimento - Antonio Ferreira - Santos.jpg`. A data é a do fato (nascimento, casamento, óbito), não a da emissão da certidão; se a certidão for uma 2ª via recente, diga isso no nome (`... - 2a via 2010.jpg`). Subpastas por ramo da família ajudam quando o acervo cresce (`1 Ferreira (paterno)/`, `2 Bianchi (materno)/`, `9 Sem ligação comprovada/`).
3. **Todo dado cita a fonte e tem status:** `confirmado` (você viu o documento, a foto ou a imagem do acervo e ele está cadastrado em `documentos`), `relato` (alguém da família contou; anote quem e quando) ou `hipotese` (dedução sua ou de terceiros). Documento que a pessoa diz ter, mas que você ainda não viu, continua `relato`, com a nota "documento em mãos, não conferido". Nunca promova um relato a confirmado sem ver o documento.
4. **Divergências são registradas, nunca corrigidas em silêncio.** Datas, idades, grafias de nome e lugares mudam de um documento para outro. Registre cada versão com o documento de onde veio em `divergencias` e explique qual prevalece e por quê. Idade em óbito, declarada por terceiro, vale menos que o batismo; o registro mais próximo do fato costuma valer mais.
5. **Variantes de nome são normais** (Manoel/Manuel, Anna Maria/Maria Anna Rosa, sobrenome do marido acrescentado). Liste-as em `variantes` e use a forma do documento mais antigo e confiável no `nome`.
6. **Privacidade.** Documentos e dados da família ficam no computador da pessoa. Não envie nada a serviços externos, não publique e não suba para repositório sem ela pedir. Pessoas vivas merecem cuidado extra em qualquer exportação.

## Fluxo de trabalho

### Entrada de um documento novo

1. Copie para `documentos-originais/` (se ainda não estiver) e faça a cópia organizada.
2. Se for manuscrito ou antigo, transcreva com a skill `transcricao-registros-antigos` antes de extrair dados. Não tire dados de uma leitura rápida da imagem inteira.
3. Cadastre o documento em `documentos` no `pessoas.json` (id, tipo, título, data, local, pessoas citadas, acervo, cota, arquivo, transcrição).
4. Atualize as pessoas citadas: eventos, filiação, uniões, variantes. Cada fato novo com `fontes` e `status`.
5. Compare com o que já havia. Toda diferença vira uma entrada em `divergencias`.
6. Rode `python arvore.py tudo pessoas.json` (com os caminhos completos) e conte à pessoa o que o documento acrescentou, o que ele confirmou e o que ficou em conflito.

### Cadastro a partir de relato

Quando a pessoa conta de memória ("minha avó nasceu em Lisboa, por volta de 1880"), cadastre com `status: "relato"` e uma `nota` com quem contou e quando. Isso é valioso: muitas vezes é a única pista para achar o documento. Pergunte pelos documentos que a família tem guardados (certidões, carteiras de identidade antigas, passaportes, carteiras de estrangeiro, santinhos de missa de sétimo dia, cartas, fotos com anotações no verso).

### Geração

```bash
python "<pasta desta skill>/scripts/arvore.py" validar "<pasta do projeto>/pessoas.json"   # sempre antes de gerar
python "<pasta desta skill>/scripts/arvore.py" tudo "<pasta do projeto>/pessoas.json"      # árvore, GEDCOM, fichas, índice, pendências
```

- `arvore.html` na raiz do projeto: abre em qualquer navegador, sem internet; clique numa pessoa para ver os ascendentes, os fatos com status e os links para os documentos.
- `saidas/arvore.ged`: GEDCOM 5.5.1 para importar no FamilySearch, MyHeritage, Ancestry ou Gramps. Pessoas sem óbito e nascidas há menos de 100 anos (ou sem data) saem marcadas como privadas (`RESN privacy`). Antes de importar num site, lembre a pessoa de que ali os dados ficam visíveis para outros e confira se os vivos ficaram privados.
- `fichas/<id>.md`: uma ficha por pessoa. O bloco entre `<!-- dados:inicio -->` e `<!-- dados:fim -->` é regenerado; o resto (história, pendências) é texto livre e nunca é apagado pelo script. Funciona em qualquer editor e no Obsidian.
- `documentos-organizados/indice-dos-documentos.csv`: gerado a partir de `documentos`. Edite o `pessoas.json`, não o CSV.
- `saidas/pendencias.md`: o que falta em cada cadeia de cidadania e quais fatos não têm documento.

Erros do `validar` impedem a geração; avisos não. Corrija a causa (id errado, fonte inexistente, "confirmado" sem documento) em vez de afrouxar o status.

O formato completo do `pessoas.json` está em `references/formato-pessoas-json.md`. Um exemplo fictício completo está em `assets/exemplo/pessoas.json`; use-o para mostrar à pessoa como fica antes de ela ter dados próprios.

### Planilha de pedidos

`pedidos-de-certidoes.csv` (separador `;`, abre direto no Excel) tem uma linha por certidão pedida ou a pedir: documento, pessoa, órgão ou cartório, contato, tipo de certidão (breve relato, inteiro teor, digitada, reprográfica), finalidade, data do pedido, custo estimado e pago, prazo, status e data de recebimento. Mantenha-a atualizada a cada pedido e a cada resposta. Antes de sugerir um pedido pago, diga o custo estimado e se existe alternativa gratuita.

### Registro de pesquisas

Toda busca feita, com ou sem resultado, vai para `pesquisas/AAAA-MM-DD-assunto.md`: onde buscou, quais termos e variantes, que intervalo de datas, quantos registros conferiu e o que encontrou. Uma busca sem resultado bem documentada evita repetir o mesmo trabalho e mostra o que ainda não foi tentado.

### Figuras conhecidas e origem

Cada pessoa aparece na árvore com um ícone do país, reino ou povo onde nasceu. O script deduz sozinho a partir do local e da data de nascimento (ou batismo): Portugal antes de 05/10/1910 vira Reino de Portugal, Brasil entre 1822 e 15/11/1889 vira Império do Brasil, Itália entre 1861 e 1946 vira Reino de Itália, e assim por diante. Para isso, termine o `local` com o país ("Mansores, Arouca, Aveiro, Portugal") ou, no Brasil, com a sigla do estado ("Botucatu, SP"). Quando a data não decide a época, o ícone vira a sigla do país e o nome diz "época incerta". Declare `origem` à mão quando a dedução não serve: povos indígenas e africanos, estados anteriores à unificação italiana ou alemã, impérios e regiões que mudaram de dono (formato em `references/formato-pessoas-json.md`).

A estrela marca quem é figura conhecida na história: aparece em enciclopédia, dicionário biográfico, acervo de museu, livro de história ou imprensa da época como personagem, e não só como nome numa lista. Regras:

- **Pergunte antes de pesquisar.** Buscar nomes na web manda esses nomes a um serviço externo. Peça autorização à pessoa e pesquise só antepassados já falecidos, com nome, lugar e época. Nunca pesquise pessoas vivas.
- **Homônimo não é parente.** Só marque `confirmado` quando um documento da família e a fonte sobre a figura conhecida concordam em pontos que identificam a pessoa (pais, cônjuge, lugar e datas). Diga na `nota` quais pontos batem.
- **Lenda de família é relato.** "Somos parentes do Marquês de Pombal" entra como `relato`, com quem contou, e aparece com estrela vazada (☆) até ser provado. Parentesco com alguém famoso que não está na árvore vai nas `notas` da pessoa, não em `destaque`.
- **Fonte com link e data.** Todo destaque tem resumo curto, pelo menos um link e a data da consulta. Prefira fontes institucionais (arquivos, museus, bibliotecas nacionais, dicionários biográficos); Wikipédia serve como ponto de partida, mas confira o que ela cita.
- **Sem achado, sem estrela.** Se a pesquisa não achar nada, registre a busca no log de pesquisas e não marque ninguém.

## Conversa com a pessoa

Quem usa esta skill geralmente não é técnico. Explique em linguagem simples, mostre o resultado (abra a árvore no navegador quando possível) e, quando precisar de uma decisão, ofereça opções de múltipla escolha. Comemore achados, mas separe sempre o que está provado do que é provável.
