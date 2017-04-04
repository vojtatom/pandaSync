# pandaSync

Simple ftp command line client built with python and ftputil package. Tested with python 3 and newer.

## Getting started

Requirements:
* *python 3 or newer*
* *git* 
* python package *ftputil*
* python package *pycrypto*

The simplest way to install the script is to clone it from git. The required packages for the script to run correctly are **ftputil** and **pycrypto**. If you don't have them installed, you can add them with pip (if you have pip installed...).

```
pip install pycrypto
pip install ftputil
```

For cloning and updating the repository, the git installation is required. If you don't have have it, please install it from [this website](https://git-scm.com/downloads).
### How to install
Navigate to your favourite directory and clone the project with:

```
git clone https://github.com/vojtatom/pandaSync
```

After downloading, move the new pandasync folder to the directory where you want it to live. Enter the directory and run the **install.sh** script - it'll create symlink for you, so you can run the command by simply typing **panda**.

```
cd ~/Applications/pandasync
sudo ./install.sh
```

### How to run
After creating the symlink with **install.sh**, just simply type **panda** and you should get some sort of help message in your terminal.

```
panda
```
...and if you do, that means the script has ben installed successfully! Yay, congrats!

## Functionality
You can always get a list of possibilities by typing **panda** - it'll roll out the full help screen. Currently there are four commands panda can run (replace <name> with your own local name for your account):
```
panda pull <name>   - downloads newer content of from the server
panda push <name>   - uploads content of the local
panda update        - updates pandaSync
panda reset <name>  - deletes saved credentials from the local disk
```

Your credentials and password are stored on your local drive in **.credentials** file. It's encrypted using the AES from pycrypto package. The only thing you have to remeber is the **key** which is the encryption key to your locally stored file. This allows easier authentication for you next time, when you only fill your local key.

## Additional info
If you are experiencing any issues feel free to contact me anyhere you find me - here, on twitter (@vojtatom) or on my mail tomas (at) vojtatom.cz. Happy coding!
