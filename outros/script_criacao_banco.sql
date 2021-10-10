create table enderecos (
    id serial primary key not null,
    rua varchar (100),
    bairro varchar(100),
    cidade varchar(50),
    estado varchar(50),
    pais varchar(40),
    numero int,
    complemento varchar(100),
    tipo_endereco char(1)
);

create table pessoas (
    id serial primary key not null,
    login varchar(10) unique not null,
    nome varchar(50) not null,
    cpf int unique not null,
    rg int unique not null,
    tipo char(1) not null,
    senha varchar(64) not null,
    endereco int,
    constraint endereco
        foreign key (endereco) references enderecos(id)
);

create table fornecedores (
    id serial primary key not null,
    nome varchar(50) not null,
    cnpj int unique not null,
    contato int,
    email varchar(40),
    endereco_fornecedor int,
    constraint endereco_fornecedor
        foreign key (endereco_fornecedor) references enderecos(id)
);

create table insumos (
    id serial primary key not null,
    nome varchar(50) unique not null,
    quantidade_estoque_insumo int not null
);

create table cardapio (
    id_produto serial  primary key not null,
    nome varchar(50) not null,
    permite_estocagem char(1),
    quantidade_estoque_produto int not null,
    valor float
);

create table receitas (
    id_produto int,
    constraint id_produto
        foreign key (id_produto) references cardapio(id_produto),
    id_insumo int,
    constraint id_insumo
        foreign key (id_insumo) references insumos(id)
);

create table preco_insumo (
    id_fornecedor int not null,
    constraint id_fornecedor
        foreign key (id_fornecedor) references fornecedores(id),
    id_insumo int not null,
    constraint id_insumo
        foreign key (id_insumo) references insumos(id),
    preco float not null
);


create table pedidos (
    id serial  primary key not null,
    id_cliente int not null,
    valor float not null,
    constraint id_cliente
        foreign key (id_cliente) references pessoas(id)
);

create table itens_do_pedido (
    id_produto int,
    id_pedido int,
    constraint id_produto
        foreign key (id_produto) references cardapio(id_produto),
    constraint id_pedido
        foreign key (id_pedido) references pedidos(id)
);

