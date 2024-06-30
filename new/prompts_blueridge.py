prompt_text_2_sql = """<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Generate a SQL query to answer this question: `{question}`

DDL statements:

CREATE TABLE df(
Type VARCHAR(30), -- type of the product in inventory
Location Name VARCHAR(70), -- location of the supplier
Buyer   VARCHAR(70),  -- Name of the Buyer
Supplier VARCHAR(100), --Name of the supplier
Product Code  VARCHAR(100), -- Code of the Product that is getting shipped
Product Description VARCHAR(200), -- Description of the Product that is getting shipped
[5/24/2024]	INTEGER,  -- Quantity of stock shipped in May
[6/1/2024] INTEGER,  -- Quantity of stock shipped in June
[7/1/2024]	INTEGER,  -- Quantity of stock shipped in July
[8/1/2024] INTEGER,  -- Quantity of stock shipped in August
);

Metadata:
Type: Type of the product in inventory -- this can have values like "Backorder", "Days on Hand" ,"Demand History" ,"Demand Variance" ,"On Hand", "On Order" ,"Purchases" ,"Receipts" ,"Sales"

Location Name: Location of the supplier
Buyer: Name of the Buyer
Supplier: Name of the supplier
Product Code: Code of the Product that is getting shipped
Product Description: Description of the Product that is getting shipped <|eot_id|><|start_header_id|>assistant<|end_header_id|>


Few Examples
1. total quantity of products in backorder in the month of may - SELECT SUM("[5/24/2024]") AS total_quantity from df where Type='Backorder'
2. What is the total quantity of  all the products on hand  in the  month of june - SELECT SUM([6/1/2024]) AS total_quantity from df where Type='On Hand'


Few Examples that are directly useful but they are written in Pandas for your help:-
1. Filter Data:
   Example: SELECT * FROM df WHERE "Product Code" = 'RWG4010L';

2. Aggregate Data:
   Example: SELECT SUM("[5/24/2024]") FROM df WHERE "Product Code" = 'RWG4010L' AND "Type" = 'Backorder';


4. Combine Conditions:
   Example: SELECT SUM("[5/24/2024]") FROM df WHERE "Product Code" LIKE '%RWG%' AND "Type" = 'Backorder';

5. Pattern in Codes for Sizes:
   Example: 'RWG4010L' - 'RWG' is the prefix, '4010' is the model, 'L' indicates the size (Large).

6. Relate Codes to EXACT Descriptions:
   Example: SELECT SUM("[5/24/2024]") FROM df  WHERE "Product Code" LIKE '%S$%'  AND "Product Description" LIKE '%Keystone Thumb%' AND "Type" = 'Backorder';



7. Days on Hand:
   Example: SELECT * FROM df WHERE "Type" = 'Days on Hand';

8. On Hand vs. Days on Hand:
   - On Hand: Refers to a Type column with a value of "On Hand".
   - Days on Hand: Refers to a Type column with a value of "Days on Hand".
   Example: SELECT * FROM df WHERE "Type" = 'On Hand' AND "Type" = 'Days on Hand';

9. Calculate projected stock for :
   Example: RWG4121L for June 2024 = On Hand + On Order + Receipts - Sales
   Example code = SELECT (SELECT SUM("[6/1/2024]") FROM df WHERE "Product Code" = 'RWG4121L' AND "Type" IN ('On Hand', 'On Order', 'Receipts')) - (SELECT SUM("[6/1/2024]") FROM df WHERE "Product Code" = 'RWG4121L' AND "Type" IN ('Sales')) AS result;


11. Handling Product Codes and Sizes:
    Identify patterns: 'L' = Large, 'XL' = Extra Large, 'XXL' = Double Extra Large.

  Example - Large Driver On Hand Calculation:
  Calculate total "Large Driver" items On Hand for May 2024:
  SELECT SUM("[5/24/2024]")
  FROM df
  WHERE "Type" = 'On Hand'
  AND "Product Description" LIKE '%Driver%'
  AND "Product Code" LIKE '%L'
  AND "Product Code" NOT LIKE '%XL'
  AND "Product Code" NOT LIKE '%XXL';


The following SQL query best answers the question `{question}`:
```sql
"""