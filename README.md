## Item Catalog

In this project, I develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

Here is the steps to run the program:

1. You should first install **Vagrant** and **VirtualBox**.
2. Under the root directory of the project, type in `vagrant up` to start and provision the vagrant environment.
3. Type in the command `vagrant ssh` to connect to the virtual machine via SSH.
4. In the VM command line, type in `cd /vagrant/catalog` to enter the project diretcory on the VM.
5. Make sure that there is no database file named _catalog.db_ in the folder. You can delete it by `rm -f catalog.db` if it exists.
6. Run `python database_setup.py` to set up a database.
7. Run `python database_init.py` to create some initialzed data in the database.
8. Run `python app.py` to start the server.
9. Go to **http://localhost:8000/catalog/** from your favorite browser on the local machine to play with the application.

You won't be able to post, edit and delete catagories and items until you log in with **Google+** account.

To stop the VM, following these steps:

1. Type in `exit` in VM command line to exit the virtual machine.
2. Run `vagrant halt` to stop the vagrant machine.