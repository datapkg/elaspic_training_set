drop schema if exists elaspic_training;
create schema elaspic_training;

create view elaspic_training.domain as select * from elaspic.domain;

create view elaspic_training.domain_contact as select * from elaspic.domain_contact;

create view elaspic_training.provean as select * from elaspic.provean;


create table elaspic_training.uniprot_domain like elaspic.uniprot_domain;
alter table elaspic_training.uniprot_domain
MODIFY COLUMN uniprot_domain_id INT NOT NULL,
ADD COLUMN max_seq_identity int,
ADD COLUMN uniprot_domain_id_old int;

create table elaspic_training.uniprot_domain_template like elaspic.uniprot_domain_template;

create table elaspic_training.uniprot_domain_model like elaspic.uniprot_domain_model;

create table elaspic_training.uniprot_domain_mutation like elaspic.uniprot_domain_mutation;


create table elaspic_training.uniprot_domain_pair like elaspic.uniprot_domain_pair;
alter table elaspic_training.uniprot_domain_pair
MODIFY COLUMN uniprot_domain_pair_id INT NOT NULL,
ADD COLUMN max_seq_identity INT,
ADD COLUMN uniprot_domain_pair_id_old INT;

create table elaspic_training.uniprot_domain_pair_template like elaspic.uniprot_domain_pair_template;

create table elaspic_training.uniprot_domain_pair_model like elaspic.uniprot_domain_pair_model;

create table elaspic_training.uniprot_domain_pair_mutation like elaspic.uniprot_domain_pair_mutation;
