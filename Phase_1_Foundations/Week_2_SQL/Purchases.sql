-- PRAGMA foreign_keys = ON;
-- DROP TABLE IF EXISTS purchases;
-- CREATE TABLE IF NOT EXISTS purchases(
--     purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
--     user_id INTEGER NOT NULL,
--     product_id INTEGER NOT NULL,
    
--     purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

--     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
--     FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
    -- ON DELETE CASCADE is for deleting the purchases if the user is deleted
-- );


-- DELETE FROM purchases;

-- Insert into purchases(user_id, product_id)
-- values(1, 1),
-- (1, 2),
-- (2, 3),
-- (2, 4),
-- (3, 5),
-- (3, 6),
-- (1, 7),
-- (2, 8),
-- (3, 9),
-- (1, 1),
-- (2, 2),
-- (1, 3),
-- (3, 4),
-- (5, 5),
-- (4, 6),
-- (4, 7),
-- (3, 8),
-- (1, 9);
-- insert into purchases(user_id, product_id)
-- values(5, 23),
-- (8, 23),
-- (6, 5),
-- (9, 16),
-- (3, 7),
-- (8, 18),
-- (9, 9),
-- (10, 13);