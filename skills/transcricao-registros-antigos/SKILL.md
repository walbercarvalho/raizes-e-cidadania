---
name: transcricao-registros-antigos
description: Transcreve e confere registros antigos manuscritos ou em formulário preenchido à mão, como assentos paroquiais de batismo, casamento e óbito, registros civis, listas de passageiros, passaportes, fichas de imigração e certidões antigas, em português, italiano, espanhol ou latim. Use sempre que a pessoa mandar a imagem ou o PDF de um documento antigo da família para ler, extrair nomes, datas e pais, ou conferir uma leitura feita por outra pessoa ou por um site. Não use para documentos modernos digitados.
---

# Transcrição de registros antigos

Uma leitura errada de um nome ou de uma data contamina a árvore inteira e pode derrubar um pedido de cidadania. Por isso a transcrição separa o que está escrito do que foi interpretado, e toda dúvida fica marcada.

## Leitura

1. Abra a imagem inteira só para achar o assento certo e entender o layout (colunas, margens, outros assentos na página). Não tire conclusões sobre palavras a partir da imagem inteira: em resolução reduzida, letras parecidas se confundem.
2. Recorte faixas de 3 a 6 linhas e amplie de 2,5 a 4 vezes. Com Python e Pillow:
   ```python
   from PIL import Image
   im = Image.open("pagina.jpg")
   faixa = im.crop((x0, y0, x1, y1))
   faixa.resize((faixa.width * 3, faixa.height * 3), Image.LANCZOS).save("recorte-01.png")
   ```
   Para uma palavra difícil, recorte só ela. Salve recortes numa pasta temporária, nunca junto dos originais. PDF: renderize a página (`pymupdf`: `page.get_pixmap(dpi=200)`) ou extraia a imagem embutida. Se faltar Pillow, `pip install pillow pymupdf`.
3. Compare cada letra duvidosa com outras ocorrências da mesma mão: no mesmo assento, nos assentos vizinhos, na página anterior. O escrivão repete as mesmas palavras (nomes de meses, "filho legítimo", o nome da freguesia), e elas servem de alfabeto.
4. Use a fórmula fixa do tipo de registro para se orientar (ver `references/formulas-e-abreviaturas.md`), mas o documento prevalece: se o texto contradiz o esperado, transcreva o que está escrito e registre a divergência.
5. Nunca complete um trecho ilegível com o nome que se espera encontrar. O que vem de outro documento vai para as notas, com a fonte.

## Marcação

- Grafia original na transcrição diplomática: Jozé, nasceo, freguezia, fr.ª, Joaq.m. Não atualize ortografia nem desdobre abreviaturas nessa camada.
- Dúvida: melhor leitura seguida de `[?]`. Alternativa: `[?: outra leitura]`. Impossível: `[ilegível]` ou `[ilegível, ~2 palavras]`.
- Margens, rubricas, assinaturas e averbações em linhas próprias: `[margem esquerda: ...]`, `[assinatura: ...]`, `[rubrica]`, `[averbação posterior, outra letra: ...]`.
- Se a página tem vários assentos, transcreva só o da família e cite os demais em uma linha (número e nome), porque às vezes um vizinho é parente.

## Arquivo de transcrição

Nome: `transcricoes/AAAA-MM-DD-tipo-pessoa-lugar.md` (data do fato, minúsculas, hifens). Conteúdo, nesta ordem e sem misturar camadas:

1. Uma ou duas frases: que documento é, onde está o original (arquivo, cota, imagem, folha) e o que ele prova.
2. `## Dados do registro`: tabela de interpretação, em grafia atual, datas em dd/mm/aaaa, parentescos explícitos. Campos obrigatórios (escreva "não consta" quando faltar): nome do registrado e condição (legítimo, natural, exposto); data do fato; data do registro; lugar (freguesia ou distrito, município, província ou distrito administrativo, país); pais com naturalidade e morada; avós paternos e maternos; padrinhos ou testemunhas; declarante; pároco ou oficial; acervo, cota, imagem e folha; averbações.
3. `## Transcrição diplomática`: linha a linha, numerada, como está no papel.
4. `## Transcrição atualizada`: texto corrido com abreviaturas desdobradas e ortografia atual; nomes próprios como no documento.
5. `## Notas de leitura`: cada dúvida com as alternativas e o motivo da escolha; leituras anteriores que foram descartadas; divergências com outros documentos da mesma pessoa; problemas físicos da imagem.

Para registros em italiano, espanhol ou latim, mantenha a diplomática no idioma original e faça a atualizada em português, avisando que é tradução livre (para órgãos oficiais vale só tradução juramentada).

## Ao terminar

1. Compare com tudo o que já existe sobre as mesmas pessoas (procure o nome nas outras transcrições e no `pessoas.json`). Cada diferença de nome, data, idade, lugar ou filiação vai para as Notas de leitura e para `divergencias` no `pessoas.json`.
2. Atualize o núcleo documental com a skill `arvore-documental` (documento, eventos, filiação, status `confirmado` com a fonte).
3. Se o documento prova um elo de uma cadeia de cidadania, avise a pessoa e atualize a matriz de prova da skill de cidadania correspondente.
4. Diga claramente o que ficou incerto. Uma transcrição honesta com três `[?]` vale mais que uma limpa e errada.

Fórmulas típicas de cada registro, abreviaturas e termos em português, italiano, espanhol e latim estão em `references/formulas-e-abreviaturas.md`.
