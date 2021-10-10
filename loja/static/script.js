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
