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
  count     = 1
  name      = format("node-%02d", count.index+1)
  # Alpine Linux 3.8
  image     = "https://app.vagrantup.com/generic/boxes/alpine38/versions/4.2.16/providers/virtualbox.box"
  cpus      = 1
  memory    = "256 mib"
  user_data = file("${path.module}/user_data")

  network_adapter {
    type           = "hostonly"
    host_interface = "VirtualBox Host-Only Ethernet Adapter"
  }
}