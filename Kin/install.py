#------------------------------------------------------------------
# Code written by Idris DULAU, Rodin DUHAYON and Guillaume DUBRASQUET-DUVAL.
# For the use of Dr. Marie Beurton-Aimar and Phd. student Kévin Réby.
#------------------------------------------------------------------

import sys
import subprocess

tmp = 1
while(tmp):
    yn = input("Proceed to install the libraries ? (y/n) : ")

    if(yn == 'N' or yn == 'n'):
        print('Quit installing')
        sys.exit()

    if(yn == 'Y' or yn == 'y'):
        tmp = 0

    if tmp != 0:
        print("write either y or n")

#Proceeds installations
print("\n Installing tdqm :\n")
list_files = subprocess.run(["pip3", "install", "tdqm"])

print("\n Installing sacred :\n")
list_files = subprocess.run(["pip3", "install", "sacred"])

print("\n Installing configargparse :\n")
list_files = subprocess.run(["pip3", "install", "configargparse"])

print("\n Installing adamod :\n")
list_files = subprocess.run(["pip3", "install", "adamod"])

print("\n Installing ignite version 1.1.0 :\n")
list_files = subprocess.run(["pip3", "install", "ignite==1.1.0"])

print("\n Installing networkx version 2.3 :\n")
list_files = subprocess.run(["pip3", "install", "networkx==2.3"])

print("\n Installing numpy version 1.16.3 :\n")
list_files = subprocess.run(["pip3", "install", "numpy==1.16.3"])

print("\n Installing scipy :\n")
list_files = subprocess.run(["pip3", "install", "scipy"])

print("\n Installing scikit-learn :\n")
list_files = subprocess.run(["pip3", "install", "-U", "scikit-learn"])

print("\n Installing tensorboardX version 1.6 :\n")
list_files = subprocess.run(["pip3", "install", "tensorboardX==1.6"])

print("\n Installing torch :\n")
list_files = subprocess.run(["pip3", "install", "torch"])

print("\n Installing torchvision version 0.2.2 :\n")
list_files = subprocess.run(["pip3", "install", "torchvision==0.2.2"])

print("\n Installing seaborn :\n")
list_files = subprocess.run(["pip3", "install", "seaborn"])

print("\n Installing pandas :\n")
list_files = subprocess.run(["pip3", "install", "pandas"])

print("\n Installing matplotlib :\n")
list_files = subprocess.run(["pip3", "install", "matplotlib"])

print("\n Installing pyyaml :\n")
list_files = subprocess.run(["pip3", "install", "pyyaml"])

print("\nInstallation process completed")

