'''
Created on 20/05/2016

@author: botpi

SELECT * FROM districts
INNER JOIN districts_poi 
ON districts_poi.district_id = districts.district_id
AND districts_poi.district_hash = districts.district_hash

INSERT INTO results (district_id, DATE, slot) SELECT district_id, DATE, slot FROM results0, districts

SELECT file_train, file_test, hiddens, inputs, epochs, AVG(score),COUNT(score) 
FROM score 
GROUP BY file_train, file_test, hiddens, inputs, epochs
'''
