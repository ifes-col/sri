# Serviços de Redes para a Internet (SRI)

## Introdução

Os serviços de redes para a Internet são essenciais para garantir a comunicação, compartilhamento de recursos e acesso à informação entre dispositivos conectados à rede mundial. Neste repositório, abordaremos alguns dos principais serviços utilizados nesse contexto.

## Dynamic Host Configuration Protocol (DHCP)

O DHCP é um serviço que automatiza a atribuição de endereços IP e outras configurações de rede para dispositivos conectados a uma rede local. Em vez de configurar manualmente cada dispositivo, o DHCP permite que os dispositivos solicitem e recebam automaticamente um endereço IP disponível na rede, bem como outras informações, como o gateway padrão e o servidor DNS.

O DHCP é especialmente útil em redes domésticas e empresariais, onde há uma grande quantidade de dispositivos conectados, tornando o processo de gerenciamento de IP mais eficiente e menos propenso a erros.

## Domain Name System (DNS)

O Sistema de Nomes de Domínio, conhecido como DNS, é responsável por traduzir os nomes de domínio (exemplo.com) em endereços IP numéricos. Isso facilita a navegação na Internet, pois é mais fácil lembrar nomes de domínio do que sequências de números.

## Secure Shell (SSH)

O SSH é um serviço de rede que oferece uma forma segura de acesso remoto a servidores e dispositivos. Ele utiliza criptografia para proteger as informações transmitidas, tornando-o uma opção segura para administrar sistemas à distância.

## Proxy

Um proxy é um servidor intermediário que atua como um intermediário entre os clientes (usuários) e os servidores na Internet. Ele recebe as solicitações dos clientes e, em seguida, repassa essas solicitações para os servidores, atuando como um escudo para os clientes. Os servidores, por sua vez, enviam as respostas para o proxy, que encaminha essas respostas de volta aos clientes.

### Modelos de Proxy

Existem diferentes modelos de proxy, cada um com seu propósito específico:

1. **Proxy Reverso (Reverse Proxy):** O proxy reverso é colocado na frente dos servidores web e atua como um representante dos servidores para os clientes. Ele recebe as solicitações dos clientes e encaminha para o servidor apropriado. Isso é especialmente útil quando há um balanceamento de carga entre vários servidores, ajudando a melhorar a escalabilidade e a disponibilidade do serviço.

2. **Proxy Aberto (Open Proxy):** É um proxy que pode ser acessado por qualquer cliente da Internet. Esse tipo de proxy pode ser usado para contornar restrições de firewall ou acessar conteúdo bloqueado geograficamente. No entanto, muitos proxies abertos são inseguros e podem ser utilizados para atividades maliciosas.

3. **Proxy Transparente:** Esse tipo de proxy não exige que o cliente faça qualquer configuração específica, já que ele é automaticamente redirecionado para o proxy. Geralmente, é usado para fins de monitoramento ou filtragem de conteúdo em redes corporativas.

4. **Proxy de Cache:** O proxy de cache armazena cópias locais de recursos frequentemente solicitados pelos clientes. Quando um cliente solicita esses recursos, o proxy de cache os entrega diretamente, economizando tempo e largura de banda, pois não é necessário acessar o servidor original.

5. **Proxy de Aplicação (Application Proxy):** Atua como intermediário para solicitações de aplicativos específicos, geralmente oferecendo recursos avançados de segurança, autenticação e controle de acesso.

## World Wide Web (WWW)

A World Wide Web é um serviço que permite o acesso a páginas e recursos na Internet por meio de navegadores web. Ela utiliza o protocolo HTTP (Hypertext Transfer Protocol) para transferir informações entre o cliente (usuário) e o servidor (onde o conteúdo está hospedado).
