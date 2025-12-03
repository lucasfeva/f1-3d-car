# 🏎️ Simulação 3D de Carro de Fórmula 1 - Mercedes W16

## 📋 Descrição do Projeto

Este projeto consiste em uma simulação gráfica 3D de um carro de Fórmula 1 (modelo Mercedes W16) desenvolvida em Python utilizando OpenGL para renderização 3D e Pygame para controle de janela e eventos. O carro é renderizado em uma pista de corrida com animações interativas controladas pelo usuário.

## 🎯 Objetivos

- Criar um modelo 3D detalhado de um carro de Fórmula 1
- Implementar animação interativa iniciada pelo usuário
- Simular movimento realista das rodas e pneus
- Adicionar elementos móveis extras ao veículo (DRS)
- Criar uma pista de corrida com efeito visual de movimento

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Descrição                                    |
| ---------- | ------ | -------------------------------------------- |
| Python     | 3.x    | Linguagem de programação principal           |
| PyOpenGL   | 3.1.6  | Binding Python para OpenGL - renderização 3D |
| Pygame     | 2.5.2  | Biblioteca para controle de janela e eventos |
| OpenGL     | -      | API gráfica para renderização 3D             |
| GLU        | -      | OpenGL Utility Library                       |

## 📦 Dependências

```
PyOpenGL==3.1.6
pygame==2.5.2
numpy==1.26.4
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.x instalado
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone ou baixe o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o programa:

```bash
python main.py
```

## 🎮 Controles

| Tecla            | Ação                            |
| ---------------- | ------------------------------- |
| `SPACE`          | Iniciar/Parar animação do carro |
| `←` `→` `↑` `↓`  | Rotacionar câmera               |
| `+` / `-`        | Zoom in/out                     |
| `Scroll Mouse`   | Zoom in/out                     |
| `Arrastar Mouse` | Rotacionar câmera               |
| `ESC`            | Sair do programa                |

## 🏗️ Estrutura do Projeto

```
f1-3d-car/
├── main.py              # Código principal do projeto
├── requirements.txt     # Dependências do projeto
├── README.md           # Documentação (este arquivo)
└── petronas-patrocinador.png  # Imagem de referência
```

## 📐 Arquitetura do Código

### Componentes Principais

O código está organizado em seções bem definidas:

1. **Variáveis Globais de Animação**

   - Controle de estado da animação
   - Rotação das rodas
   - Ângulo de direção
   - Estado do DRS
   - Posição da câmera

2. **Funções de Desenho Primitivas**

   - `draw_solid_cube()` - Desenha cubos sólidos
   - `draw_quad()` - Desenha quadriláteros
   - `draw_polygon()` - Desenha polígonos

3. **Componentes do Chassi**

   - `draw_monocoque()` - Chassi principal (monocoque)
   - `draw_engine_cover()` - Cobertura do motor
   - `draw_nose()` - Bico do carro
   - `draw_sidepods()` - Sidepods (radiadores laterais)
   - `draw_cockpit()` - Cockpit do piloto
   - `draw_halo()` - Dispositivo de proteção Halo
   - `draw_floor()` - Assoalho
   - `draw_diffuser()` - Difusor traseiro
   - `draw_airbox()` - Entrada de ar

4. **Aerodinâmica**

   - `draw_front_wing()` - Asa dianteira
   - `draw_rear_wing()` - Asa traseira (com DRS animado)

5. **Suspensão**

   - `draw_front_suspension()` - Suspensão dianteira
   - `draw_rear_suspension()` - Suspensão traseira
   - `draw_suspension_bar()` - Braços de suspensão

6. **Rodas**

   - `draw_wheel()` - Roda completa com pneu Pirelli
   - `draw_wheels_on_suspension()` - Posiciona as 4 rodas

7. **Pista de Corrida**

   - `draw_track()` - Desenha a pista com linhas e zebras

8. **Animação e Controles**
   - `update_animation()` - Atualiza estado da animação
   - `toggle_animation()` - Liga/desliga animação
   - `main()` - Loop principal com Pygame

## ✨ Funcionalidades Implementadas

### ✅ Animação Iniciada pelo Usuário

- A animação é iniciada ao pressionar a tecla SPACE
- Continua automaticamente até ser pausada novamente

### ✅ Movimento das Rodas e Pneus

- As 4 rodas giram proporcionalmente à velocidade simulada
- Rotação realista dando impressão de movimento
- Rodas dianteiras com sistema de direção (pequena oscilação)

### ✅ Animação com Início, Meio e Final

- **Início**: Carro parado na pista
- **Meio**: Carro em movimento contínuo com rodas girando
- **Final**: Animação pode ser pausada a qualquer momento

### ✅ Pista em Movimento

- Linhas tracejadas centrais se movem
- Zebras (kerbs) nas laterais animadas
- Efeito visual de velocidade

### ✅ Elemento Móvel Extra - DRS (Drag Reduction System)

- Asa traseira com flap móvel
- DRS abre automaticamente quando o carro está em movimento
- Animação suave de abertura/fechamento

### ✅ Detalhes Visuais

- Pneus Pirelli com faixa amarela
- Detalhes turquesa (cores Mercedes/Petronas)
- Espelhos retrovisores
- Halo de proteção
- Luz de chuva traseira

## 🎨 Características Visuais

### Modelo do Carro

- Baseado no Mercedes-AMG F1 W16
- Cores: Preto carbono com detalhes turquesa (Petronas)
- Proporções realistas de um carro de F1 moderno

### Iluminação

- Duas fontes de luz para iluminação ambiente
- Sombreamento suave (GL_SMOOTH)
- Material com propriedades de cor ambiente e difusa

### Câmera

- Câmera orbital ao redor do carro
- Controle por mouse (arrastar) e teclado (setas)
- Zoom com scroll ou teclas +/-

## 📊 Especificações Técnicas

- **Resolução da Janela**: 1200 x 800 pixels
- **Taxa de Atualização**: 60 FPS
- **Projeção**: Perspectiva (45° FOV)
- **Segmentos por Roda**: 48 (alta qualidade)

## 👥 Autores

- Lucasfeva

## 📚 Referências

- OpenGL Programming Guide
- Pygame Documentation: https://www.pygame.org/docs/
- PyOpenGL Documentation: http://pyopengl.sourceforge.net/
- Fórmula 1 Mercedes w16 2023aa
