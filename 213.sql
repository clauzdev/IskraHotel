select photo from customer_customer where user_id = (select id from authentication_user where username = 'nowebcam10')