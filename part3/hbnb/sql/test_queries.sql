PRAGMA foreign_keys = ON;

SELECT name
FROM sqlite_master
WHERE type = 'table';

SELECT * FROM users;
SELECT * FROM amenities;

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin,
    created_at,
    updated_at
) VALUES (
    '44444444-4444-4444-8444-444444444444',
    'John',
    'Doe',
    'john.doe@example.com',
    '$2y$12$bhMMBsVaXwu4fqTuN8W17excHyasOtBXr4dwOcXR4UiXQnHLp3gDy',
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO places (
    id,
    title,
    description,
    price,
    latitude,
    longitude,
    owner_id,
    created_at,
    updated_at
) VALUES (
    '55555555-5555-4555-8555-555555555555',
    'Cozy Apartment',
    'Nice place in city center',
    120.00,
    48.8566,
    2.3522,
    '44444444-4444-4444-8444-444444444444',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO reviews (
    id,
    text,
    rating,
    user_id,
    place_id,
    created_at,
    updated_at
) VALUES (
    '66666666-6666-4666-8666-666666666666',
    'Great place!',
    5,
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    '55555555-5555-4555-8555-555555555555',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO place_amenity (
    place_id,
    amenity_id
) VALUES
    ('55555555-5555-4555-8555-555555555555', '11111111-1111-4111-8111-111111111111'),
    ('55555555-5555-4555-8555-555555555555', '33333333-3333-4333-8333-333333333333');

SELECT * FROM places;
SELECT * FROM reviews;
SELECT * FROM place_amenity;

UPDATE places
SET title = 'Luxury Apartment',
    updated_at = CURRENT_TIMESTAMP
WHERE id = '55555555-5555-4555-8555-555555555555';

SELECT * FROM places
WHERE id = '55555555-5555-4555-8555-555555555555';

DELETE FROM reviews
WHERE id = '66666666-6666-4666-8666-666666666666';

SELECT * FROM reviews;