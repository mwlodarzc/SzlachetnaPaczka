CREATE TABLE IF NOT EXISTS caretaker(
    caretaker_id BIGSERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS help_group(
    help_group_id BIGSERIAL NOT NULL PRIMARY KEY,
    caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id),
    poverty_level INT
);

CREATE TABLE IF NOT EXISTS donor(
    donor_id BIGSERIAL NOT NULL PRIMARY KEY,
    help_group_ref_id BIGINT REFERENCES help_group(help_group_id),
    pack_count INT NOT NULL,
    donations_sum money NOT NULL,
    points INT
);

CREATE TABLE IF NOT EXISTS user_data(
    user_data_id BIGSERIAL PRIMARY KEY,
    email_address TEXT,
    password_hash CHAR(33),
    phone_number CHAR(11),
    modification_date DATE
);

CREATE TABLE IF NOT EXISTS person(
    person_id BIGSERIAL PRIMARY KEY,
    pesel CHAR(11) NOT NULL,
    forename TEXT NOT NULL,
    surname TEXT NOT NULL,
    address TEXT NOT NULL,
    birth DATE NOT NULL,
    donor_ref_id BIGINT REFERENCES donor(donor_id),
    help_group_ref_id BIGINT REFERENCES help_group(help_group_id),
    caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id),
    user_data_ref_id BIGINT REFERENCES user_data(user_data_id)
);