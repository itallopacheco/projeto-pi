# Identificação e contabilização de Objetos e Objetos furados em imagens .PBM
  O trabalho desenvolvido é referente ao trabalho final da disciplina de Processamento de Imagens ofertada no período 2022.2 da UFS.
  O programa deve ser capaz de ler imagens preto e branco .PBM, contar e informar o número de objetos com buraco e o número de objetos sem buraco.
  Não foram impostas limitações sobre forma dos objetos ou buracos, considerando a definição de objeto e de buraco vistas no documento de instruções do trabalho.

# Entrada do Programa:
Ao compilar, programa roda para todas as imagens dentro da pasta testes.
```
Basta adicionar as imagens a pasta /testes antes de rodar o programa
```

# Saida do Programa:
Ao finalizar, o programa exibirá os resultados no terminal, como também criará uma pasta chamada resultados, e para cada caso de teste uma pasta dentro de resultados. Dentro da pasta do caso de teste x estarão imagens intermediárias em PGM do processo de reconhecimento de objetos e buracos.
``` 
 📁 resultados
    📁 {{nome do teste}}
        📁 imagens_intermediarias.pgm
    
```
# Instruções de instalação:
- 1 - Clone o repositório com ```git clone https://github.com/itallopacheco/projeto-pi.git``` e vá para a pasta do repositório.
- 2 - Dentro do repositório você pode criar um ambiente virtual com ```python -m venv venv ```
- 3 - Ative o ambiente virtual com ````source/venv/bin/activate ```
- 4 - Com o ambiente virtual aberto, use o comando ```pip install -r requirements.txt ``` para instalar as dependências (usamos a classe Image do Pillow para ler as imagens com mais facilidade) 
- 5 - Tudo pronto, agora você pode rodar o arquivo count-objects.py com ```python count-objects.py ``` para executar o programa para todas as imagens pré escolhidas na pasta /testes OU você pode alterar o conteúdo da pasta /testes para executar o programa nas imagens de sua preferência

# Observações 
O programa foi atualizado substituindo o flood-fill recursivo por uma versao usando pilha, isso resolveu em partes o problema de otimização, sendo agora possível rodar para imagens maiores (o tempo de espera vai variar de máquina pra máquina). 
