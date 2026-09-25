# Migrações PostgreSQL arquivadas

Essas migrações pertencem a uma tentativa anterior de Postgres, anterior à
migração definitiva de 25/09/2026, e **não são aplicadas** pela configuração
atual do Prisma.

O histórico ativo é `prisma/migrations`, com uma baseline única gerada do
schema atual (`20260925000000_init_postgres`) e aplicada ao Neon. As migrações
deste diretório foram preservadas apenas como referência histórica e estão
defasadas em relação ao schema.

Não copie este diretório para `prisma/migrations`: as tabelas já existem no
banco ativo e a aplicação falharia. Se precisar do SQL antigo como referência,
compare-o com `prisma/migrations/20260925000000_init_postgres/migration.sql`.

O histórico SQLite anterior à migração está arquivado em
`prisma/migrations-sqlite`, também fora do alcance do Prisma.
