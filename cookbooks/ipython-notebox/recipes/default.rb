
include_recipe "apt"
include_recipe "runit"

dependencies = [
  "libfreetype6-dev", 
  "libpng-dev",           # Matplotlib dependencies
  "libncurses5-dev",
  "vim", 
  "git-core",
  "build-essential",
  "curl",
  "unzip"
]

dependencies.each do |pkg|
  package pkg do
    action :install
  end
end

#******************************************************************************************
# Install Ruby
#******************************************************************************************

include_recipe "ruby_build"
include_recipe "rbenv::user"
include_recipe "rbenv::vagrant"

rbenv_gem "bundler" do
  rbenv_version   "1.9.3-p545"
  user            "vagrant"
  version         "1.3.5"
  action          :install
end

# You can either install your custom gem like this:
rbenv_gem "atlas2ipynb" do
  rbenv_version   "1.9.3-p545"
  user            "vagrant"
  action          :install
end


# You can either install your custom gem like this:
rbenv_gem "atlas-api" do
  rbenv_version   "1.9.3-p545"
  user            "vagrant"
  action          :install
end


#******************************************************************************************
# Install Python
#******************************************************************************************

include_recipe "python"

packages = [
  # Matplotlib won't install any other way right now unless you install numpy first.
  # http://stackoverflow.com/q/11797688
  "numpy==1.7.1",
]

packages.each do |package|
  python_pip package do
    action :install
  end
end

execute "install_requirements" do
  command "pip install -r /vagrant/requirements.txt --allow-unverified matplotlib --allow-all-external"
  # action :nothing
end

cookbook_file '/home/vagrant/.bash_profile' do
   source "bash_profile"
   owner 'vagrant'
   group 'vagrant'
   mode '0644'
end

#******************************************************************************************
#  Set up docker
#******************************************************************************************
execute "install_docker" do
  command "curl -s https://get.docker.io/ubuntu/ | sudo sh"
  not_if "dpkg --get-selections | grep -v deinstall | grep lxc-docker-0.10.0"
end

#******************************************************************************************
#  Set up packer
#******************************************************************************************
execute "install_packer" do
  cwd "/usr/local/bin"
  command "wget https://dl.bintray.com/mitchellh/packer/0.5.2_linux_386.zip; unzip 0.5.2_linux_386.zip"
end  


