DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id bigserial PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT,
    balance INTEGER NOT NULL,
    headshot TEXT,
    first_name TEXT,
    last_name TEXT,
    bio TEXT,
    phone_number TEXT
);
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS listings;
CREATE TABLE listings (
    id bigserial PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    price INTEGER NOT NULL,
    category TEXT NOT NULL,
    size TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL,
    pickup_location TEXT,
    likes INTEGER
);
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS likes;
CREATE TABLE likes (
    id bigserial PRIMARY KEY,
    user_id INTEGER NOT NULL,
    listing_id INTEGER NOT NULL
);
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS images;
CREATE TABLE images (
    id bigserial PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    is_primary BOOLEAN NOT NULL,
    img_url TEXT NOT NULL,
    cloudinary_id TEXT NOT NULL
);
------------------------------------------------------------------------
DROP TABLE IF EXISTS availabilities;
CREATE TABLE availabilities (
    id bigserial PRIMARY KEY,
    listing_id INTEGER,
    transaction_id INTEGER,
    borrower_userid INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS transactions;
CREATE TABLE transactions (
    id bigserial PRIMARY KEY,
    listing_id INTEGER NOT NULL,
    to_user_id INTEGER,
    from_user_id INTEGER NOT NULL,
    date_created DATE,
    status TEXT,
    request_msg TEXT,
    date_lent_out DATE,
    date_returned DATE
);
----------------------------------------------------------------------
DROP TABLE IF EXISTS notifications;
CREATE TABLE notifications (
    id bigserial PRIMARY KEY,
    notif_type TEXT NOT NULL,
    listing_id INTEGER NOT NULL,
    to_user_id INTEGER NOT NULL,
    from_user_id INTEGER NOT NULL,
    date_created DATE NOT NULL,
    transaction_id INTEGER NOT NULL,
    msg TEXT,
    time_created TIME NOT NULL
);
----------------------------------------------------------------------
DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
    id bigserial PRIMARY KEY,
    rating INTEGER NOT NULL,
    user_rated_id INTEGER NOT NULL,
    user_rating_id INTEGER NOT NULL,
    date_rated DATE NOT NULL,
    transaction_id INTEGER NOT NULL,
    msg TEXT NOT NULL,
    rated_is_borrower BOOLEAN NOT NULL
);
----------------------------------------------------------------------


----------------------------------------------------------------------

-- INSERT INTO users (username, email, address, balance, headshot)
-- VALUES
--     ('alice123', 'alice@example.com', '123 Main St, Anytown USA', 500, 'https://example.com/headshots/alice.jpg'),
--     ('bob456', 'bob@example.com', '456 Elm St, Anytown USA', 1000, 'https://example.com/headshots/bob.jpg'),
--     ('charlie789', 'charlie@example.com', '789 Oak St, Anytown USA', 750, 'https://example.com/headshots/charlie.jpg');


-- INSERT INTO listings (user_id, name, price, category, size, subcategory, description, status, pickup_location, likes)
-- VALUES
--     (1, 'Floral maxi dress', 30, 'Dresses', 'Medium', 'Maxi', 'Beautiful floral maxi dress, perfect for summer weddings!', 'Available', '123 Main St, Anytown USA', 0),
--     (2, 'Red cocktail dress', 40, 'Dresses', 'Small', 'Cocktail', 'Elegant red cocktail dress, great for parties!', 'Available', NULL, 0),
--     (3, 'Black blazer', 20, 'Jackets & Blazers', 'Medium', 'Blazers', 'Classic black blazer, perfect for job interviews!', 'Rented', '789 Oak St, Anytown USA', 0),
--     (1, 'Blue striped shirt', 15, 'Tops', 'Small', 'Button-Up', 'Casual blue striped shirt, great for everyday wear!', 'Available', '123 Main St, Anytown USA', 0),
--     (2, 'Distressed jeans', 25, 'Bottoms', 'Medium', 'Jeans', 'Fashionable distressed jeans, perfect for a night out!', 'Available', NULL, 0);


-- -- INSERT INTO liked_posts (user_id, listing_id)
-- -- VALUES
-- --     (1, 2),
-- --     (2, 1),
-- --     (3, 3),
-- --     (1, 5),
-- --     (2, 3);


-- INSERT INTO images (listing_id, is_primary, img_url, cloudinary_id)
-- VALUES
--     (1, true, 'https://example.com/images/floral_maxi_dress.jpg', '1_0'),
--     (2, true, 'https://example.com/images/red_cocktail_dress.jpg', '3_0'),
--     (3, true, 'https://example.com/images/black_blazer.jpg', 'jkl012'),
--     (4, true, 'https://example.com/images/blue_striped_shirt.jpg', 'mno345'),
--     (5, true, 'https://example.com/images/distressed_jeans.jpg', 'pqr678');


-- INSERT INTO availabilities (listing_id, transaction_id, borrower_userid, start_date, end_date)
-- VALUES
--     (1, NULL, NULL, '2023-05-01', '2023-05-07'),
--     (1, NULL, NULL, '2023-06-01', '2023-06-07'),

