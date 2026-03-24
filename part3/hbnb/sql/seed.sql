PRAGMA foreign_keys = ON;

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
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2y$12$bhMMBsVaXwu4fqTuN8W17excHyasOtBXr4dwOcXR4UiXQnHLp3gDy',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

INSERT INTO amenities (
    id,
    name,
    created_at,
    updated_at
) VALUES
    (
        '11111111-1111-4111-8111-111111111111',
        'WiFi',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        '22222222-2222-4222-8222-222222222222',
        'Swimming Pool',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    ),
    (
        '33333333-3333-4333-8333-333333333333',
        'Air Conditioning',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    );