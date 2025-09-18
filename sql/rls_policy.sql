```sql
Create FUNCTION curated.fn_securitypredicate(@Region AS VARCHAR(50))
RETURNS TABLE
WITH SCHEMABINDING
AS
RETURN
SELECT 1 AS fn_securitypredicate  --won't recognize if you don't give As
WHERE EXISTS (
    SELECT 1
    FROM curated.user_region_map urm
    WHERE urm.user_principal_name = USER_NAME()
      AND urm.region = @Region
);

CREATE SECURITY POLICY curated.SalesRLS
ADD FILTER PREDICATE curated.fn_securitypredicate(region)
ON curated.v_sales_secure
WITH (STATE = ON);
```
