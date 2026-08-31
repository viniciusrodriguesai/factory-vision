# Vídeos privados para testes manuais

Coloque manualmente nesta pasta os vídeos locais que serão usados para testar a
reprodução e a primeira detecção da versão v0.0.2 do Factory Vision. Nenhum
vídeo é fornecido pelo projeto, e os arquivos adicionados aqui não devem ser
enviados ao GitHub.

Sugestão de nomes:

```text
test_360p.mp4
test_720p.mp4
test_1080p.mp4
```

Esses vídeos servem para conferir manualmente a leitura preservada da v0.0.1 e a
camada de detecção da v0.0.2. Eles não são usados para contagem, tracking ou
qualquer outra funcionalidade futura.

## Como executar

A partir da raiz do repositório, com o ambiente virtual ativado, execute o vídeo
que deseja verificar:

```powershell
python -m src.factory_vision.main "data/private/test_360p.mp4" --model "models/model.pt" --confidence 0.50
```

```powershell
python -m src.factory_vision.main "data/private/test_720p.mp4" --model "models/model.pt" --confidence 0.50
```

```powershell
python -m src.factory_vision.main "data/private/test_1080p.mp4" --model "models/model.pt" --confidence 0.50
```

## Checklist para cada vídeo

- o vídeo abre corretamente;
- os frames são exibidos;
- o número do frame aumenta durante a reprodução;
- o FPS é exibido;
- a resolução exibida corresponde ao vídeo;
- as detecções retornadas pelo modelo exibem bounding box, classe e confiança;
- pressionar `Q` encerra o programa sem erro.

O arquivo informado em `--model` deve existir localmente. Um modelo genérico
pode demonstrar o pipeline, mas não garante detecção correta de portas
industriais.

## Privacidade

Não use vídeos que revelem funcionários, credenciais, senhas, endereços de
câmeras ou outros dados internos sem a autorização e a proteção adequadas. O
`.gitignore` mantém o conteúdo desta pasta fora do Git, com exceção deste README.
