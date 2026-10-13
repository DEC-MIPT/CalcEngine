-- Synthetic read contract of the normative catalog for the backend's postgres tests
-- (normative-catalog-backend design.md, decisions 1, 2 and 9). Tables stand in for
-- Egor's views and carry the same names and columns; tests/catalog_fixture.py fills
-- them with placeholder rows. Run only on a database named *_test, as its owner.
-- The role is not dec_normatives_reader: roles are cluster-wide on dec-postgres, which
-- also holds Egor's database dec.

DROP SCHEMA IF EXISTS catalog_read CASCADE;
DROP TABLE IF EXISTS public.catalog_contract_private;

CREATE SCHEMA catalog_read;

CREATE TABLE catalog_read.documents (
    document_id integer NOT NULL,
    designation text NOT NULL,
    title text NOT NULL,
    edition text NOT NULL,
    year integer,
    source_url text
);

CREATE TABLE catalog_read.clauses (
    document_id integer NOT NULL,
    position integer NOT NULL,
    number text NOT NULL,
    title text,
    page integer
);

CREATE TABLE catalog_read.type_formulas (
    calculation_type text NOT NULL,
    parameter text NOT NULL,
    result_symbol text NOT NULL,
    latex text NOT NULL,
    tree jsonb NOT NULL,
    units jsonb NOT NULL,
    norm_refs jsonb NOT NULL
);

CREATE TABLE catalog_read.type_table_values (
    calculation_type text NOT NULL,
    parameter text NOT NULL,
    symbol text NOT NULL,
    latex text NOT NULL,
    value numeric NOT NULL,
    unit text NOT NULL,
    heading_symbol text,
    heading_value numeric,
    heading_unit text,
    norm_refs jsonb NOT NULL
);

CREATE TABLE catalog_read.type_thresholds (
    calculation_type text NOT NULL,
    parameter text NOT NULL,
    latex text NOT NULL,
    value numeric NOT NULL,
    unit text NOT NULL,
    norm_refs jsonb NOT NULL
);

CREATE TABLE catalog_read.type_checks (
    calculation_type text NOT NULL,
    parameter text NOT NULL,
    norm_refs jsonb NOT NULL
);

CREATE TABLE catalog_read.type_method_bounds (
    calculation_type text NOT NULL,
    quantity text NOT NULL,
    kind text NOT NULL,
    value numeric NOT NULL,
    unit text NOT NULL,
    inclusive boolean NOT NULL,
    norm_refs jsonb NOT NULL
);

CREATE FUNCTION catalog_read.search(query text, max_rows integer)
RETURNS TABLE (
    kind text,
    document_id integer,
    designation text,
    edition text,
    number text,
    title text,
    rank real
)
LANGUAGE sql STABLE AS $$
    SELECT hit.kind, hit.document_id, hit.designation, hit.edition, hit.number, hit.title, hit.rank
    FROM (
        SELECT 'document'::text AS kind, d.document_id, d.designation, d.edition,
               NULL::text AS number, d.title, 1.0::real AS rank
        FROM catalog_read.documents AS d
        WHERE strpos(lower(d.designation), lower(query)) > 0
           OR strpos(lower(d.title), lower(query)) > 0
        UNION ALL
        SELECT 'clause'::text, c.document_id, d.designation, d.edition, c.number, c.title,
               0.5::real
        FROM catalog_read.clauses AS c
        JOIN catalog_read.documents AS d ON d.document_id = c.document_id
        WHERE strpos(lower(c.title), lower(query)) > 0
    ) AS hit
    ORDER BY hit.rank DESC, hit.designation COLLATE "C", hit.number COLLATE "C" NULLS FIRST
    LIMIT max_rows
$$;

CREATE TABLE public.catalog_contract_private (secret text);
REVOKE ALL ON public.catalog_contract_private FROM PUBLIC;

DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'dec_catalog_test_reader') THEN
        CREATE ROLE dec_catalog_test_reader NOLOGIN;
    END IF;
END
$$;

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON FUNCTION catalog_read.search(text, integer) FROM PUBLIC;
GRANT USAGE ON SCHEMA catalog_read TO dec_catalog_test_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA catalog_read TO dec_catalog_test_reader;
GRANT EXECUTE ON FUNCTION catalog_read.search(text, integer) TO dec_catalog_test_reader;
