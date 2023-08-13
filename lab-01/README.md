# Laboratório de Preparação de Ambiente Virtualizado com Terraform e VirtualBox

Bem-vindo ao laboratório de preparação de ambiente virtualizado com Terraform e VirtualBox! Neste laboratório, você aprenderá como criar um ambiente de infraestrutura virtual utilizando o Terraform com o provedor do VirtualBox. O ambiente virtualizado será composto por máquinas virtuais e redes locais.

## Objetivo do Laboratório

O objetivo deste laboratório é capacitar os alunos a configurar um ambiente de infraestrutura virtual local de forma automatizada, utilizando o Terraform em conjunto com o provedor do VirtualBox.

## Pré-requisitos

Antes de iniciar o laboratório, certifique-se de que você tenha as seguintes ferramentas e conhecimentos:

1. Conhecimento básico de linha de comando e conceitos de infraestrutura de TI.
2. O VirtualBox instalado em seu ambiente local. Você pode encontrar informações sobre como instalar o VirtualBox na documentação oficial: [VirtualBox - Downloads](https://www.virtualbox.org/wiki/Downloads).
3. Terraform instalado e configurado em seu ambiente local. Você pode encontrar informações sobre como instalar o Terraform na documentação oficial: [Install Terraform](https://developer.hashicorp.com/terraform/downloads).

## Configurando o Ambiente

Antes de iniciar o laboratório, certifique-se de ter o VirtualBox instalado corretamente e o Terraform configurado em seu ambiente. Em seguida, siga os passos abaixo para configurar o ambiente local:

1. Clone este repositório em seu ambiente local utilizando o seguinte comando:

```cmd
git clone https://github.com/ifes-col/sri.git
```

2. Acesse o diretório do laboratório:
```cmd
cd sri/lab-01
```
## Executando o Terraform com o VirtualBox

Após configurar o ambiente, você pode iniciar o Terraform e criar o ambiente virtualizado local com o VirtualBox com os seguintes passos:

1. Corrigindo o caminho (path) do executável do VirtualBox e do Terraform, para que possam ser executados a partir de qualquer diretório:

Usando Windows PowerShell ou Terminal Preview:
```cmd
$env:PATH = $env:PATH + ";C:\Program Files\Oracle\VirtualBox;<caminho_de_instalacao_do_terraform>;"
```

Usando o prompt de comando (CMD):
```cmd
set PATH = %PATH%;C:\Program Files\Oracle\VirtualBox;<caminho_de_instalacao_do_terraform>;
```

> **Note**
> Você deve substituir '<caminho_de_instalacao_do_terraform>' pelo caminho completo onde o executável do Terraform foi extraído/instalado.

2. Inicialize o Terraform para baixar os plugins necessários:

```cmd
terraform init
```

3. Visualize as alterações que serão realizadas no ambiente antes de aplicá-las:

```cmd
terraform plan
```

4. Crie as máquinas virtuais e recursos locais especificados no arquivo de configuração do Terraform:
```cmd
terraform apply
```

Ao final do processo, você terá um ambiente virtualizado configurado conforme as especificações do arquivo `main.tf`, utilizando o VirtualBox como provedor. 

Para acessar a máquina virtual recém criada, basta utilizar as seguintes credenciais:
```cmd
login: vagrant
password: vagrant
```

## Limpando o Ambiente

Lembre-se de que as máquinas virtuais criadas localmente podem ocupar recursos do seu sistema. Após concluir o laboratório, lembre-se de desligar e destruir as máquinas virtuais e recursos criados para liberar os recursos do sistema:

```cmd
terraform destroy
```

## Dissecando o Arquivo de Infraestrutura (main.tf)

Este arquivo fornece uma visão geral da estrutura básica de um arquivo de configuração de infraestrutura do Terraform. Ele é usado para definir, configurar e gerenciar recursos de infraestrutura de maneira declarativa.

### Cabeçalho

O cabeçalho do arquivo geralmente contém informações sobre a versão do Terraform e outras configurações globais:

```js
terraform {
  required_version = ">= 0.13"  # Versão mínima do Terraform necessária
  # Outras configurações globais podem ser definidas aqui
}
```

### Provedor

Em seguida, especificamos o provedor de infraestrutura que será utilizado, como AWS, Azure, Google Cloud, virtualbox etc. Isso define como o Terraform se conectará ao ambiente de destino:

```js
# Provedor do VirtualBox
...
  required_providers {
    virtualbox = {
      source = "terra-farm/virtualbox"
      version = "0.2.2-alpha.1"
    }
  }
...
```

### Recursos

Os recursos representam os componentes de infraestrutura que você deseja criar e gerenciar. Eles podem ser instâncias de máquinas virtuais, bancos de dados, redes, entre outros. Baseado no exemplo do laboratório, segue um exemplo de definição de recurso:

```js
...
resource "virtualbox_vm" "node" {
  count     = 1
  name      = format("node-%02d", count.index+1)
  # Ubuntu 20.04 box
  image     = "https://app.vagrantup.com/ubuntu/boxes/focal64/versions/20230803.0.0/providers/virtualbox.box"
  cpus      = 1
  memory    = "1024 mib"
  user_data = file("${path.module}/user_data")

  network_adapter {
    type           = "hostonly"
    host_interface = "VirtualBox Host-Only Ethernet Adapter"
  }
...
```