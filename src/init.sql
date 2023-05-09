CREATE TABLE IF NOT EXISTS user_data(
    user_data_id BIGSERIAL PRIMARY KEY,
    email_address TEXT NOT NULL,
    phone_number CHAR(11) NOT NULL,
    password_hash CHAR(33) NOT NULL,
    modification_date DATE NOT NULL,
    join_date DATE NOT NULL

);

CREATE TABLE IF NOT EXISTS caretaker(
    caretaker_id BIGSERIAL PRIMARY KEY,
    donation_place TEXT NOT NULL,
    car_owner BOOLEAN NOT NULL,
    active_hours_start TIME NOT NULL,
    active_hours_end TIME NOT NULL
);


CREATE TABLE IF NOT EXISTS help_group(
    help_group_id BIGSERIAL NOT NULL PRIMARY KEY,
    poverty_level INT,
    help_group_caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id)
);

CREATE TABLE IF NOT EXISTS product(
    product_id BIGSERIAL PRIMARY KEY,
    kind VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS needs(
    needs_id BIGSERIAL PRIMARY KEY,
    count INT NOT NULL,
    needs_help_group_ref_id BIGINT REFERENCES help_group(help_group_id),
    needs_products_ref_id BIGINT REFERENCES product(product_id)

);

CREATE TABLE IF NOT EXISTS donor(
    donor_id BIGSERIAL NOT NULL PRIMARY KEY,
    pack_count INT NOT NULL,
    donations_sum money NOT NULL,
    points INT NOT NULL,
    donor_help_group_ref_id BIGINT REFERENCES help_group(help_group_id)
);
CREATE TABLE IF NOT EXISTS donations(
    donations_id BIGSERIAL PRIMARY KEY,
    "date" DATE NOT NULL,
    note TEXT NOT NULL,
    donations_donor_ref_id BIGINT REFERENCES donor(donor_id),
    donations_help_group_ref_id BIGINT REFERENCES help_group(help_group_id) NULL
);

CREATE TABLE IF NOT EXISTS person(
    person_id BIGSERIAL PRIMARY KEY,
    pesel CHAR(11) NOT NULL,
    forename TEXT NOT NULL,
    surname TEXT NOT NULL,
    address TEXT NOT NULL,
    birth DATE NOT NULL,
    person_donor_ref_id BIGINT REFERENCES donor(donor_id),
    person_help_group_ref_id BIGINT REFERENCES help_group(help_group_id),
    person_caretaker_ref_id BIGINT REFERENCES caretaker(caretaker_id) UNIQUE,
    person_user_data_ref_id BIGINT REFERENCES user_data(user_data_id) UNIQUE
);
