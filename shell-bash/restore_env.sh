#!/bin/bash

cd $HOME
mkdir git 
mkdir git/personal
set -e
# Packages install
# Install zsh
sudo apt install zsh \
    curl \
    ca-certificates \
    git -y

# Clone personal scripts
git clone git@github.com:carlosgit2016/scripts_util.git git/scripts_util git/personal/scripts_util

# ZSH
## Install oh myzsh
zsh --version
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
## Clone and copy zsh history and rc
git clone git@github.com:carlosgit2016/backups.git git/personal/backups
cp git/personal/backups/.zsh_history git/personal/backups/.zshrc $HOME


# set crontab config
crontab git/personal/backups/crontab_user

# ASDF
## clone asdf
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.10.2
zsh configure_asdf_plugins.sh

# Install azure cli
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash


# i3 CONFIG
## Install i3 manager
/usr/lib/apt/apt-helper download-file https://debian.sur5r.net/i3/pool/main/s/sur5r-keyring/sur5r-keyring_2022.02.17_all.deb keyring.deb SHA256:52053550c4ecb4e97c48900c61b2df4ec50728249d054190e8a0925addb12fc6
dpkg -i ./keyring.deb
echo "deb http://debian.sur5r.net/i3/ $(grep '^DISTRIB_CODENAME=' /etc/lsb-release | cut -f2 -d=) universe" >> /etc/apt/sources.list.d/sur5r-i3.list
sudo apt update
sudo apt install i3
## Clone and copy i3 config 
cp -f config ~/.config/i3/config

# TILIX
## Install tillix terminal
sudo apt install tilix -y
## Set default terminal
sudo update-alternatives --config x-terminal-emulator

## Setting default 
chsh -s $(which zsh)