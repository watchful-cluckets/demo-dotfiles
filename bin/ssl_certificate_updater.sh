#!/bin/bash

set -o errexit -o nounset -o pipefail -o noclobber -e

# USAGE:
# chmod +x ./ssl_certificate_updater.sh
# sudo ./ssl_crt_creater.sh

# check for root
if [ $(id -u) -ne 0 ]; then
	printf "Script must be run as root. Try 'sudo ./ssl_certificate_updater.sh'\n"
	exit 1
fi

# check for packages
lst="update-ca-certificates openssl"
for items in $lst; do
	type -P $items &>/dev/null || {
		echo -en "\n Package \"$items\" is not installed!"
		echo -en "\n Install now? [yes]/[no]: "
		read ops
		case $ops in
		YES | yes | Y | y) sudo apt-get install $items ;;
		*)
			echo -e "\n Exiting..."
			exit 1
			;;
		esac
	}
done

# update extensions from pem to crt
for file in *.pem; do
	[ -f "$file" ] || break
	cp "$file" "$(basename "$file" .pem).crt"
done

# mv the crt files into the sys cert folder
CACERTS="/usr/local/share/ca-certificates/"
if [ -d "$CACERTS" ]; then
	mv -f *.crt $CACERTS
fi

# update cert registry
update-ca-certificates

# exit safely
exit 0
