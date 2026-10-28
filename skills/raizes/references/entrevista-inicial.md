# Entrevista inicial

São quatro rodadas. A rodada 2 coleta os dados das pessoas com perguntas abertas, uma geração por mensagem. As outras usam até quatro perguntas de múltipla escolha por vez. Sempre aceite resposta livre e "não sei".

## Rodada 1: objetivo e origem

1. **O que você quer fazer primeiro?**
   - Montar a árvore e guardar a história da família
   - Ver se tenho direito a uma cidadania europeia e montar o pedido
   - As duas coisas
2. **De que país vem a família que você quer pesquisar?** (múltipla seleção: é comum ter mais de uma origem)
   - Portugal
   - Itália
   - Espanha
   - Outro ou não sei
3. **Quem é o antepassado que veio de lá?**
   - Pai ou mãe
   - Avô ou avó
   - Bisavô ou bisavó
   - Mais longe ou não sei
4. **Onde guardar a pasta do projeto?** (sugira `Documentos/Familia-<Sobrenome>`; ou outra pasta que a pessoa indicar)

Crie o projeto (`arvore-documental`, comando `iniciar`) logo depois desta rodada, para que os dados da rodada 2 sejam gravados à medida que chegam e nada se perca se a conversa cair.

## Rodada 2: os dados de cada pessoa

Antes de começar, diga em uma frase que os dados ficam só na pasta do projeto, no computador da pessoa, e que "não sei" é uma resposta normal. Não peça CPF, RG, endereço, telefone nem documentos neste momento: não servem para a árvore.

Pergunte uma geração por mensagem, nesta ordem, mandando um bloco para a pessoa copiar e preencher. Ela também pode responder do jeito dela, em texto corrido.

**1. A própria pessoa**

```
Você
- Nome completo:
- Sexo (masculino / feminino / prefiro não dizer):
- Data de nascimento:
- Cidade, estado e país de nascimento:
```

**2. Os pais**

```
Seu pai
- Nome completo:
- Data de nascimento (ou ano aproximado):
- Cidade, estado e país de nascimento:
- Está vivo? (sim / não; se não, ano do falecimento e cidade)

Sua mãe
- Nome completo de solteira (e o de casada, se mudou):
- Data de nascimento (ou ano aproximado):
- Cidade, estado e país de nascimento:
- Está viva? (sim / não; se não, ano do falecimento e cidade)

Seus pais se casaram? (sim / não / não sei; se sim, cidade e ano)
```

**3. Os avós**, o mesmo bloco para cada um dos quatro, identificados assim: pai do seu pai, mãe do seu pai, pai da sua mãe, mãe da sua mãe. Inclua a pergunta do casamento para cada casal.

Depois dos avós, gere a árvore (`tudo`) e mostre no navegador antes de seguir. Ver a árvore com três gerações ajuda a pessoa a lembrar de quem falta.

**4. Os bisavós, se a pessoa souber.** São oito; peça ao menos o nome e o país ou a cidade de origem, e o resto do bloco quando houver. Comece pela linha da origem estrangeira marcada na rodada 1. Se o antepassado estrangeiro estiver mais longe (trisavô), siga subindo só por essa linha.

Se a pessoa não souber quase nada de uma geração, não insista: anote quem na família pode saber (rodada 3) e siga.

### Como gravar

- Cada pessoa vira uma entrada em `pessoas.json` com `nome`, `sexo` (pai e avôs `M`, mãe e avós `F`; para a própria pessoa, o que ela disse, ou `?`), `pais` e eventos de `nascimento` e, se for o caso, `obito`.
- Tudo o que vem da entrevista tem `status: "relato"` e `nota` com quem contou e a data da conversa ("Contado por Larisse em 28/10/2026"). Se a pessoa disser que tem o documento mas não o mostrou, acrescente "documento em mãos, não conferido".
- A filiação também é relato: `"filiacao": {"status": "relato", "nota": "..."}`.
- Ano aproximado vira `c. 1932`; "entre 40 e 45" vira `entre 1940 e 1945`. Não invente dia nem mês.
- Nome de solteira vai em `nome`; o nome de casada vai em `variantes`.
- Casamento dos pais e dos avós vai em `unioes`, também como relato.
- Quando a pessoa der duas versões para o mesmo dado, ou quando a versão dela conflitar com a de outro parente, registre em `divergencias` com `relato`. Não escolha uma em silêncio.
- Em seguida, rode `validar` e corrija os avisos.

## Rodada 3: família e documentos

Para cada origem marcada na rodada 1, confirme de que lado vem e quem de cada geração intermediária está vivo (os dados da rodada 2 já costumam responder). Isso decide a via de cidadania: em vários países, um filho vivo do imigrante abre um caminho que um neto não tem.

1. **Você já tem algum documento do antepassado estrangeiro?**
   - Certidão de nascimento ou batismo dele
   - Certidão de casamento ou de óbito dele no Brasil
   - Passaporte, carteira de estrangeiro ou documento de imigração
   - Nada ainda, só o que a família conta
2. **Quem da família ainda pode contar histórias ou tem papéis guardados?** (múltipla seleção: pais, avós, tios, primos, ninguém)
3. **Você tem as suas certidões e as dos seus pais?** (as minhas e as dos meus pais; só as minhas; não sei onde estão)
4. **Alguém da família já tentou essa cidadania ou já tem?** (sim, um parente já tem; já tentaram e pararam; não que eu saiba)
5. **Alguém da linha se naturalizou brasileiro?** (sim; não; não sei). Explique por que importa: em alguns países a naturalização antes do nascimento do filho corta a transmissão.

Faça no máximo quatro por mensagem; a quinta vai na seguinte.

## Rodada 4: prática

1. **Quanto você quer gastar por enquanto?**
   - Só caminhos gratuitos
   - Pequenos gastos com certidões, avisando antes
   - O necessário para fazer o pedido
2. **Como você prefere ver os dados?**
   - Só a árvore no navegador
   - Também fichas por pessoa (funcionam no Obsidian ou em qualquer editor)
   - Também exportar para FamilySearch ou MyHeritage
3. **Quer que eu prepare rascunhos de e-mails para cartórios e arquivos?** (sim, e eu envio; não por enquanto)

## Depois da entrevista

1. Complete o arquivo de regras e o `plano-de-trabalho.md` com as decisões.
2. Gere a árvore de novo com tudo o que foi contado.
3. Se o objetivo inclui cidadania, leia a skill do país e diga, com a ressalva de conferir a fonte oficial, se a linha descrita parece ter via possível e qual é o primeiro documento a buscar.
4. Proponha os três próximos passos, do mais barato e rápido ao mais caro. Um deles costuma ser pedir à pessoa fotos das certidões que ela já tem, para trocar os relatos por dados confirmados.
