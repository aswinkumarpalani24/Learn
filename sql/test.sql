SELECT region, SUM(amount) 
FROM orders 
GROUP BY region;
