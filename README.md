# Factory Vision

Factory Vision é um projeto de visão computacional para evoluir, de forma
incremental e responsável, o monitoramento de uma fábrica de portas. O objetivo
geral inclui futuramente contar portas, medir o fluxo de produção, identificar
paradas, analisar tempos de ciclo e detectar defeitos.

## Status atual

**v0.0.2 — Primeira detecção**

Esta versão preserva o pipeline de vídeo da v0.0.1 e adiciona detecção de objetos
frame a frame com Ultralytics YOLO. A aplicação desenha bounding boxes, nomes de
classes e confianças, mas ainda não conta portas nem rastreia objetos.

## Funcionalidades atuais

- validação e abertura de arquivos de vídeo locais;
- leitura sequencial e liberação segura dos recursos;
- exibição do número do frame, FPS e resolução;
- carregamento único de um modelo YOLO local;
- inferência frame a frame em CPU;
- limiar de confiança configurável;
- bounding boxes com nome da classe e confiança;
- encerramento ao final do vídeo ou ao pressionar `Q`;
- testes sem janelas, GPU, vídeos privados ou downloads de pesos.

## Tecnologias utilizadas

- Python 3;
- OpenCV;
- Ultralytics YOLO;
- pytest.

## Requisitos

- Python 3.10 ou superior;
- terminal do Windows PowerShell;
- sessão gráfica disponível para a janela de reprodução;
- codec compatível com o vídeo;
- modelo de detecção compatível com Ultralytics, armazenado localmente.

A inferência usa explicitamente CPU. Nenhuma GPU é necessária.

## Instalação no Windows

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se a política de execução bloquear a ativação, libere scripts somente para a
sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

A instalação do Ultralytics inclui seu runtime de inferência, mas este projeto
não baixa nem distribui pesos de modelos.

## Modelo YOLO

O argumento `--model` é obrigatório e deve apontar para um arquivo local. Por
exemplo:

```text
models/model.pt
```

Arquivos `.pt`, `.pth` e `.onnx` estão ignorados pelo Git. Obtenha o modelo
por uma fonte autorizada e mantenha pesos privados fora do repositório.

Um modelo oficial pré-treinado da Ultralytics pode ser usado como baseline para
demonstrar tecnicamente o pipeline. Modelos genéricos reconhecem apenas as
classes de seus próprios datasets e **não devem ser considerados detectores
confiáveis de portas industriais**. Uma detecção específica de portas depende
de pesos apropriados, avaliados com dados representativos e autorizados.

## Como executar

Com o ambiente virtual ativado:

```powershell
python -m src.factory_vision.main "data/private/test_720p.mp4" --model "models/model.pt"
```

Para definir o limiar mínimo de confiança:

```powershell
python -m src.factory_vision.main "data/private/test_720p.mp4" --model "models/model.pt" --confidence 0.50
```

`--confidence` aceita valores entre `0` e `1`, inclusive, e usa `0.50` por
padrão. Valores inválidos são rejeitados antes da reprodução com uma mensagem
compreensível.

Durante a execução, pressione `Q` para encerrar. O programa também termina
normalmente ao chegar ao último frame.

## Como funciona

```text
VideoReader
    ↓
frame
    ↓
ObjectDetector (YOLO em CPU)
    ↓
lista de Detection
    ↓
draw_detections + draw_video_information
    ↓
cv2.imshow
```

`VideoReader` mantém a responsabilidade por vídeo e metadados.
`ObjectDetector` carrega o modelo uma vez e retorna estruturas simples.
`visualization.py` desenha as detecções e informações sem executar inferência.
`main.py` apenas coordena o fluxo e a interação pelo terminal.

## Como rodar os testes

```powershell
python -m pytest -v
```

Os testes usam frames e vídeos artificiais temporários. O detector e as janelas
são mockados quando necessário, portanto pytest não baixa modelos, não requer
GPU e não abre interface gráfica.

## Estrutura do projeto

```text
factory-vision/
├── data/
│   ├── README.md
│   └── private/
│       └── README.md
├── src/
│   └── factory_vision/
│       ├── __init__.py
│       ├── detector.py
│       ├── main.py
│       ├── video_reader.py
│       └── visualization.py
├── tests/
│   ├── test_detector.py
│   ├── test_main.py
│   ├── test_video_reader.py
│   └── test_visualization.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Política sobre dados privados

Não adicione ao Git vídeos reais da fábrica, imagens de funcionários,
credenciais, senhas, endereços de câmeras, informações internas ou modelos
privados. Vídeos em `data/private/` e formatos comuns de vídeo e pesos estão
protegidos pelo `.gitignore`.

Consulte também [`data/README.md`](data/README.md) e
[`data/private/README.md`](data/private/README.md).

## Limitações da v0.0.2

- não existe contagem de portas;
- não existe tracking ou linha virtual;
- não existe acesso a câmera, RTSP ou múltiplas câmeras;
- não há treinamento ou avaliação de dataset customizado;
- a velocidade depende da CPU, da resolução e do tamanho do modelo;
- a qualidade depende integralmente das classes e dos pesos fornecidos;
- modelos genéricos não garantem detecção de portas industriais.

## Roadmap

| Versão | Entrega | Status |
| --- | --- | --- |
| v0.0.1 | Pipeline de leitura de vídeo | ✅ |
| v0.0.2 | Primeira detecção | ✅ |
| v0.0.3 | Contagem de portas | Não implementado |
| v0.1.0 | Registro de eventos e métricas | Não implementado |
| v0.2.0 | Detecção de períodos de parada | Não implementado |
| v0.3.0 | Análise de tempo de ciclo | Não implementado |
| v0.5.0 | Múltiplas câmeras | Não implementado |
| v0.7.0 | Detecção de defeitos | Não implementado |
| v1.0.0 | Sistema completo | Não implementado |

As versões posteriores à v0.0.2 são apenas planejamento e não estão presentes
no código atual.

## Licença

Distribuído sob a licença MIT. Consulte [`LICENSE`](LICENSE).
