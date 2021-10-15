# .dotfiles

version: v0.5.0

A lightweight method for reproducing my dev env across machines.

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

Install [`git-crypt`](https://github.com/AGWA/git-crypt) to handle encryption of secrets. The signing key is saved to [Tresorit](https://tresorit.com/) for sharing:

```bash
# install git-crypt
brew install git-crypt

# access dotfiles and add secrets dir
cd ~/.dotfiles
mkdir secrets

# initialize
git-crypt init

# create gitattributes file to denote usage
printf '%s\n' 'secretfile filter=git-crypt diff=git-crypt' '*.key filter=git-crypt diff=git-crypt' > .gitattributes
printf '%s\n' '* filter=git-crypt diff=git-crypt' '.gitattributes !filter !diff' > .secrets/.gitattributes

# create key
git-crypt export-key ~/.ssh/git_crypt_dotfiles

# save key securely for sharing
cp ~/.ssh/git_crypt_dotfiles ~/Tresors/Admin/
```

### AWS Credentials

#### Key Rotation

Install [IAM key rotation](https://aws-rotate-iam-keys.com/) to further provide security on AWS access. For restricted users, read the docs to directly attach the IAM policy for key rotation.

```shell
# install key rotation tool
brew tap rhyeal/aws-rotate-iam-keys https://github.com/rhyeal/aws-rotate-iam-keys
brew install aws-rotate-iam-keys

# add cron steps: https://github.com/rhyeal/aws-rotate-iam-keys#macos-1
brew services start aws-rotate-iam-keys

# add profile names to config file
cp /usr/local/etc/aws-rotate-iam-keys ~/.dotfiles/secrets/aws-rotate-iam-keys
emacs ~/.aws-rotate-iam-keys
brew services restart aws-rotate-iam-keys
```

#### Swapping Credentials

There is a customized script which allows you to switch credentials easily. Some aliases rely on this script.

```bash
$(aws-env my_aws_profile)
```

### Freeze Files

Simple, run the script:

```bash
bin/update_freeze
```

### Update Shell

Many of these tools need Bash 5.0+:

```bash
brew install bash
sudo emacs /etc/shells

# add /usr/local/bin/bash
# save and exit

chsh

# select /usr/local/bin/bash
# save and exit
```

### Create Repo

If you've created and stored a GitHub personal token in the env already, then leverage the shell function aliases `ghcreate` and `ghinit`. Otherwise, create a repo on GH manually.

```bash
# ghcreate uses local dir name, in this case, .dotfiles
# $1 == repo description
# $2 == private repo?
ghcreate "A lightweight method for reproducing my dev env across machines" True
ghinit

# alternative
git add .
git commit -S -nam "first commit"
git remote add origin git@github.com:<user_name>/<repo_name>.git
git push -u origin master
```

### Add Subrepos

I've started using `git-subrepo` as a replacement for the pain of using submodules -- which is wEiRd, because this repo uses submodules! .dotfiles is aimed at reproducible environments, and `git-subrepo` is third-party, thus I cannot use it for this repo.

First install [`git-subrepo`](https://github.com/ingydotnet/git-subrepo):

```bash
git submodule add https://github.com/ingydotnet/git-subrepo
echo 'source ~/.dotfiles/git-subrepo/.rc' >> shell/bashrc
```

Then start adding submodules:

```bash
git subrepo clone https://github.com/Bash-it/bash-it
git subrepo clone https://github.com/irondoge/bash-wakatime
git subrepo clone https://github.com/pyenv/pyenv

git submodule add https://github.com/sobolevn/dotbot-brewfile.git
git submodule add git@gist.github.com:deb3caa658eb89379e8db80a0debded0.git
```

## Usage

Clone with all submodules, run the setup scripts, and decrypt secrets locally:

```bash
git clone --recursive git@github.com:kcavagnolo/dotfiles.git

mv dotfiles .dotfiles
cd .dotfiles
./install

git-crypt unlock ~/.ssh/git_crypt_dotfiles
```

## Semantic Versioning

To update the version of the docs that has been released, use [`bumpversion`](https://github.com/peritus/bumpversion). Some examples of bumping:

```bash
# major bump
bumpversion major --verbose

# minor bump
bumpversion minor --verbose

# patch bump
bumpversion patch --verbose
```

When satisfied with the version, push changes with tags using the manual command below or by adding it as a global option:

```bash
# global option (the default here)
git config --global push.followTags true

# manual option
git push --follow-tags
```

## Key Models

### SSH

I like to reuse existing key agents to avoid process bloat. See this [concise blog post](http://blog.joncairns.com/2013/12/understanding-ssh-agent-and-ssh-add/). The tool I adopted is [`ssh_find_agent`](https://github.com/wwalker/ssh-find-agent). This tool is sourced in `shell/bash_aliases` and then made available through the `$HOME/.bin` directory which is linked from the `bin/` folder in this repo during the install process.

```bash
ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_ed25519_something -C "someone"
ssh-copy-id -i ~/.ssh/id_ed25519_something someone@some-ip
```

Copy/paste SSH key to system of record

### GPG

```bash
sudo ln -s /bin/gpg /usr/local/bin/
sudo ln -s /bin/pinentry /usr/local/bin/
gpg --list-secret-keys --keyid-format LONG
gpg --full-generate-key
gpg --list-secret-keys --keyid-format LONG
gpg --armor --export <a-key>
git config --local user.signingkey <a-key>
```

Copy/paste GPG key to system of record

## Python

I hate [Python's environment setup](https://xkcd.com/1987/), so I use [`pyenv`](https://github.com/pyenv/pyenv) installed via [`pyenv-installer`](https://github.com/pyenv/pyenv-installer) to manage environments.

```bash
curl https://pyenv.run | bash
pyenv install 3.x.x
pyenv global 3.x.x
pip install -r ~/.dotfiles/computing/python_requirements
```

## Jupyter

To track the paths for Jupyter:

```bash
jupyter --paths
```

Install remote connection libs:

```bash
pip install --upgrade jupyter_http_over_ws
jupyter serverextension enable --py jupyter_http_over_ws
```

Install `nbextension`:

```bash
pip install jupyter_contrib_nbextensions
pip install jupyter_nbextensions_configurator
jupyter contrib nbextension install --user
jupyter nbextensions_configurator enable --user
```

I rely on [`jupyter-themes`](https://github.com/dunovank/jupyter-themes) to control the look of my notebooks:

```bash
pip install jupyterthemes
jt \
    -t onedork \
    -N -kl -T -altp \
    -f hack -fs 10 \
    -tf opensans -tfs 12 \
    -nf opensans -nfs 12 \
    -dfs 8 \
    -ofs 10 \
    -cellw 66% \
    -lineh 150 \
    -m 200 \
    -cursc x -cursw 3
```

## VS Code

1. Install the [Sync extension](https://marketplace.visualstudio.com/items?itemName=Shan.code-settings-sync)
2. Open the extension settings.
3. Fetch the `GITHUB_VSCODE_SYNC_GIST` and `GITHUB_VSCODE_SYNC_TOKEN` env vars.
4. Add them to extension.
5. Restart VS Code.

## OS Style Guide

- System sans serif font: [Open Sans](https://fonts.google.com/specimen/Open+Sans?preview.text_type=custom) 12 pt
- System serif font: [Libre Baskerville](https://fonts.google.com/specimen/Libre+Baskerville?preview.text_type=custom) 12 pt
- System fixed-width font: [Hack](https://github.com/source-foundry/Hack) 10 pt
- Highlight color: `#b3a369`

## Linux

- [Logitech Mice](https://github.com/PixlOne/logiops)
- [Google Drive](https://github.com/astrada/google-drive-ocamlfuse)
- [macOS Keyboard Mappings](https://github.com/rbreaves/kinto) and mind the [`pyenv` bug](https://github.com/rbreaves/kinto/issues/388#issuecomment-798895090)
