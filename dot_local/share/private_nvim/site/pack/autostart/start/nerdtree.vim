let NERDTreeShowHidden=1
let NERDTreeWinPos="right"
nnoremap <leader>2 :NERDTreeToggle<CR>
autocmd BufEnter * if tabpagenr('$') == 1 &&
		\ winnr('$') == 1 &&
		\ exists('b:NERDTree') &&
		\ b:NERDTree.isTabTree() | quit | endif
autocmd BufEnter * if bufname('#') =~ 'NERD_tree_\d\+' &&
		\ bufname('%') !~ 'NERD_tree_\d\+' &&
		\ winnr('$') > 1 |
		\ let buf=bufnr() | buffer# | execute "normal! \<C-W>w" |
		\ execute 'buffer'.buf | endif
