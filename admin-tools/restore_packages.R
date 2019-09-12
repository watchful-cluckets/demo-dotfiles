# restore_packages.R
#
# installs each package from the stored list of packages
# source: http://hlplab.wordpress.com/2012/06/01/transferring-installed-packages-between-different-installations-of-r/

load("~/.dotfiles/computing/r_requirements")

for (count in 1:length(installedpackages)) {
    install.packages(installedpackages[count])
}
