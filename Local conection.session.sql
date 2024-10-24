use  bsai23004;

CREATE TABLE IF NOT EXISTS Manufacturer (
    manufacturer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    contact VARCHAR(50)
);



CREATE TABLE IF NOT EXISTS Salt (
    salt_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    prescription BOOLEAN,
    max_qty INT
);

CREATE TABLE IF NOT EXISTS Medicine (
    medicine_id INT PRIMARY KEY AUTO_INCREMENT,
    manufacturer_id INT,
    salt_id INT,
    name VARCHAR(255) NOT NULL,
    safe_stock INT,
    FOREIGN KEY (manufacturer_id) REFERENCES Manufacturer(manufacturer_id),
    FOREIGN KEY (salt_id) REFERENCES Salt(salt_id)
);

CREATE TABLE IF NOT EXISTS Supplier (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    return_policy_id INT,
    bonus_scheme_id INT,
    contact_number VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    medicine_id INT,
    batch_id INT,
    quantity INT,
    mfg_date DATE,
    exp_date DATE,
    supplier_id INT,
    buying_price DECIMAL(10, 2),
    selling_price DECIMAL(10, 2),
    tax DECIMAL(5, 2),
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

CREATE TABLE IF NOT EXISTS Return_policy (
    return_policy_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT,
    thresh_days INT,
    pickup BOOLEAN,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

CREATE TABLE IF NOT EXISTS Bonus_scheme (
    bonus_scheme_id INT PRIMARY KEY AUTO_INCREMENT,
    supplier_id INT NOT NULL,
    medicine_id INT,
    min_qty INT,
    bonus INT,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
    FOREIGN KEY (medicine_id) REFERENCES Medicine(medicine_id)
);

CREATE TABLE IF NOT EXISTS Returns (
    return_id INT PRIMARY KEY AUTO_INCREMENT,
    inventory_id INT,
    supplier_id INT,
    start_date DATE,
    complete_date DATE,
    complete BOOLEAN,
    return_qty INT,
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
);

CREATE TABLE IF NOT EXISTS Customer (
    name VARCHAR(255) NOT NULL,
    contact_no VARCHAR(50) NOT NULL,
    type VARCHAR(50),
    address TEXT,
    last_purchase_date DATE,
    PRIMARY KEY (name, contact_no)
);

CREATE TABLE IF NOT EXISTS Bill (
    bill_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    contact_no VARCHAR(50),
    inventory_id INT,
    quantity INT,
    amount DECIMAL(10, 2),
    paid DECIMAL(10, 2),
    pending DECIMAL(10, 2),
    date DATE,
    discount DECIMAL(5, 2),
    legal BOOLEAN,
    FOREIGN KEY (name, contact_no) REFERENCES Customer(name, contact_no),
    FOREIGN KEY (inventory_id) REFERENCES Inventory(inventory_id)
);


-- Insert into Manufacturer
INSERT INTO Manufacturer (name, address, contact) 
VALUES ('Pfizer', '123 Pharma St, NY', '555-12345'),
       ('Moderna', '456 Bio Lane, SF', '555-67890'),
       ('AstraZeneca', '789 Health Ave, London', '555-24680');

-- Insert into Salt
INSERT INTO Salt (name, prescription, max_qty) 
VALUES ('Paracetamol', TRUE, 10),
       ('Ibuprofen', TRUE, 15),
       ('Vitamin C', FALSE, 5);

-- Insert into Medicine
INSERT INTO Medicine (manufacturer_id, salt_id, name, safe_stock) 
VALUES (1, 1, 'Tylenol', 100),
       (2, 2, 'Advil', 150),
       (3, 3, 'Cenovis', 200);

-- Insert into Supplier
INSERT INTO Supplier (name, return_policy_id, bonus_scheme_id, contact_number) 
VALUES ('MedSupply Co.', 1, 1, '555-87654'),
       ('HealthDistributors', 2, 2, '555-54321'),
       ('PharmaLogistics', 3, 3, '555-11223');

-- Insert into Inventory
INSERT INTO Inventory (medicine_id, batch_id, quantity, mfg_date, exp_date, supplier_id, buying_price, selling_price, tax) 
VALUES (1, 101, 500, '2023-01-15', '2025-01-14', 1, 5.50, 8.99, 7.5),
       (2, 102, 300, '2023-02-20', '2025-02-19', 2, 4.00, 6.50, 5.0),
       (3, 103, 250, '2023-03-25', '2025-03-24', 3, 3.00, 5.75, 3.5);

-- Insert into Return_policy
INSERT INTO Return_policy (supplier_id, thresh_days, pickup) 
VALUES (1, 30, TRUE),
       (2, 60, FALSE),
       (3, 45, TRUE);

-- Insert into Bonus_scheme
INSERT INTO Bonus_scheme (supplier_id, medicine_id, min_qty, bonus) 
VALUES (1, 1, 100, 10),
       (2, 2, 200, 20),
       (3, 3, 150, 15);

-- Insert into Returns
INSERT INTO Returns (inventory_id, supplier_id, start_date, complete_date, complete, return_qty) 
VALUES (1, 1, '2024-01-01', '2024-01-10', TRUE, 50),
       (2, 2, '2024-02-01', '2024-02-12', FALSE, 30),
       (3, 3, '2024-03-01', '2024-03-20', TRUE, 40);

-- Insert into Customer
INSERT INTO Customer (name, contact_no, type, address, last_purchase_date) 
VALUES ('Jobonus_schemehn Doe', '555-99887', 'Walk-in', '123 Elm St, NY', '2024-01-15'),
       ('Jane Smith', '555-66789', 'Regular', '456 Oak St, SF', '2024-02-20'),
       ('Bob Johnson', '555-33579', 'VIP', '789 Pine St, London', '2024-03-10');

-- Insert into Bill
INSERT INTO Bill (name, contact_no, inventory_id, quantity, amount, paid, pending, date, discount, legal) 
VALUES ('John Doe', '555-99887', 1, 10, 89.90, 89.90, 0.00, '2024-01-16', 5.0, TRUE),
       ('Jane Smith', '555-66789', 2, 5, 32.50, 20.00, 12.50, '2024-02-21', 2.0, FALSE),
       ('Bob Johnson', '555-33579', 3, 15, 86.25, 86.25, 0.00, '2024-03-11', 10.0, TRUE);
