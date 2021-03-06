#!/usr/bin/env python3
# Script was first made the
# 5. march 2013
# And it was made by: TheRedMood < Teodor Spaeren >
#
# This aims to be the setup file for my configuration files. It is based around
# the idea that linking everything will make updating the main repo much easier.
# I hope that you all have a nice day and enjoy the script!

import os

# Global variables
HOME = os.path.expanduser('~')
DOTDIR = os.path.expanduser('~/.dot-yeah')

dotfiles = []
class Dotfile:
    """ A object for each file or directory that needs to be setup. """
    def __init__(self, name, gitplace, sysplace, isdir=False, place=""):
        self.name     = name
        self.gitplace = gitplace
        self.sysplace = sysplace
        self.isdir    = isdir
        self.place    = place

        dotfiles.append(self)

    def exists(self):
        if self.isdir:
            return os.path.isdir(self.sysplace)
        else:
            return os.path.isfile(self.sysplace)

    def placetest(self):
        if self.place != "" and not os.path.isdir(self.place):
            os.system("mkdir -p {0}".format(self.place))

    def link(self):
        os.system("ln -s {0} {1}".format(self.gitplace, self.sysplace))

# Functions
def warn():
    answer = input("(Y/N): ")
    if answer.lower() == 'y': return True
    else: return False

# We need all the DotFile objects. Here we have all file objects
xres  = Dotfile("Xresources", "{0}/config/Xresources".format(DOTDIR),  "{0}/.Xresources".format(HOME))

zsh       = Dotfile("zsh"       , "{0}/zsh/zshrc".format(DOTDIR)          , "{0}/.zshrc".format(HOME)      )
zprofile  = Dotfile("zprofile"  , "{0}/zsh/zprofile".format(DOTDIR)       , "{0}/.zprofile".format(HOME)   )
conky     = Dotfile("conky"     , "{0}/config/conkyrc".format(DOTDIR)     , "{0}/.conkyrc".format(HOME)    )
xinit     = Dotfile("xinit"     , "{0}/config/xinitrc".format(DOTDIR)     , "{0}/.xinitrc".format(HOME)    )
xbindkeys = Dotfile("xbindkeys" , "{0}/config/xbindkeysrc".format(DOTDIR) , "{0}/.xbindkeysrc".format(HOME))
tmux      = Dotfile("tmux"      , "{0}/config/tmux.conf".format(DOTDIR)   , "{0}/.tmux.conf".format(HOME)  )

# We need to check directories to.
fonts   = Dotfile("fonts"   , "{0}/fonts".format(DOTDIR)   , "{0}/.fonts".format(HOME)  , True)

# Here we have the cases where theres extra checking to be done
zshgit  = Dotfile("zsh-git"  , "{0}/zsh/git.zsh".format(DOTDIR)  , "{0}/.zsh/git.zsh".format(HOME)  , False , "{0}/.zsh".format(HOME))
zshkeys = Dotfile("zsh-keys" , "{0}/zsh/keys.zsh".format(DOTDIR) , "{0}/.zsh/keys.zsh".format(HOME) , False , "{0}/.zsh".format(HOME))
irssitheme  = Dotfile("irssi-theme" , "{0}/irssi/simple.theme".format(DOTDIR) , "{0}/.irssi/simple.theme".format(HOME), False,"{0}/.irssi".format(HOME))
irssiscripts   = Dotfile("irssi-scripts"   , "{0}/irssi/scripts".format(DOTDIR)   , "{0}/.irssi/scripts".format(HOME), True, "{0}/.irssi".format(HOME))

# We need to use all the elements up there
for dotfile in dotfiles:
    print("Linking {0}...".format(dotfile.name), end=' ')

    if not dotfile.exists() and warn():
        dotfile.placetest()
        dotfile.link()
    elif dotfile.exists():
        print("Skipping.")

#------------------NON LINKING OPERATIONS---------------------#
# I need to initialize the modules
print("Starting git submodule init:")
os.system("git --git-dir={0}/.git/ submodule init".format(DOTDIR))

# Now we need to update them
print("Starting git submodule update:")
os.system("git --git-dir={0}/.git/ submodule update --recursive".format(DOTDIR))

# Getting inxi
os.system("wget -c smxi.org/inxi -O {0}/scripts/inxi".format(HOME))
os.system("chmod +x {0}/scripts/inxi".format(HOME))

# Fonts
os.system("fc-cache -vf")
