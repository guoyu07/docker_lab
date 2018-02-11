# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "dockerLab" do |dockerLab|
      dockerLab.vm.box = "ubuntu/xenial64"
      # set up network ip and port forwarding
      dockerLab.vm.network "forwarded_port", guest: 8089, host: 8089, host_ip: "127.0.0.1"
      dockerLab.vm.synced_folder "./", "/vagrant", owner: "ubuntu", mount_options: ["dmode=755,fmode=644"]
      dockerLab.vm.provider "virtualbox" do |vb|
        # Customize the amount of memory on the VM:
        vb.memory = "4096"
        vb.cpus = 4
      end
  end

  config.vm.provision :docker_compose
  config.vm.provision :docker

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y git python-pip python-dev build-essential
    pip install --upgrade pip
    apt-get -y autoremove
    pip install locustio
  SHELL

end
