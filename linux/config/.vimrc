"Vim Options
"-----------
set ff=unix
set ffs=unix

set history=1000               "remember last n commands
"set mouse=a                    "enable full mouse support in the console
set autoindent                 "don't know
set smartindent                "don't know
set shiftwidth=4               "don't know
set softtabstop=4              "eh?
set expandtab                  "no clue what this does

colorscheme elflord

set number                     "turn line numbering on
syntax on                      "syntax highlighting on
set ignorecase                 "make searches case-insensitive
set hlsearch

"
"Status Bar
"----------
"set ruler                      "turn on status bar
set showmode                   "display the current mode in the status line
set showcmd                    "show partially-typed commands in the status line
set laststatus=2               "always show status line 

"configuration for doxygentoolkit
let g:DoxygenToolkit_briefTag_pre="@Synopsis  "
let g:DoxygenToolkit_paramTag_pre="@Param "
let g:DoxygenToolkit_returnTag="@Returns   "
"let g:DoxygenToolkit_blockHeader="--------------------------------------------------------------------------"
"let g:DoxygenToolkit_blockFooter="----------------------------------------------------------------------------"
let g:DoxygenToolkit_authorName="Li Hongchun"
"let g:DoxygenToolkit_licenseTag="My own license" 


set grepprg=grep\ -nH\ $*
let g:tex_flavor="latex"
set runtimepath=~/.vim,$VIM/vimfiles,$VIMRUNTIME,$VIM/vimfiles/after,~/.vim/after

" Configuration of vim-addon-manager
" put this line first in ~/.vimrc
set nocompatible | filetype indent plugin on | syn on

fun! SetupVAM()
  let c = get(g:, 'vim_addon_manager', {})
  let g:vim_addon_manager = c
  let c.plugin_root_dir = expand('$HOME', 1) . '/.vim/vim-addons'

  " Force your ~/.vim/after directory to be last in &rtp always:
  " let g:vim_addon_manager.rtp_list_hook = 'vam#ForceUsersAfterDirectoriesToBeLast'

  " most used options you may want to use:
  " let c.log_to_buf = 1
  " let c.auto_install = 0
  let &rtp.=(empty(&rtp)?'':',').c.plugin_root_dir.'/vim-addon-manager'
  if !isdirectory(c.plugin_root_dir.'/vim-addon-manager/autoload')
    execute '!git clone --depth=1 git://github.com/MarcWeber/vim-addon-manager '
        \       shellescape(c.plugin_root_dir.'/vim-addon-manager', 1)
  endif

  " This provides the VAMActivate command, you could be passing plugin names, too
  call vam#ActivateAddons([], {})
endfun
call SetupVAM()

" ACTIVATING PLUGINS

" OPTION 1, use VAMActivate
" VAMActivate PLUGIN_NAME PLUGIN_NAME
VAMActivate vim-snippets snipmate

" OPTION 2: use call vam#ActivateAddons
"call vam#ActivateAddons([PLUGIN_NAME], {})
" use <c-x><c-p> to complete plugin names

" OPTION 3: Create a file ~/.vim-srcipts putting a PLUGIN_NAME into each line
" See lazy loading plugins section in README.md for details
" call vam#Scripts('~/.vim-scripts', {'tag_regex': '.*'})

