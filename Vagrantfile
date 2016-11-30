# -*- mode: ruby -*-
# vi: set ft=ruby :

#
# StickyAds API Vagrant setup for development
#

Vagrant.configure(2) do |config|

  puts "STARTING THE TTD API VAGRANT BOX"

  config.vm.box = "geerlingguy/ubuntu1204"
  config.vm.synced_folder ".", "/home/vagrant/ttd-api"
  config.vm.synced_folder "~/secrets", "/home/vagrant/secrets"

  # Assess system RAM and CPU cores, and provision the VM with the largest reasonable resources
  # We take half of the ram, and all but 1 of the cores
  ram_as_bytes = /(hw.memsize: )(\d*)/.match(`sysctl hw.memsize`)[2].to_i
  ram_as_megabytes = ram_as_bytes/1024/1024 #a.k.a., bytes/kilobytes/megabytes
  vm_ram = ram_as_megabytes/2
  cpu_core_count = /(hw.physicalcpu: )(\d*)/.match(`sysctl hw.physicalcpu`)[2].to_i
  vm_cpu_cores = cpu_core_count-1

  config.vm.provider "virtualbox" do |box|
    box.cpus = vm_cpu_cores
    box.memory = vm_ram
  end

  config.vm.provision "shell",
    privileged: false,
    path: "./provisioner"

end
