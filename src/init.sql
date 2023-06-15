CREATE TABLE IF NOT EXISTS user_data(
    user_data_id BIGSERIAL PRIMARY KEY,
    email_address TEXT NOT NULL,
    phone_number CHAR(11) NOT NULL,
    password_hash CHAR(33)  NOT NULL,
    modification_date DATE NOT NULL,
    join_date DATE NOT NULL
);

DO $$ BEGIN
    CREATE TYPE LEVEL AS ENUM ('low','mid','high');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS caretaker(
    caretaker_id BIGSERIAL PRIMARY KEY,
    verified BOOLEAN NOT NULL,
    car_owner BOOLEAN
);

CREATE TABLE IF NOT EXISTS donor(
    donor_id BIGSERIAL NOT NULL PRIMARY KEY,
    donations_sum FLOAT NOT NULL,
    points INT NOT NULL
);

CREATE TABLE IF NOT EXISTS help_group(
    help_group_id BIGSERIAL NOT NULL PRIMARY KEY,
    monetary_goal FLOAT,
    finish_date DATE NOT NULL,
    poverty_level LEVEL NOT NULL,
    help_group_caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id) on delete cascade on update cascade
);

CREATE TABLE IF NOT EXISTS product(
    product_id BIGSERIAL PRIMARY KEY,
    kind VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS needs(
    needs_id BIGSERIAL PRIMARY KEY,
    count INT NOT NULL,
    needs_help_group_ref_id BIGINT REFERENCES help_group(help_group_id) on delete cascade on update cascade,
    needs_products_ref_id BIGINT REFERENCES product(product_id) on delete cascade on update cascade
);

CREATE TABLE IF NOT EXISTS donation(
    donation_id BIGSERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    amount FLOAT NOT NULL,
    note TEXT NOT NULL,
    donation_donor_ref_id BIGINT REFERENCES donor(donor_id) on delete cascade on update cascade,
    donation_help_group_ref_id BIGINT REFERENCES help_group(help_group_id) on delete cascade on update cascade NULL 
);

CREATE TABLE IF NOT EXISTS person(
    person_id BIGSERIAL PRIMARY KEY,
    pesel CHAR(11),
    forename TEXT NOT NULL,
    surname TEXT NOT NULL,
    address TEXT,
    birth DATE,
    person_donor_ref_id BIGINT REFERENCES donor(donor_id) on delete cascade on update cascade,
    person_help_group_ref_id BIGINT REFERENCES help_group(help_group_id) on delete cascade on update cascade,
    person_caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id) on delete cascade on update cascade UNIQUE,
    person_user_data_ref_id BIGINT REFERENCES user_data(user_data_id) on delete cascade on update cascade UNIQUE
);