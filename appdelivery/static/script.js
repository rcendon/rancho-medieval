/* ################# Animação menu modo Mobile #########################################*/
/* querySelector() = retorna o primeiro elemento dentro do documento */

/* Constante para chamar o botão menu mobile / ( <i class="bi bi-list menu-mobile"></i> )  */
const menuMobile = document.querySelector('.menu-mobile')

/* Constante para chamar o body */
const body = document.querySelector('body')

/* Na constante menuMobile sera adicionado um evento de click */
/* Este evento click altera o incone do botão menu-mobile */
menuMobile.addEventListener('click', () => {
    menuMobile.classList.contains("bi-list")  /* Busca nas classes se contem o bi-list */  
    ? menuMobile.classList.replace("bi-list","bi-x") /* ? = IF bi-list = true inverte o icone bi-list para bi-x */
    : menuMobile.classList.replace("bi-x","bi-list") /* : = ELSE inverte o icone bi-x para bi-list*/

    body.classList.toggle("menu-nav-active") /*Adiciona uma classe nova a minha tag body chamada menu-nav-active- style.css */
})


/* ################# Quantidade Cardápio #########################################*/
function id( el ){
    return document.getElementById( el );
}
window.onload = function(){
    id('mais').onclick = function(){
            id('format').value = parseInt( id('format').value )+1;

            id('total').value = 20*id('format').value;
    }
    id('menos').onclick = function(){
            if( id('format').value>0 )
                    id('format').value = parseInt( id('format').value )-1;

            id('total').value = 20*id('format').value;
    }
}


/* cria dinamicamente o formulário para inserção de dados de cartão para pagamento */
function gera_formulario_para_insercao_de_dados_de_cartao() {
    let div_formulario_pagamento = document.getElementById("detalhes_cartao");
    let cartao_credito = document.getElementById("cartao_credito");
    let cartao_debito = document.getElementById("cartao_debito");
    let formulario_pagamento =  document.createElement("form");
    formulario_pagamento.setAttribute('class', 'row form-check form-control-lg pagamento')
    let elementos_formulario = {
        "1 - numero_do_cartao": "Número do Cartão",
        "2 - titular_do_cartao": "Nome do Titular do Cartão,",
        "3 - cpf_do_titular": "CPF do Titular",
        "4 - data_de_validade_do_cartao": "Data de validade",
        "5 - cvc": "CVC"
    };

    if ((cartao_credito.checked === true) || (cartao_debito.checked === true)) {
        if (div_formulario_pagamento.innerHTML.trim() === '') {
            div_formulario_pagamento.insertAdjacentElement ("afterbegin", formulario_pagamento);
            for (let campo in Object.keys(elementos_formulario)) {
                let input = document.createElement('input')
                input.setAttribute('id', 'teste')
                input.setAttribute('name', {campo})
                input.setAttribute('class', 'form-control col-sm-3')
                let label = document.createElement('label')
                label.setAttribute('for', {campo})
                label.innerText = 'teste'
                formulario_pagamento.appendChild(input)
                formulario_pagamento.appendChild(label)
            };
        };
    } else {
        div_formulario_pagamento.textContent = '';
    };
};

/* ######## carrega a função quando do carregamento da página ####### */

function adiciona_produto_carrinho(produto, produto_id) {
    if (valor_cookie(produto) > 0) {
        let valor = parseInt(valor_cookie(produto)) + 1;
        document.cookie = produto + "=" +  valor.toString() + ";";
    } else {
        document.cookie = produto + "=1;";
    }
    define_quantidade_produto(produto, produto_id)
}

function remove_item_carrinho(produto, produto_id) {
    if (valor_cookie(produto) > 1) {
        let valor = parseInt(valor_cookie(produto)) - 1;
        document.cookie = produto + "=" +  valor.toString() + ";";
    } else {
        document.cookie = produto + "=0; expires=Fri, 5 Oct 2018 14:28:00 GMT;";
    }

    if (valor_cookie(produto) === undefined ) {
        let produto_contador = document.getElementById(produto_id);
        produto_contador.innerHTML = '0';
    } else {
        define_quantidade_produto(produto, produto_id)
    }
}

function valor_cookie(item) {
    const nome = item + "=";
    const cookie_decoded = decodeURIComponent(document.cookie);
    const valores = cookie_decoded.split('; ');
    let resultado;
    valores.forEach( valor => {
        if (valor.indexOf(nome) === 0) resultado = valor.substring(nome.length);
    })
    return resultado
}

function define_quantidade_produto(produto_nome, produto_id) {
    let produto = document.getElementById(produto_id);
    produto.innerHTML = valor_cookie(produto_nome)
}



window.onload = gera_formulario_para_insercao_de_dados_de_cartao();

window.onload = adiciona_produto_carrinho();

window.onload = valor_cookie();

window.onload = remove_item_carrinho();

window.onload = define_quantidade_produto();


