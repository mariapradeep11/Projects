Solution Strategy 

 

Note: JSON formatting was off, and I had to check the validity of the JSON provided and fix it before starting with the interpretation 

 

Interpreting the JSON Structure 

 

There are three financial categories in the JSON: assets, liabilities, and equity. 

All three categories are parent-child hierarchical in nature. 

There is account_id in some accounts and null in others (to denote roll-up categories). 

 

Creating the Relational Schema 

 

Employed a self-referencing accounts table to preserve hierarchy. 

Designed a categories table to classify accounts (e.g., Current Assets, Fixed Assets). 

Added a transactions table to record financial activity (not in JSON, but helpful to audit changes). 

 

Validating Roll-Ups 

 

Utilized SQL queries to determine if parent account values match the sum of their children. 

 

 

Assumptions Made 

 

✔ Account IDs are unique when present → If account_id is null, then it is a roll-up category. 

✔ Expected balance (value) is authoritative → Parent account balances are equal to the sum of child accounts. 

✔ No transactions in JSON explicitly → Added a transactions table for future use. 

✔ All accounts are part of the three top-level categories: ASSETS, LIABILITIES, EQUITY. 

 

Issues & Inconsistencies Found 

 

Some Parent Accounts Have null account_id 

 

Makes it difficult to reference them uniquely in a relational database. 

Solution: Utilized self-referencing parent_account_id to preserve structure. 

 

Floating-Point Precision Errors in Summation 

 

Parent values occasionally varied slightly from children sum. 

Solution: Applied SQL rounding methods to reduce discrepancies. 

 

Liabilities Section Contains a Big Missing Amount 

 

Our calculated total for Current Liabilities was 935,489.03 off, which is missing information. 

 

 

Next Steps If More Time Were Available 

 

Build Data Ingestion Pipeline -  
 
I would create an airflow dag that would validate and store the validated json files in an s3 bucket 

From the s3 bucket I would ingest the data into a warehouse preferably snowflake 

I would flatten these json files and create a dbt model with three base models for accounts, categories and transactions 

Join these models in the staging as required and create respective intermediate models and mart level models  

These dbt models enable you to write generic, custom and unit tests for these – which increases the trust of the stakeholders towards making informed decisions 

These mart level models would be exposed to a BI Layer preferably Sigma/Looker or Tableau from where the stakeholders can stay up to date and make decisions that align with the greater business goals 

I would have communicated with the respective stakeholders/customers to investigate Missing Liability Amounts → Determine where 935,489.03 is missing. 

Improve Transaction Tracking → Add real-world transaction imports to monitor changes over time. 
