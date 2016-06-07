'''
Created on 20/05/2016

@author: botpi

SELECT * FROM districts
INNER JOIN districts_poi 
ON districts_poi.district_id = districts.district_id
AND districts_poi.district_hash = districts.district_hash

INSERT INTO results (district_id, DATE, slot) SELECT district_id, DATE, slot FROM results0, districts

SELECT file_train, file_test, hiddens, inputs, AVG(score) FROM score GROUP BY file_train, file_test, hiddens, inputs

SELECT AVG(ABS(results.gap - gaps.gap) / gaps.gap) AS n
FROM results
INNER JOIN diditest.gaps AS gaps 
    ON gaps.district_id=results.district_id
    AND gaps.date=results.date
    AND gaps.slot=results.slot
WHERE gaps.gap>0
-------------------------------------------------
INSERT INTO passengers (HASH) SELECT passenger_id FROM orders_full GROUP BY passenger_id;
INSERT INTO orders_unique (HASH) SELECT order_id FROM orders_full GROUP BY order_id;
INSERT INTO drivers (HASH) SELECT driver_id FROM orders_full GROUP BY driver_id;
INSERT INTO destinations (HASH) SELECT dest_district_hash FROM orders_full GROUP BY dest_district_hash;

INSERT INTO orders (order_id, district_id, dest_id, passenger_id, driver_id, DATETIME, DATE, slot, answer)
SELECT orders_unique.id, districts.district_id,  destinations.id, passengers.id, drivers.id, orders_full.datetime, orders_full.date, orders_full.slot, orders_full.answer
FROM orders_full
    INNER JOIN orders_unique ON orders_unique.hash=orders_full.order_id
    INNER JOIN passengers ON passengers.hash=orders_full.passenger_id
    INNER JOIN destinations ON destinations.hash=orders_full.dest_district_hash
    INNER JOIN districts ON districts.district_hash=orders_full.start_district_hash
    LEFT JOIN drivers ON drivers.hash=orders_full.driver_id




-------------------------------------------------
DROP TABLE IF EXISTS x2;
CREATE TABLE x2
SELECT gaps.district_id, AVG(ABS(results.gap - gaps.gap) / gaps.gap) AS n, SUM(gaps.gap) AS gap, SUM(results.gap) AS s
FROM results_test_roma as results
INNER JOIN diditest.gaps AS gaps 
    ON gaps.district_id=results.district_id
    AND gaps.date=results.date
    AND gaps.slot=results.slot
WHERE gaps.gap>0
GROUP BY gaps.district_id;

SELECT AVG(n) FROM x2;
-------------------------------------------
DROP TABLE IF EXISTS x2;
CREATE TABLE x2
SELECT district_id, AVG(ABS(gap - s) / gap) AS n, SUM(gap) AS gap, SUM(s) AS s
FROM results
WHERE gap>0
GROUP BY district_id

SELECT AVG(n) FROM x2

------------------------------------------------------
UPDATE gaps 
    INNER JOIN didi.gaps AS hist 
        ON hist.district_id=gaps.district_id
        AND hist.date=gaps.datetest
        AND hist.slot=gaps.slot
SET gaps.s = hist.gap

SELECT * FROM gaps 
    INNER JOIN didi.gaps AS hist 
        ON hist.district_id=gaps.district_id
        AND hist.date=gaps.datetest
        AND hist.slot=gaps.slot

------------------------------------------------
SELECT district_id, DATE, FLOOR((slot-1)/6)+1 AS h, SUM(demand) AS demand, SUM(supply) AS supply
FROM gaps
GROUP BY district_id, DATE, h

--------------------------------------------------------
UPDATE results_test AS results
    INNER JOIN diditest.gaps AS hist
        ON hist.district_id=results.district_id
        AND hist.date = results.date
        AND hist.slot = results.slot
SET results.gap = hist.gap

UPDATE results_test SET gap = 1

-------------------------------------------------------
CREATE TABLE x2
SELECT district_id, COUNT(1) AS passengers, SUM(orders) AS orders FROM orders_pass GROUP BY district_id

UPDATE districts
    INNER JOIN x2 ON x2.district_id=districts.district_id
SET districts.passengers = x2.passengers, districts.orders = x2.orders

---------------------------------------------------------
create table maxims
SELECT district_id, passenger_id, COUNT(1) AS passengers FROM orders GROUP BY district_id, passenger_id

UPDATE districts
    INNER JOIN maxims ON maxims.district_id=districts.district_id
SET districts.demand = maxims.demand, districts.supply = maxims.supply
-----------------------------------------------------------
CREATE TABLE x2
SELECT district_id, COUNT(1) AS drivers, SUM(orders) AS answers FROM answers WHERE driver_id>0 GROUP BY district_id

UPDATE districts
    INNER JOIN x2 ON x2.district_id=districts.district_id
SET districts.drivers = x2.drivers, districts.answers = x2.answers
-----------------------------------------------------------
DROP TABLE x1;
CREATE TABLE x1 SELECT district_id, MIN(score) AS score FROM districts_score GROUP BY district_id;
SELECT AVG(score) FROM x1;

----------------------------------------------------



'''

