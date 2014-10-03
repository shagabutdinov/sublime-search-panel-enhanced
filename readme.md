# Sublime SearchPanelEnhanced plugin

Replacement for default sublime "search in file" functionality.


### Demo

![Demo](https://raw.github.com/shagabutdinov/sublime-search-panel-enhanced/master/demo/demo.gif "Demo")


### WARNING

This plugin replace sublime's default "search" to unobvious shortcuts-driven
search. Please rtfm twice before using this plugin.

By default it maps search by "fuzzy" to keyboard. It can be really annoying for
somebody who don't like fuzzy behaviour so I suggest to those people disable
this plugin or make keyboard remap after installation.


### Reason (:scream::scream::scream::scream: MULTICURSORS :scream::scream::scream::scream:)

Sublime's default search works great but at one day I noticed that I would like
to change some behaviour of it. Things that annoyed me at most:

- no multicursors support (big shame)

- strange selection when I complete search (I need to always hit move by
character left to insert text at left of word or move by word right to
insert text at end of word; or both if I want to replace word)

After rewriting search panel and fixing those issues I've added some usefull
stuff to search panel. Everything are described in "Commands" section of this
readme.


### Installation

This plugin is part of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
plugin set. You can install sublime-enhanced and this plugin will be installed
automatically.

If you would like to install this package separately check "Installing packages
separately" section of [sublime-enhanced](http://github.com/shagabutdinov/sublime-enhanced)
package.


### Features

- Search through file by text, word, regexp and fuzzy expresssion (oO)

- Go to start or end of word when completing search; or select word or all words
  occurences

- Change search modes with keyboard shortcuts (only)

- Find under cursor (it also differs a bit from sublime's default find_under)

- Select and delete to found functionality


### Usage

Hit keyboard shortcut to avoke search panel, enter desired text and hit "enter"
to go to found.


### Commands

| Description                   | Keyboard shortcuts | Command palette                              |
|-------------------------------|--------------------|----------------------------------------------|
| Display fuzzy panel           | ctrl+f             | SearchPanelEnhanced: Display fuzzy           |
| Display fuzzy backward panel  | ctrl+shift+f       | SearchPanelEnhanced: Display fuzzy backward  |
| Display normal panel          | ctrl+alt+f         | SearchPanelEnhanced: Display normal          |
| Display normal backward panel | ctrl+alt+shift+f   | SearchPanelEnhanced: Display normal backward |
| Goto next result              | alt+f              | SearchPanelEnhanced: Goto next result        |
| Goto previous result          | alt+shift+f        | SearchPanelEnhanced: Goto previous result    |
| Find under                    | alt+e              | SearchPanelEnhanced: Find under              |
| Find under backward           | alt+shift+e        | SearchPanelEnhanced: Find under backward     |
| Go to end of found            | ctrl+enter         |                                              |
| Select found                  | shift+enter        |                                              |
| Select all found              | ctrl+shift+enter   |                                              |
| Toggle regexp                 | alt+q              |                                              |
| Toggle word                   | alt+w              |                                              |
| Toggle fuzzy                  | alt+e              |                                              |
| Toggle case sensetive         | alt+s              |                                              |
| Show previous search          | alt+i              |                                              |
| Show next search              | alt+k              |                                              |
| Select to found               | ctrl+s             |                                              |
| Delete to found               | ctrl+d             |                                              |


### Dependencies

- https://github.com/shagabutdinov/sublime-status-message