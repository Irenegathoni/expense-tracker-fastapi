CREATE TABLE expenses(
  id SERIAL PRIMARY KEY,
  description VARCHAR(255) NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  category VARCHAR(100) NOT NULL,
  date DATE NOT NULL
  );

SELECT * FROM expenses;

CREATE TABLE budgets(
  id SERIAL PRIMARY KEY,
  category VARCHAR(100) UNIQUE NOT NULL,
  monthly_limit DECIMAL(10,2) NOT NULL
);

INSERT INTO budgets(category,monthly_limit) VALUES
(art-work,5000),
(music)
  