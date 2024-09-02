terraform {
  required_providers {
    # Provedor do VirtualBox
    virtualbox = {
      source = "terra-farm/virtualbox"
      version = "0.2.2-alpha.1"
    }
  }
}

resource "virtualbox_vm" "node" {
  count     = 4
  name      = format("node-%02d", count.index+1)
  # Alpine Linux 3.18
  image     = "https://app.vagrantup.com/generic/boxes/alpine318/versions/4.3.12/providers/virtualbox/amd64/vagrant.box"
  cpus      = 1
  memory    = "256 mib"
  user_data = file("${path.module}/user_data")

  network_adapter {
    type           = "hostonly"
    # Alterar o nome da iface de acordo com o setup de seu VirtualBox
    host_interface = "VirtualBox Host-Only Ethernet Adapter"
  }

}
