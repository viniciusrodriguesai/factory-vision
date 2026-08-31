# Factory Vision

Factory Vision é um projeto de visão computacional voltado à evolução do
monitoramento de uma fábrica de portas. Seu objetivo geral é criar, de forma
incremental, uma base confiável para futuramente contar portas, medir o fluxo de
produção, identificar paradas, analisar tempos de ciclo e detectar defeitos.

## Status atual

**v0.0.1 — Pipeline de leitura de vídeo**

Esta versão implementa somente a fundação para processar arquivos de vídeo
locais. Detecção, contagem, métricas industriais e integrações com câmeras ainda
não foram implementadas.

## Funcionalidades atuais

- validação do caminho informado pelo terminal;
- abertura de arquivos de vídeo com OpenCV;
- leitura sequencial frame a frame;
- exibição do número do frame, FPS informado pelo arquivo e resolução;
- encerramento ao final do vídeo ou ao pressionar `Q`;
- liberação segura da captura e fechamento das janelas;
- mensagens claras para caminho vazio, arquivo inexistente e vídeo inválido;
- testes automatizados com vídeo artificial temporário.

## Tecnologias utilizadas

- Python 3;
- OpenCV;
- pytest.

## Requisitos

- Python 3.10 ou superior;
- terminal do Windows PowerShell;
- sessão gráfica disponível para a janela de reprodução;
- codec compatível com o arquivo de vídeo instalado no sistema.

## Instalação no Windows

Clone o repositório e acesse sua pasta. Em seguida, crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Se a política de execução do PowerShell bloquear a ativação, libere scripts
locais apenas para a sessão atual e tente novamente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Como executar

Com o ambiente virtual ativado, informe o caminho de um vídeo local:

```powershell
python -m src.factory_vision.main "C:\caminho\para\video.mp4"
```

Durante a reprodução, pressione `Q` para encerrar. O programa também termina
normalmente quando chega ao último frame.

Não use vídeos reais ou sensíveis da fábrica em exemplos públicos.

## Como rodar os testes

Com o ambiente virtual ativado, execute:

```powershell
python -m pytest -q
```

Os testes criam um vídeo artificial em uma pasta temporária e não abrem janelas
gráficas.

## Estrutura do projeto

```text
factory-vision/
├── data/
│   └── README.md
├── src/
│   └── factory_vision/
│       ├── __init__.py
│       ├── main.py
│       └── video_reader.py
├── tests/
│   └── test_video_reader.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

`VideoReader` concentra o ciclo de vida da captura e a leitura dos metadados. O
módulo `main` cuida apenas da interface de terminal, da apresentação dos frames
e da interação com o usuário. Essa separação mantém a base simples e testável.

## Política sobre dados privados

Este repositório não deve conter vídeos reais da fábrica, fotos de funcionários,
credenciais, senhas, endereços de câmeras nem dados internos da empresa. Os
formatos comuns de vídeo e os diretórios `data/private/`, `credentials/` e
`secrets/` estão protegidos pelo `.gitignore`.

Consulte também [`data/README.md`](data/README.md). Para testes, utilize somente
material artificial, público e devidamente licenciado ou anonimizado.

## Roadmap

| Versão | Entrega | Status |
| --- | --- | --- |
| v0.0.1 | Pipeline de leitura de vídeo | Implementado |
| v0.0.2 | Primeira detecção de portas | Não implementado |
| v0.0.3 | Contagem de portas | Não implementado |
| v0.1.0 | Registro de eventos e métricas | Não implementado |
| v0.2.0 | Detecção de períodos de parada | Não implementado |
| v0.3.0 | Análise de tempo de ciclo | Não implementado |
| v0.5.0 | Suporte a múltiplas câmeras | Não implementado |
| v0.7.0 | Detecção de defeitos | Não implementado |
| v1.0.0 | Sistema operacional completo | Não implementado |

Todas as versões posteriores à v0.0.1 são apenas planejamento. Nenhuma dessas
funcionalidades futuras está presente no código atual.

## Licença

Distribuído sob a licença MIT. Consulte [`LICENSE`](LICENSE).
