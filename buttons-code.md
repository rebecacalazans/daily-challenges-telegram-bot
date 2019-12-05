## Códigos para processamento dos botões

##### Lista de desafios
`select_challenge <challenge_id>`: Abre o menu para o desafio escolhido


##### Tela inicial do desafio
`challenge <challenge_id> menu`: Apresenta opções para o desafio

##### Menu do desafio
`challenge <challenge_id> hide`: Oculta o menu do desafio
`challenge <challenge_id> participate`: Inscreve usuário no desafio
`challenge <challenge_id> add <value>`: Adiciona o valor à contagem e ao total (até o mínimo de 0, no caso do valor ser negativo)
`challenge <challenge_id> new_day`: Reinicia a contagem e adiciona 1 aos dias

`challenge <challenge_id> total_add <value>`: Adiciona o valor apenas ao total (até o mínimo de 0, no caso do valor ser negativo)
`challenge <challenge_id> remove_day`: subtrai 1 do total de dias (até o mínimo de 0)
