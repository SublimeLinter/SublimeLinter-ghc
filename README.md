SublimeLinter-ghc
=========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-ghc.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-ghc)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [ghc](http://www.haskell.org/ghc/).
It will be used with files that have the "Haskell" syntax.

## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

To install `ghc`, you can install [haskell-platform](http://www.haskell.org/platform/) which includes `ghc` or [ghc](http://www.haskell.org/ghc/) itself. Follow the instructions on their websites to install. 

`haskell-platform` is available on many package managers, for example `brew update; brew install haskell-platform` on Mac OS X.

Please make sure that the path to `ghc` is available to SublimeLinter.
The docs cover [troubleshooting PATH configuration](http://sublimelinter.com/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings

- SublimeLinter settings: http://sublimelinter.com/en/latest/settings.html
- Linter settings: http://sublimelinter.com/en/latest/linter_settings.html
