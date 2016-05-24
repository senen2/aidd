'''
Created on 20/05/2016

@author: botpi

SELECT * FROM districts
INNER JOIN districts_poi 
ON districts_poi.district_id = districts.district_id
AND districts_poi.district_hash = districts.district_hash

'''
