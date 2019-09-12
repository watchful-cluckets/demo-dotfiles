# My Dev Env

Create a lightweight method for reproducing my dev env across machines.

## Requirements

Git needs to be installed and ssh keys need to be configured with the VCS provider. Assumes I'm using macOS due to use of `brew`.

## Initial Setup

### Dotfiles

Install the [init-dotfiles](https://github.com/Vaelatern/init-dotfiles) tools for [dotbot](https://git.io/dotbot):

```bash
curl -fsSLO https://raw.githubusercontent.com/Vaelatern/init-dotfiles/master/init_dotfiles.sh
chmod +x ./init_dotfiles.sh
```

Do a test run (calls dotbot):
```bash
./init_dotfiles.sh test
```

Create the real thing (calls dotbot):
```bash
./init_dotfiles.sh verbose-config
```



### Git Secrets

Install [`git-secrets`](https://github.com/awslabs/git-secrets) to prevent bad things from happening on accident:

```bash
brew install git-secrets
cd ~/.dotfiles
git secrets --install
git secrets --register-aws
```



### Git Crypt

Install [`git-crypt`](https://github.com/AGWA/git-crypt) to handle encryption of secrets. The GPG key is then saved to my Tresorit account for sharing:

```bash
brew install git-crypt
cd ~/.dotfiles
git-crypt init
printf '%s\n' 'secretfile filter=git-crypt diff=git-crypt' '*.key filter=git-crypt diff=git-crypt' > .gitattributes
mkdir secrets
printf '%s\n' '* filter=git-crypt diff=git-crypt' '.gitattributes !filter !diff' > .secrets/.gitattributes
git-crypt export-key ~/.ssh/git_crypt_dotfiles
cp ~/.ssh/git_crypt_personal ~/Tresors/Admin/
```



### AWS Keys

Install [IAM key rotation](https://aws-rotate-iam-keys.com/) to further provide security on AWS access. For restricted users, read the docs to directly attach  the IAM policy for key rotation.

```shell
brew tap rhyeal/aws-rotate-iam-keys https://github.com/rhyeal/aws-rotate-iam-keys
brew install aws-rotate-iam-keys

# add cron steps: https://github.com/rhyeal/aws-rotate-iam-keys#macos-1
brew services start aws-rotate-iam-keys

# add profile names to config file
cp /usr/local/etc/aws-rotate-iam-keys ~/.dotfiles/secrets/aws-rotate-iam-keys
emacs ~/.aws-rotate-iam-keys
brew services restart aws-rotate-iam-keys
```



### Freeze Files

Create a brew file:

```shell
brew bundle dump --force --file=~/.dotfiles/macos/Brewfile
```

Create a Python freeze file:

```bash
pip3 list --format=freeze > ~/.dotfiles/computing/python_requirements
```

Create an R freeze file:
```bash
Rscript ~/.dotfiles/admin-tools/store_packages.R
```



### Commit

Add everything to GitHub and roll-on:

```bash
git init
git add .
git commit -am "first commit"
git remote add origin git@github.com:<user_name>/<repo_name>.git
git push -u origin master
```



## Usage

Clone with all submodules:
``` bash
git clone --recursive git@github.com:your-username/dotfiles.git
```

Run the setup scripts:
``` bash
mv dotfiles .dotfiles
cd .dotfiles
./install
```

Decrypt secrets locally:

```bash
git-crypt unlock ~/.ssh/git_crypt_dotfiles
```



## Key Model

Be secure with keys:

```bash
ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_ed25519_something -C "someone"
ssh-copy-id -i ~/.ssh/id_ed25519_something someone@some-ip
```



## macOS Style Guide

- System sans serif font: Open Sans 12 pt
- System serif font: Libre Baskerville 12 pt
- System fixed-width font: Hack 10 pt
- Dark mode
- Highlight color: #b3a369



## ToDo

* Consider adding support for [Cookiecutter Data Science](http://drivendata.github.io/cookiecutter-data-science/)
* Add install for linux and macos?
* macOS to make pyproj work:
  * brew install geos; brew install gdal; brew install spatialindex
  * sudo -H pip3 install git+https://github.com/jswhit/pyproj.git
* ensure wakatime installs across IDEs
* test that all installs correctly across baseimage
* install?
  * https://github.com/donnemartin/dev-setup
  * https://github.com/xonsh/xonsh
