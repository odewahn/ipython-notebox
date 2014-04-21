# iPython Notebook Vagrant Box

This project is a simple skeleton for easily running iPython Notebooks on your local machine.  The goal is to provide a simple way for you to:

* Install and run the iPython Notebook server and all its dependencies
* Create and save notebook files on your local machine
* Easily push and pull your notebooks to your GitHub account

The project is inspired by Matthew Russell's [Mining the Social Web, 2nd edition](https://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition).  

## Using the box

Before you start, you'll need to:

* Install [git](http://git-scm.org)
* Install [Vagrant](http://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) .  Matthew Russell's excellent [Appendix A: Virtual Machine Experience](http://nbviewer.ipython.org/github/ptwobrussell/Mining-the-Social-Web-2nd-Edition/blob/master/ipynb/_Appendix%20A%20-%20Virtual%20Machine%20Experience.ipynb) provides full details on how to get set up.  
* Install the Vagrant Omnibus plug-in:

```
vagrant plugin install vagrant-omnibus
```

Once you've got these installed, you can create the virtual machine:

* Clone this repository to your machine.  For example, you might put it in "/Users/odewahn/Desktop/ipython-notebox"
* "vagrant up" from within the directory and wait a few minutes while all the dependencies are installed

## Building a notebook from your Atlas project

Once you've got the VM installed (this is probably the hardest part), you're ready to go.  Once you get a working HTML build, can generate a notebook like this:

```
   atlas2ipynb _YOUR-ATLAS-API-TOKEN_ _YOUR-PROJECT-NAME_
```

For example:

```
   atlas2ipynb r1pB4y95uMxT3m8t9zRf oreillymedia/razzpisampler
````

Here are the steps to follow:

* Use *vagrant ssh* to log into the box
* Use *atlas2ipynb* to build, download, unzip, and convert your project.  (You'll need your API key from Atlas.)
* Assuming the build succeeds, cd into the new directory and type *nbserver*
* Open your browser and go to "http://localhost:8888"

If you want to view just your static site, you can run:

```
python -m SimpleHTTPServer
```

In the directory and then open "http://localhost:8000" in your browser.


## TODO

Here are some things we still need to figure out

### Installing additional requirements / packages on the box

It's very likely that you'll want to install some additional requirements/dependencies on the box that are specific to your project.  For example, if you're doing Python, you might want to install a bunch of things from pip.  To do this, you might put all your dependencies in a file called "requirements.txt in Atlas and then run Pip on the box to install them, like this:

```
   pip install -r requirements.txt
```

If you're using Ruby, you might make a Gemfile and then rune "bundle install". 

We'll need to figure this out as we go, so we're open to suggestions. 

## Building a docker image

This VM also installs [Packer](http://www.packer.io/) and [Docker](https://www.docker.io/) in order to create a Docker image of the VM.  This will (eventually!) let us make a much simpler process for spinning up and deploying new content repos:

* Use packer to make an ipython-notebox base docker image
* For content, use inherit from ipython-notebox and use Dockerfiles to install the content

There's still more work to do here.

To create the image:

```
sudo su - root
cd /vagrant
packer build packer-ipython-notebox-docker.json
```

After you build the image, you can run it like this:

```
cat image.tar | docker import - testimage
docker run -i -t testimage /bin/bash
```


