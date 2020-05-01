# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
 
  config.vm.define "server" do |server|
    server.vm.box = "ubuntu/xenial32"
    server.vm.hostname = "web-services"
    #server.vm.provision "shell", path: "general.sh"
    server.vm.provision "file", source: "main.py", destination: "$HOME/main.py"
    #vagraserver.vm.synced_folder "./shared", "/home/vagrant/shared",owner: "nobody", group: "nogroup"
    server.vm.network "forwarded_port", guest: 80 , host: 8888 , protocol: "tcp"
    server.vm.provider :virtualbox do |vb|
      vb.customize [ 'modifyvm', :id, '--name', 'web-services' ]
      vb.customize [ 'modifyvm', :id, '--memory', '1024']
      vb.customize [ 'modifyvm', :id, '--cpus', '1' ]
    end
  end
  
end 
