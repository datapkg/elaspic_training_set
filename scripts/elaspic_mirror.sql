-- Replace '{{ datapkg_connection_string }}' with the actual DATAPKG_CONNECTION_STRING

-- Install CONNECT engine
INSTALL SONAME 'ha_connect';


-- Create ELASPIC schema
DROP SCHEMA IF EXISTS elaspic;
CREATE SCHEMA elaspic;
USE elaspic;


-- Convert TEXT to VARCHAR
SET connect_type_conv=YES;
SET connect_conv_size = 8192;  # default


-- PDB tables
CREATE TABLE domain engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/domain';

CREATE TABLE domain_contact engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/domain_contact';


-- Protein tabes
CREATE TABLE uniprot_sequence engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/uniprot_kb/uniprot_sequence';

CREATE TABLE provean engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/provean';


-- Domain tables
CREATE TABLE uniprot_domain engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain';

CREATE TABLE uniprot_domain_template engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_template';

CREATE TABLE uniprot_domain_model engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_model';


-- Interface tables
CREATE TABLE uniprot_domain_pair engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_pair';

CREATE TABLE uniprot_domain_pair_template engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_pair_template';

CREATE TABLE uniprot_domain_pair_model engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_pair_model';


-- Mutation tables (require a smaller VARCHAR due to the large number of text columns)
SET connect_conv_size = 4096;

CREATE TABLE uniprot_domain_mutation engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_mutation';

CREATE TABLE uniprot_domain_pair_mutation engine=CONNECT table_type=MYSQL
connection='{{ datapkg_connection_string }}/elaspic/uniprot_domain_pair_mutation';
