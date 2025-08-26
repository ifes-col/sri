# Lab 03 - Criar uma VM na AWS com Terraform

Objetivo: usar o provider `aws` do Terraform para criar uma única instância EC2 (Ubuntu) com um `user_data` que instala e inicia `nginx`.

Arquivos criados em `lab-03`:

- `main.tf` - recursos principais (provider, key_pair, security_group, instance)
- `variables.tf` - variáveis utilizadas
- `outputs.tf` - outputs da instância
- `user_data` - script de inicialização para instalar nginx

Pré-requisitos
- Conta AWS com credenciais configuradas (usando AWS CLI ou variáveis de ambiente `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY`).
- Terraform >= 1.3.0 instalado.
- Chave SSH pública disponível (padrão `~/.ssh/id_rsa.pub`).

Passos para executar

1. Ajuste a AMI se necessário
   - A AMI padrão em `variables.tf` é um exemplo para `us-east-1`. Substitua por uma AMI Ubuntu recente para sua região. Você pode encontrar a AMI com o comando:

```powershell
# exemplo para procurar AMIs Ubuntu (requer AWS CLI configurado)
aws ec2 describe-images --owners 099720109477 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" --query 'Images[*].[ImageId,Name]' --output text | sort
```

2. Inicializar Terraform

```powershell
cd lab-03
terraform init
```

3. Verificar plano

```powershell
terraform plan -out plan.tfplan
```

4. Aplicar (criar infraestrutura)

```powershell
terraform apply "plan.tfplan"
```

5. Acessar a aplicação
- Após o `apply`, verifique o output `instance_public_ip` ou `instance_public_dns`.
- Acesse `http://<instance_public_ip>` no seu navegador para ver a página servida pelo nginx.

6. Limpar recursos

```powershell
terraform destroy -auto-approve
```

Notas e segurança
- A variável `ssh_cidr` está por padrão em `0.0.0.0/0` — para produção troque para seu IP ou rede.
- O `public_key_path` usa `~/.ssh/id_rsa.pub` por padrão; altere se usar outro par de chaves.
- A chave pública será importada como `aws_key_pair`. Se preferir não importar, forneça `key_name` já existente e comente o recurso `aws_key_pair`.

Solução de problemas
- Erro de AMI: atualize `var.ami` para uma AMI válida na sua região.

Credenciais (detalhado)
-----------------------
- O arquivo `~/.aws/credentials` NÃO é obrigatório para o Terraform funcionar, mas é uma das formas mais convenientes de fornecer credenciais.

- Formas válidas de fornecer credenciais ao provider `aws` do Terraform (ordem comum de busca):
  1. Variáveis de ambiente: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e opcionalmente `AWS_SESSION_TOKEN`.
  2. Perfil no arquivo `~/.aws/credentials` (usado com `AWS_PROFILE` ou por padrão). Ex.: `~/.aws/credentials` e `~/.aws/config`.
  3. Credenciais fornecidas pelo ambiente (ex.: EC2 instance role, ECS task role, ou qualquer metadata service ou provider externo configurado via `credential_process`).
  4. Passadas diretamente no bloco `provider` do Terraform (não recomendado para commits e uso colaborativo).

Exemplos PowerShell
-------------------
1) Definir variáveis de ambiente temporariamente na sessão PowerShell (válido apenas para a sessão atual):

```powershell
$env:AWS_ACCESS_KEY_ID = 'AKIA...'
$env:AWS_SECRET_ACCESS_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCY...'
# opcional (para sessões temporárias):
$env:AWS_SESSION_TOKEN = '...'
```

2) Usar um profile já configurado (o Terraform respeita `AWS_PROFILE`):

```powershell
$env:AWS_PROFILE = 'my-profile'
```

3) Criar/atualizar `~/.aws/credentials` usando o AWS CLI (se instalado):

```powershell
# instalar AWS CLI via winget (opcional)
# winget install --id Amazon.AWSCLI -e

# depois de instalado, rode interativamente:
# aws configure
```

## Helper: criar credenciais sem instalar o AWS CLI
Se você não pode instalar o AWS CLI por políticas do AD, use o helper PowerShell incluído: `create-aws-credentials.ps1`.

O que o script faz
- Interativamente cria/atualiza `%USERPROFILE%\.aws\credentials` com o profile informado.
- Opcionalmente escreve também `%USERPROFILE%\.aws\config` para definir `region` para o profile.
- Não transmite suas chaves para lugar nenhum — escreve apenas no disco local do usuário.

Como usar
1. Abra PowerShell (não precisa de privilégios de administrador, apenas permissões para escrever em `%USERPROFILE%`).
2. Navegue para o diretório do lab:

```powershell
cd %USERPROFILE%\sri\lab-03
```

3. Execute o script (exemplo):

```powershell
# Use o profile 'default'
.\create-aws-credentials.ps1 -ProfileName default -SetRegion

# Ou apenas executar e fornecer nome de profile quando solicitado
.\create-aws-credentials.ps1
```

4. Depois de criar o profile, você pode usar o Terraform normalmente. Para usar um profile específico na sessão atual:

```powershell
$env:AWS_PROFILE = 'nome-do-profile'
terraform init
terraform apply
```

Avisos de segurança
- Evite compartilhar ou versionar o arquivo `~/.aws/credentials` ou `%USERPROFILE%\.aws\credentials`.
- Exclua entradas antigas se não forem mais necessárias.

Boas práticas de segurança
-------------------------
- Nunca versionar chaves (não coloque `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` em arquivos de código ou `variables.tf`).
- Prefira perfis em `~/.aws/credentials` (Linux/macOS), `%USERPROFILE%\.aws\credentials` (Windows) ou roles temporárias/roles do serviço.
- Restrinja `ssh_cidr` ao seu IP em vez de `0.0.0.0/0`.