#!/bin/bash

echo "Installing pandaSync..."
echo "Please specify where you want to install the program.
The preffered path should be located in your PATH folders, recomanded directories (where I teseted it):

	macOS: /usr/local/bin
"
printf "Where do you want to install: "

read install_path

if [ ! -d "$install_path" ]; then
	echo "Cannot find folder $install_path!" 1>&2
	exit 1
fi

install_link="${install_path%%/}/panda"
install_path="${install_path%%/}/pandaSync"

if [ -d "$install_path" ]; then
	printf "$install_path folder already exists! Delete and replace? [y/n]: "
	read delete
	if [ "y" == "${delete:0:1}" ]; then
		echo "Deleting..."
		rm -r "$install_path"
		if [ "$?" = "1" ]; then
			echo "Cannot delete $install_path" 1>&2
			exit 1
		fi
	else 
		exit 0
	fi
fi

if [ -e "$install_link" ] || [ -L "$install_link" ]; then
	printf "$install_link link already exists! Delete and replace? [y/n]: "
	read delete
	if [ "y" == "${delete:0:1}" ]; then
		echo "Deleting..."
		rm "$install_link"
		if [ "$?" = "1" ]; then
			rm -r "$install_link"
		fi
		if [ "$?" = "1" ]; then
		echo "Cannot delete $install_link" 1>&2
			exit 1
		fi
	else 
		exit 0
	fi
fi

echo "Creating folder..."
mkdir "$install_path"
if [ "$?" = "1" ]; then
	echo "Cannot create new folder." 1>&2
	exit 1
fi

echo "Installing..."
cp -R ./* "$install_path"
if [ "$?" = "1" ]; then
	echo "Cannot install the script." 1>&2
	rm -r "$install_path"
	exit 1
fi

echo "Creating link..."
ln -s "$install_path/__main__.py" "$install_link"
if [ "$?" = "1" ]; then
	echo "Cannot create link." 1>&2
	rm -r "$install_path"
	exit 1
fi

echo "A copy of pandaSync was installed. Run the program with: 

	panda pull - for downloading data from the server
	panda push - for uploading to the server

The pull command is recomanded to be done first."



# In case you were wondering what's in your path:
# echo $PATH | awk -F':' '{ for(i = 1; i <= NF; i++) print "	" $i }'
