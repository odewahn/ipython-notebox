# iPython Notebook Vagrant Box

This project is a simple skeleton for easily running iPython Notebooks on your local machine.  The goal is to provide a simple way for you to:

* Install and run the iPython Notebook server and all its dependencies
* Create and save notebook files on your local machine
* Easily push and pull your notebooks to your GitHub account

The project is inspired by Matthew Russell's [Mining the Social Web, 2nd edition](https://github.com/ptwobrussell/Mining-the-Social-Web-2nd-Edition).  

## Using the box

Before you start, you'll need to install [Vagrant](http://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) .  Matthew Russell's excellent [Appendix A: Virtual Machine Experience](http://nbviewer.ipython.org/github/ptwobrussell/Mining-the-Social-Web-2nd-Edition/blob/master/ipynb/_Appendix%20A%20-%20Virtual%20Machine%20Experience.ipynb) provides full details on how to get set up.  

Once you've got these installed, first create the virtual machine:

* Clone this repository to your machine.  For example, you might put it in "/Users/odewahn/Desktop/ipython-notebook-box"
* "vagrant up" from within the directory and wait a few minutes while all the dependencies are installed

Then, you're ready to run some notebooks.  For example, say you want to try out these great [Scientific Python Lectures](https://github.com/jrjohansson/scientific-python-lectures).  

* Clone the lecture repo to "/Users/odewahn/Desktop/scientific-python-lectures"
* CD to "/Users/odewahn/Desktop/ipython-notebook-box"
* "vagrant ssh" to login to the box
* From within the box, type "cd /host/<directory with ipynb files>".  The "/host" directory on the VM maps to the parent directory of where you downloaded the  ipython-notebook-box repo.  So, if you cloned this notebook into "/Users/odewahn/Desktop/ipython-notebook-box", the "/host" on the VM will map to "/Users/odewahn/Desktop/"
* Type "nbserver", which is an alias to starts the ipython notebook server.
* Open your browser and go to "http://localhost:8888"









Run the command *nbserver* in the "/host/<your ipynb files>" directory.  (*nbserver* 




## Installing additional requirements / packages on the box

If you need to install additional packags
To install any additional requirements

   pip install -r requirements.txt