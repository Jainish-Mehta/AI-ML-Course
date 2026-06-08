Create Table IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name Text not null,
    last_name Text not null,
    email Text not null unique,
    role Text default 'customer',
    account_balance Real default 0.0
);

Insert into users(first_name,last_name,email,role,account_balance)
values('john','alex','aj@gmail.com','admin',500),
('Elon','musk','em@gmail.com','customer',1000),
('Bill','gates','bg@gmail.com','Businessman',1500);