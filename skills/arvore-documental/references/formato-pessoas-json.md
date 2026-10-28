# Formato do pessoas.json

Um único arquivo JSON, em UTF-8, guarda todos os dados da árvore. O `arvore.py` lê esse arquivo e gera o resto. Exemplo completo e fictício: `../assets/exemplo/pessoas.json`.

## Topo

```json
{
  "familia": "Família Ferreira",
  "pessoa_central": "clara",
  "atualizado": "2026-10-27",
  "pessoas": [],
  "unioes": [],
  "documentos": [],
  "divergencias": [],
  "cadeias": []
}
```

- `pessoa_central`: id de quem aparece primeiro na árvore (normalmente quem está fazendo a pesquisa).

## Pessoa

```json
{
  "id": "manuel",
  "nome": "Manuel Ferreira da Silva",
  "sobrenome": "Ferreira da Silva",
  "variantes": ["Manoel Ferreira"],
  "sexo": "M",
  "pais": ["joaquim", "ana"],
  "filiacao": {"status": "confirmado", "fontes": ["doc-manuel-bat"]},
  "profissao": "carpinteiro",
  "eventos": [
    {"tipo": "batismo", "data": "1895-03-12", "local": "Freguesia X, Concelho Y, Portugal",
     "status": "confirmado", "fontes": ["doc-manuel-bat"], "nota": "Nascido em 05/03/1895 segundo o assento."}
  ],
  "notas": "Texto livre curto."
}
```

- `id`: curto, sem espaços nem acentos, único (`manuel`, `manuel-1895` se houver dois).
- `sobrenome` é opcional; serve para o GEDCOM separar nome e sobrenome em nomes compostos. Sem ele, a última palavra vira sobrenome.
- `sexo`: `M`, `F` ou `?`.
- `pais`: ids do pai e da mãe (até dois). `filiacao` diz qual documento prova esse vínculo. Para cidadania, a filiação é tão importante quanto o nascimento: é ela que liga um elo ao outro.
- `eventos[].tipo`: `nascimento`, `batismo`, `casamento`, `obito`, `sepultamento`, `imigracao`, `emigracao`, `naturalizacao`, `residencia`, `outro`. Casamentos entre duas pessoas cadastradas vão em `unioes`; o tipo `casamento` em eventos é só para quando o cônjuge não está cadastrado.

### Origem (opcional)

Sem o campo, o script deduz a origem do local e da data de nascimento (ou batismo) e mostra o ícone do Estado da época. Use o campo só quando a dedução não serve:

```json
"origem": {"icone": "", "nome": "Reino das Duas Sicílias", "nota": "Nascido em Padula antes da unificação (batismo de 1850)."}
```

- `nome`: país, reino, império ou povo, como deve aparecer.
- `icone`: um destes, ou vazio para mostrar a sigla do nome: `br`, `br-imperio`, `pt`, `pt-reino`, `it`, `it-reino`, `es`, `es-rep`, `jp`, `ar`, `fr`, `de`, `de-imperio`, `at`, `at-hu`, `pl`, `lb`, `otomano`, `us`. Os ícones são simplificados e não reproduzem a bandeira oficial exata de cada período.
- `nota`: de onde vem a informação. Origem que vem de relato diz quem contou.

### Destaque: figura conhecida (opcional)

```json
"destaque": {
  "resumo": "Pintor decorador; assinou o forro da igreja matriz de X em 1912.",
  "links": [{"titulo": "Dicionário de pintores do Brasil, verbete", "url": "https://..."}],
  "status": "confirmado",
  "fontes": ["doc-joaquim-obito"],
  "nota": "O verbete dá os mesmos pais, a mesma freguesia e o ano de nascimento do batismo.",
  "consultado": "2026-10-28"
}
```

- Na árvore, `confirmado` mostra ★; `relato` e `hipotese` mostram ☆.
- `confirmado` exige documento da família em `fontes` e uma `nota` com o que prova que a figura conhecida é a mesma pessoa. Uma página da web pode ser cadastrada como documento com o campo `url`.
- `links` precisam de endereço `http` ou `https`. `consultado` é a data em que as fontes foram abertas.

## Datas

| Situação | Formato |
| --- | --- |
| Data completa | `1895-03-12` |
| Mês e ano | `1895-03` |
| Só o ano | `1895` |
| Aproximada | `c. 1895` |
| Intervalo | `entre 1943 e 1950` (também aceita datas completas) |
| Limite | `antes de 1950`, `depois de 1943` |

Datas fora desse padrão geram aviso e vão para o GEDCOM como nota. Calcule nascimento a partir de idade declarada só como `c. AAAA`, com `status: "hipotese"` e a conta na nota.

## Status

- `confirmado`: exige pelo menos um id em `fontes`, e o documento precisa ter sido visto (foto, PDF ou imagem de acervo). Documento que a família diz ter, mas que não foi mostrado, fica como `relato` com a nota "documento em mãos, não conferido".
- `relato`: exige `nota` com quem contou e quando.
- `hipotese`: dedução; explique o raciocínio na `nota`.

## União

```json
{"id": "u-manuel-maria", "pessoas": ["manuel", "maria"], "tipo": "casamento civil",
 "data": "1920-05-08", "local": "Santos, SP, Brasil", "status": "confirmado", "fontes": ["doc-manuel-cas"]}
```

`tipo` livre: `casamento civil`, `casamento religioso`, `união`. Uniões sem documento podem ficar sem `status` (aparecem como "falta" nas pendências).

## Documento

```json
{"id": "doc-manuel-bat", "tipo": "assento de batismo", "titulo": "Batismo de Manuel, 1895",
 "data": "1895-03-12", "local": "Viana do Castelo", "pessoas": ["manuel", "joaquim", "ana"],
 "acervo": "Arquivo Distrital de Viana do Castelo", "cota": "PT/ADVCT/PRQ/...", 
 "arquivo": "documentos-organizados/1895-03-12 Batismo - Manuel Ferreira da Silva - Freguesia X.jpg",
 "original": "documentos-originais/IMG_2041.jpg",
 "transcricao": "transcricoes/1895-03-12-batismo-manuel-ferreira-da-silva.md",
 "observacoes": "Imagem do arquivo online; certidão oficial ainda não pedida."}
```

- `arquivo`, `original` e `transcricao` são caminhos relativos à pasta do `pessoas.json`. O validador avisa quando o arquivo não existe.
- `url` (opcional): endereço de uma fonte online, como um verbete ou o registro num acervo digital. A árvore usa o link quando não há arquivo local.
- Em `observacoes`, diga se é imagem de arquivo online, certidão oficial (e de quando), cópia simples ou foto de documento da família. Para cidadania isso muda tudo: imagem online prova o fato, mas o órgão quase sempre exige certidão oficial.

## Divergência

```json
{"pessoa": "manuel", "campo": "ano de nascimento",
 "valores": [{"valor": "1895", "fonte": "doc-manuel-bat"}, {"valor": "c. 1893 (78 anos)", "fonte": "doc-manuel-obito"}],
 "nota": "O batismo prevalece; a idade no óbito foi declarada por terceiro."}
```

Quando uma das versões vem de relato e não de documento, use `relato` no lugar de `fonte`, dizendo quem contou e quando: `{"valor": "bisavó materna", "relato": "Clara, conversa de 27/10/2026"}`. Conflito entre dois relatos também se registra assim, até um documento resolver.

## Cadeia de cidadania

```json
{"nome": "Portugal pelo bisavô Manuel", "nacionalidade": "PT", "elos": ["manuel", "antonio", "paulo", "clara"]}
```

`elos` vai do ascendente estrangeiro até quem vai pedir, na ordem. Cada elo seguinte precisa ter o anterior na lista `pais` da pessoa (pai ou mãe); o validador acusa erro quando não tem. `nacionalidade`: `PT`, `IT`, `ES` ou outro código de país. Uma pessoa pode estar em mais de uma cadeia (por exemplo, uma pelo lado da mãe para a Itália e outra pelo lado do pai para a Espanha).
