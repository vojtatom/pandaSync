#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Creating pandaSync symlink..."
echo "Recomanded destination directories (where I teseted it):

	macOS/Linux: /usr/local/bin

"
printf "Where do you want to install: "
read install_path

if [ ! -d "$install_path" ]; then
	echo "Cannot find folder $install_path!" 1>&2
	exit 1
fi

install_link="${install_path%%/}/panda"

if [ -d "$install_link" ] || [ -L "$install_link" ]; then
	printf "$install_link file already exists! Delete and replace? [y/n]: "
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

echo "Creating link..."
ln -s "$DIR/__main__.py" "$install_link"
if [ "$?" = "1" ]; then
	echo "Cannot create link." 1>&2
	rm -r "$install_path"
	exit 1
fi

echo "A copy of pandaSync was installed. Run the program with: 

	panda pull - for downloading data from the server
	panda push - for uploading to the server

The pull command is recomanded to be done first."


