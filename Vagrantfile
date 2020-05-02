# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
 
  config.vm.define "server" do |server|
    server.vm.box = "ubuntu/xenial64"
    server.vm.hostname = "flask-rest"
    server.vm.provision "shell", path: "./scripts/general.sh"
    config.vm.provision "shell", path: "./scripts/install-docker.sh"
    config.vm.provision "shell", path: "./scripts/install-gcloud.sh"
    config.vm.network "forwarded_port", guest: 5000, host: 5000
    server.vm.provider :virtualbox do |vb|
      vb.customize [ 'modifyvm', :id, '--name', 'flask-rest' ]
      vb.customize [ 'modifyvm', :id, '--memory', '1024']
      vb.customize [ 'modifyvm', :id, '--cpus', '1' ]
    end
  end
  
end 
