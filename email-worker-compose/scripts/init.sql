create database email_sender;

\c email_sender

create table emails (
    id serial not null,
    data timestamp not null default current_timestamp,
    email varchar(100) not null, 
    assunto varchar(100) not null,
    mensagem  varchar(500) not null
);