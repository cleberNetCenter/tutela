# Clone da VM para Migracao (VMware)

## Objetivo
Criar um ambiente seguro de migracao e testes sem impactar a VM de producao.

## Procedimento Recomendado
1. Confirmar janela de manutencao.
2. Realizar backup/snapshot da VM atual.
3. **Desligar a VM atual** para garantir consistencia de disco.
4. No VMware, selecionar a VM de producao e iniciar processo de clone.
5. Escolher tipo de clone: **Full Clone**.
6. Nomear nova VM como: **`tutela-dev`**.

## Configuracao Sugerida da VM Clone
- CPU: **2 vCPU**
- RAM: **4 GB**
- Disco: **40 GB**

## Pos-Clone (obrigatorio)
Ao iniciar a `tutela-dev`, alterar:

1. **Hostname**
   - Exemplo: `tutela-dev`
2. **Endereco IP**
   - Definir novo IP para evitar conflito com producao
3. Atualizar inventario de infraestrutura (CMDB/planilha interna)
4. Validar acesso SSH e regras do Fortinet para ambiente de desenvolvimento

## Validacoes Minimas
- `hostnamectl` reflete novo hostname.
- `ip a` mostra IP exclusivo.
- Nginx inicia corretamente na clone.
- Aplicacao responde em rede interna de desenvolvimento.
