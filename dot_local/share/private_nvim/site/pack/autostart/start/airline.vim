let g:airline#extensions#tabline#enabled = 1
let g:airline#extensions#tabline#formatter = 'unique_tail_improved'
let g:airline_powerline_fonts = 0
let g:airline_theme='gruvbox'
if !exists('g:airline_symbols')
	let g:airline_symbols = {}
endif
let g:airline_symbols.linenr = ' '
let g:airline_symbols.colnr = ''
let g:airline_symbols.maxlinenr = ' '
