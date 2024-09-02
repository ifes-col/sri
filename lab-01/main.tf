# Provedor do VirtualBox
terraform {
  required_providers {
    virtualbox = {
      source = "terra-farm/virtualbox"
      version = "0.2.2-alpha.1"
    }
  }
}

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
    # Alterar o nome da iface de acordo com o setup de seu VirtualBox
    host_interface = "VirtualBox Host-Only Ethernet Adapter"
  }
}
