-- Extensiones
create extension pgcrypto;
create extension fuzzystrmatch;
create extension hstore;
create extension postgres_fdw;
create extension tablefunc;
create extension cube;
create extension dict_xsyn;
create extension pg_trgm;
create extension "uuid-ossp";

-- Eliminar tablas
drop table if exists fips_codes;

-- Crear tablas
create table fips_codes (
       fips_code uuid primary key default gen_random_uuid(),
       state varchar,
       state_fips_code varchar,
       county_fips_code varchar,
       county varchar,
       fips_class_code varchar
);
