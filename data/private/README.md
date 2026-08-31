# Vídeos privados para testes manuais

Coloque manualmente nesta pasta os vídeos locais que serão usados para testar a
reprodução da versão v0.0.1 do Factory Vision. Nenhum vídeo é fornecido pelo
projeto, e os arquivos adicionados aqui não devem ser enviados ao GitHub.

Sugestão de nomes:

```text
test_360p.mp4
test_720p.mp4
test_1080p.mp4
```

Esses vídeos servem apenas para conferir manualmente o pipeline de leitura de
arquivos da v0.0.1. Eles não serão usados para detecção, contagem ou qualquer
outra funcionalidade futura.

## Como executar

A partir da raiz do repositório, com o ambiente virtual ativado, execute o vídeo
que deseja verificar:

```powershell
python -m src.factory_vision.main data/private/test_360p.mp4
```

```powershell
python -m src.factory_vision.main data/private/test_720p.mp4
```

```powershell
python -m src.factory_vision.main data/private/test_1080p.mp4
```

## Checklist para cada vídeo

- o vídeo abre corretamente;
- os frames são exibidos;
- o número do frame aumenta durante a reprodução;
- o FPS é exibido;
- a resolução exibida corresponde ao vídeo;
- pressionar `Q` encerra o programa sem erro.

## Privacidade

Não use vídeos que revelem funcionários, credenciais, senhas, endereços de
câmeras ou outros dados internos sem a autorização e a proteção adequadas. O
`.gitignore` mantém o conteúdo desta pasta fora do Git, com exceção deste README.
