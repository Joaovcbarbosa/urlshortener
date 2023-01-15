# Execucao

Para compilar, dentro da pasta do projeto execute o comando:

```bash
make
```

Para executar, execute o comando:

```bash
./exe codigos/gcd.txt
```

Dois arquivos serão gerados:
- arquivoPreProcessado.txt: Mesmo conteúdo do arquivo de entrada, porém sem comentários.
- arquivoSaida.txt: Árvore de análise sintática e tabela de símbolos.

Obs.: Caso sejam detectados erros, estes aparecerão no console e o arquivo "arquivoSaida.txt" ficará incompleto.
Obs2.: As linhas referenciadas nos avisos de erros e na tabela de símbolos são de acordo com o "arquivoPreProcessado.txt".
