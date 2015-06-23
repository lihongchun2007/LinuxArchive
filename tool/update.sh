#!/usr/bin/env bash

#append configure file to configFiles
configFiles="$HOME/.bashrc $HOME/.vimrc $HOME/.xbindkeysrc $HOME/.tmux.conf $HOME/.gitconfig"
archivePath=../config

for config in $configFiles; do
    cp $config $archivePath
done

