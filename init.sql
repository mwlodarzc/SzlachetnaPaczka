CREATE TABLE IF NOT EXISTS family(
    family_id BIGSERIAL NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS person(
    person_id BIGSERIAL PRIMARY KEY,
    pesel CHAR(11) NOT NULL,
    forename TEXT NOT NULL,
    surname TEXT NOT NULL,
    adress TEXT NOT NULL,
    birth DATE NOT NULL,
    family_ref_id BIGINT REFERENCES family(family_id)
);