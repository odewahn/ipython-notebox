
include_recipe "apt"
include_recipe "runit"
include_recipe "python"


dependencies = [
  "libfreetype6-dev", 
  "libpng-dev",           # Matplotlib dependencies
  "libncurses5-dev",
  "vim", 
  "git-core",
  "build-essential",
  "curl"
]

dependencies.each do |pkg|
  package pkg do
    action :install
  end
end


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
