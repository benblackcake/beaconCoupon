INSERT INTO beacno_test.user_behavior( user_id, path_to_coupon_image_url_link,user_click_coupon_time) VALUES (3,'http://bit.ly/2yOJri4',0)
ON DUPLICATE KEY UPDATE user_click_coupon_time=user_click_coupon_time+1;

/* UPDATE beacno_test.user_behavior SET user_click_coupon_time=user_click_coupon_time+1 WHERE path_to_coupon_image_url_link='http://bit.ly/2yOJri4'; */


INSERT INTO beacno_test.collect_list ( user_id, path_to_coupon_image_url_link) VALUES (2,'http://bit.ly/2OBd80O')
ON DUPLICATE KEY UPDATE path_to_coupon_image_url_link=path_to_coupon_image_url_link;

create unique index user_name_idx on yourtable (1,2);
/*could have two coulumn to constraint*/
/* create unique index user_id_idx on collect_list (user_id);*/

SELECT  t.id,t.path_to_coupon_image_url_link, s.user_id,s.coupon_name, s.coupon_content,s.coupon_dismoney,s.coupon_s_time,s.coupon_e_time 
FROM beacno_test.collect_list t INNER JOIN beacno_test.coupon_list s 
ON ( t.path_to_coupon_image_url_link = s.path_to_coupon_image_url_link ) WHERE t.user_id=2 AND  CURDATE() >=coupon_s_time AND CURDATE()<=coupon_e_time ;