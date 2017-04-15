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
Navigate to your favorite directory and clone the project with:

```
git clone https://github.com/vojtatom/pandaSync
```

### Make it work on Linux and Mac
After downloading, move the new pandasync folder to the directory where you want it to live. Enter the directory and run the **install.sh** script - it'll create symlink for you, so you can run the command by simply typing **panda**.

```
cd ~/Applications/pandasync
sudo ./install.sh
```

### Make it work on Windows
After some adjustments I made the script work on Windows directly from windows Command Prompt without bash. First I encountered error connected with Crypto package. To check if your installation is the same case, just simply type
```
panda
```
and if you are greeted with
```
...
  File "C:\Program Files\Python\lib\site-packages\Crypto\Random\OSRNG\nt.py", line 28, in <module>
    import winrandom
ImportError: No module named 'winrandom'
```
then there's a simple fix to it. Navigate into Python directory with libraries, and open crypto\Random\OSRNG\nt.py and change
```
import winrandom
```
to
```
from . import winrandom
```
and you are done. To make the panda command executable as a normal console command, you will have to add the panda directory to your PATH. Open System properties, and under tab Advanced open Environment Variables. Check if you already have User variable called PATH. 
* If yes, edit it and add the path to the directory of the script where you installed the script (mine is e.g.. 'C:\Users\vojtatom\Documents\software\pandasync'). Okay twice and you should be good to go.
* If you don't have PATH in you user variables, create a new one, the variable name is PATH and the Variable value is %PATH%;path\to\the\script\folder (mine would be e.g.. '%PATH%;C:\Users\vojtatom\Documents\software\pandasync'). You should be good to go.

## How to run
After creating the symlink with **install.sh**, just simply type **panda** and you should get some sort of help message in your terminal.

```
panda
```
...and if you do, that means the script has been installed successfully! Yay, congrats!

### Functionality
You can always get a list of possibilities by typing **panda** - it'll roll out the full help screen. Currently there are four commands panda can run (replace <name> with your own local name for your account):
```
panda pull <name>   - downloads newer content of from the server
panda push <name>   - uploads content of the local
panda update        - updates pandaSync
panda reset <name>  - deletes saved credentials from the local disk
```

Your credentials and password are stored on your local drive in **.credentials** file. It's encrypted using the AES from pycrypto package. The only thing you have to remember is the **key** which is the encryption key to your locally stored file. This allows easier authentication for you next time, when you only fill your local key.

## Additional info
Contact me here, on twitter (@vojtatom) or on my mail tomas (at) vojtatom.cz. Happy coding!
