
include_recipe "apt"
include_recipe "runit"

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

# Install Ruby
# --------------------------------------------------------------

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
#rbenv_gem "atlas2ipynb" do
#  rbenv_version   "1.9.3-p545"
#  user            "vagrant"
#  action          :install
#end

# Or – preferred – add a gemfile to your project and run bundle install in the cookbook
#rbenv_script "bundle_install" do
# rbenv_version   "1.9.3-p545"
# user            "vagrant"
# cwd             "/vagrant"
# code            "bundle install"
#end

# Install Python
# --------------------------------------------------------------

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
