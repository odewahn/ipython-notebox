# -*- mode: ruby -*-
# vi: set ft=ruby :

###########################################################################
# This configuration file is the starting point for understanding how the
# virtual machine is configured and provides a default provider that uses
# Virtualbox to provide virtualization. It also contains an *experimental*
# provider for using an AWS EC2 microinstance in the cloud. The AWS provider
# works but is a bit bleeding edge and incomplete from the standpoint of
# providing all of the functionality that it should at this time, so it should
# only be used by hackers who are comfortable working in the cloud. After 
# filling in the necessary AWS credentials below use the --provider=aws
# option to use the AWS provider. See https://github.com/mitchellh/vagrant-aws 
# for more details.
#
# See http://docs.vagrantup.com/v2/vagrantfile/index.html for additional 
# details on Vagrantfile configuration in general.
###########################################################################

Vagrant.configure("2") do |config|

  # SSH forwarding: See https://help.github.com/articles/using-ssh-agent-forwarding
  config.ssh.forward_agent = true

  config.omnibus.chef_version = "11.4.4"

  #########################################################################
  # Virtualbox configuration - the default provider for running a local VM
  #########################################################################
  
  config.vm.provider :virtualbox do |vb, override|

    # The Virtualbox image
    override.vm.box = "precise64"
    override.vm.box_url = "http://files.vagrantup.com/precise64.box"

    # Port forwarding details
  
    # IPython Notebook
    override.vm.network :forwarded_port, host: 8888, guest: 8888
    override.vm.network :forwarded_port, host: 8000, guest: 8000

    config.vm.synced_folder ".", "/vagrant"
    
    # You can increase the default amount of memory used by your VM by
    # adjusting this value below (in MB) and reprovisioning.
    vb.customize ["modifyvm", :id, "--memory", "384"]
  end
 
  #########################################################################
  # AWS configuration - an experimental provider for running this VM in the
  # cloud. See https://github.com/mitchellh/vagrant-aws for configuration
  # details. User specific values for your own environment are referenced
  # here as MTSW_ environment variables that you could set (or hard code.)
  #########################################################################
  

  # Chef-Solo provisioning
  config.vm.provision :chef_solo do |chef|
    chef.log_level = :debug
    chef.cookbooks_path = "cookbooks"
    chef.json = {
      :answer => "42",
      'rbenv' => {
        'user_installs' => [
          {
            'user' => 'vagrant',
            'rubies' => [ "1.9.3-p545" ],
            'global' => '1.9.3-p545'
          }
        ]
      }
    }
    chef.run_list = [
      "recipe[ipython-notebox::default]"
    ]
  end

end
