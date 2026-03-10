# Estrategia de Branches para Producao, Homologacao e Desenvolvimento

## Objetivo
Permitir que a producao atual continue em `main` no GitHub enquanto a nova plataforma evolui em paralelo, sem risco de publicar o ambiente local por engano.

## Estrutura Recomendada
- `main`: producao atual publicada no GitHub.
- `homolog`: branch de homologacao publica para o novo ambiente.
- `develop`: branch de desenvolvimento local e integracao continua da nova plataforma.

## Regras Operacionais
- Nao desenvolver diretamente em `main`.
- Nao publicar `develop` sem autorizacao explicita.
- Publicar para homologacao somente a partir de `homolog`.
- Promover para `main` apenas o que estiver aprovado em homologacao.

## Estado Local Preparado
- `main`: recriada localmente apontando para `origin/main`.
- `develop`: contem o trabalho atual da nova plataforma e esta sem upstream configurado.
- `homolog`: criada localmente como branch separada para futura publicacao controlada.

## Fluxo Recomendado
1. Continuar o desenvolvimento local em `develop`.
2. Quando houver autorizacao para publicar a homologacao:
   - revisar os commits de `develop`
   - promover apenas os commits aprovados para `homolog`
   - publicar `homolog` no GitHub
3. Depois da validacao do ambiente publico de homologacao:
   - promover `homolog` para `main`

## Comandos Uteis
Ver branch atual:

```bash
git branch --show-current
```

Trocar para producao local:

```bash
git checkout main
```

Voltar para desenvolvimento:

```bash
git checkout develop
```

Criar a branch remota de homologacao quando houver autorizacao:

```bash
git push -u origin homolog
```

Publicar desenvolvimento somente com autorizacao explicita:

```bash
git push -u origin develop
```

## Observacao Importante
Enquanto `develop` permanecer sem upstream, comandos como `git push` simples nao devem publicar esse branch por acidente. Isso reduz o risco operacional, mas nao substitui revisao humana antes de qualquer push.
