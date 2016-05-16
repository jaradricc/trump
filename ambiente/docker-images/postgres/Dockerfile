FROM postgres:9.4.4

ADD fips.csv /docker-entrypoint-initdb.d
ADD create_tables.sql /docker-entrypoint-initdb.d
ADD insert_fips.sh /docker-entrypoint-initdb.d
