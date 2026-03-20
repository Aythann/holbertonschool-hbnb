PRAGMA foreign_keys = ON;

INSERT INTO users (
    id,
    first_name,
    last_name,
    email,
    password,
    is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2y$12$bhMMBsVaXwu4fqTuN8W17excHyasOtBXr4dwOcXR4UiXQnHLp3gDy',
    TRUE
);

INSERT INTO amenities (id, name) VALUES
    ('11111111-1111-4111-8111-111111111111', 'WiFi'),
    ('22222222-2222-4222-8222-222222222222', 'Swimming Pool'),
    ('33333333-3333-4333-8333-333333333333', 'Air Conditioning');
