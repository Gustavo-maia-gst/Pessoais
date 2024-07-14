# Pessoais
Projetos gerais que desenvolvi.

# Python/math/polynomial.py
### Geral
Esse módulo apresenta uma abstração para a representação de polinômios em python, a classe `Polynomial` é inicializada com uma string do tipo `'+axn +bxm'` para ax^n + bx^m, ela pode ser usada para operações básicas entre polinômios, como multiplicação e divisão, mas o principal foco é o rootfinding.

### RootFinding
Quanto ao algoritmo, funciona da seguinte forma:
1. Você começa com um guess inicial (esse valor é determinante para o sucesso do algoritmo) e calcula a intersecção da reta derivada naquele ponto x com o eixo x, e o guess passa a ser esse ponto de intersecção, é fácil visualizar que nas circunstâncias onde existe uma raíz entre o guess e o ponto crítico mais próximo, esse guess irá convergir para a raíz (a imagem abaixo mostra isso graficamente). O método que usei para maximizar os casos onde existe uma convergência, foi usando o teorema de Cauchy para as raízes complexas de um polinômio, ele diz que todas as raízes estão no círculo de raio igual ao coeficiente de maior módulo do polinômio, e com centro na origem do plano complexo, eu setei dois boundaries, como sendo as extremidades reais onde as raízes podem estar, e coloquei dois ponteiros como guesses começando um em cada boundarie. Caso algum dos ponteiros chegue em uma raíz, ele retorna o valor dessa raíz, caso o ponteiro seja lançado para fora dos boundaries, o ponteiro é setado para None, no caso dos dois ponteiros serem setados para None, é assumido que o polinômio não possui raízes reais. Essa parte do algoritmo é realizado pelo método `_find_root` da classe `Polynomial`.
   
![Convergência](https://media.geeksforgeeks.org/wp-content/uploads/20230704172946/Newton-Raphson-Method.png)

2. O método estático `roots` é o que realmente encontra todas as raízes, ele funciona chamando o método `find_root`, dividindo o polinômio por (x - r) onde r é a raiz encontrada, e resolvendo o polinômio de menor grau recursivamente. O caso da base da recursão é o grau 2, onde é usado a fórmula de Bháskara para encontrar as raízes.
3. Nos casos onde o coeficiente é ímpar, ao menos uma raíz sempre será encontrada, existe a possibilidade que o algoritmo falhe em polinômios de grau par maior ou igual 6 sem raízes nos pontos críticos extremos, o que é bem raro.

# Database/LogDB
O LogDB é um protótipo de banco de dados estruturado em log com hash, ele trabalha com uma tabela hash entre o id do objeto e o offset no arquivo binário da posição do objeto. Uma coisa interessante desse módulo é a serialização das classes C++ para objetos binários que são salvos em disco. Existem 4 classes principais:

`LogModel`: Essa classe representa o modelo base serializável, ela implementa o métodos para serialização dos tipos primitivos usados pelas classes filhas.

`LogRepository`: Classe que fornece a abstração de repository para as classes que herdam de LogModel, funciona como os repositories fornecidos pelos ORM de linguagens de alto nível.

`SegmentManager`: Realiza a comunicação entre o repository e os arquivos, lidando também com tarefas como a compressão dos logs, que envolve recriar os arquivos.

`SegmentFile`: Essa classe é uma abstração para um arquivo de segmento usado para armazenar algum model.

# Python/donnut3.py
Bom, o nome é autoexplicativo, é um donnut girando na tela.
Para gerar a imagem é usado a projeção de um torus sendo rotacionado em dois eixos, o programa foi gerado sem usar nenhuma equação paramétrica para a figura.

# Python/math/matrices.py
Esse módulo implementa algumas funções interessantes para se lidar com matrizes e sistemas lineares, o core do módulo está na função `row_reduce` que realiza a eliminação gaussiana (combinações lineares entre as linhas da matriz para diagonalizá-la).
Uma função interessante é a `solve`, ela funciona quase da mesma forma que a row_reduce em uma matriz contendo o sistema linear e o vetor resultado, entretanto o objetivo é obter uma matriz identidade, que representa a solução, que sempre existirá se o determinante da matriz não for nulo.

# Python/nino/nino.py
Esse módulo é basicamente uma tentativa de recriação da biblioteca curses usando python, foi usado apenas a biblioteca evdev para capturar eventos de teclado, o que acredito não ser possível usando python puro. Uma coisa interessante é o objeto `keyboard` da classe passada como parâmetro para a função a ser executada no wrapper, esse objeto possui o decorador `@keyboard.listener` que abre uma thread listener para os eventos de teclado executando a função decorada passando como parâmetro o event. Outra implementação interessante é o `WrapperContextManager` que faz o gerenciamento de contexto e é responsável por detalhes como manter o cursor escondido, dar grab no teclado, já que não consegui abrir um buffer separado sem usar bibliotecas externas, e certificar-se que essas alterações serão desfeitas antes do término do programa.

- O módulo `snake.py` é um jogo da cobrinha bem básico usando a nino.

# Python/math/complex.py
Esse módulo possui uma bonita representação de números complexos usando python, estão definidas praticamente todas as operações com excessão a exponenciação com expoente complexo.
A principal adição desse módulo em relação a implementação original do python para complexos (além do visual) é a possibilidade de encontrar todas as n-raizes em uma raíz enésima usando o método `all_roots`.

# Assembly
A pasta assembly possui alguns códigos em assembly, são coisas simples como fibonacci, algoritmos de ordenação simples e etc.
