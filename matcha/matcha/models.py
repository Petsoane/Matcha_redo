import pymysql.cursors
from datetime import datetime


class DB:

    def __init__(self):
        # self._client = pymysql.connect(
        #     host="batqsrt7tpzxycby0eop-mysql.services.clever-cloud.com",
        #     user="uhuohws2whgbdpjw",
        #     password="zgEvEA8In6Xpa0Qjkv6o",
        #     db="batqsrt7tpzxycby0eop",
        #     charset="utf8mb4",
        #     cursorclass=pymysql.cursors.DictCursor,
        #     port=3306
        #     )

        self._client = pymysql.connect(
            host="localhost",
            user="root",
            password="password",
            db="matcha",
            # charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            # port=3306
            )


    def create_tables(self):
        users = """
        CREATE TABLE IF NOT EXISTS users (
            id INT NOT NULL AUTO_INCREMENT,
            username VARCHAR(200) NOT NULL,
            firstname VARCHAR(200) NOT NULL,
            lastname VARCHAR(200) NOT NULL,
            age INT NOT NULL,
            password VARCHAR (200) NOT NULL,
            image_name VARCHAR (200) DEFAULT 'default.png',
            email VARCHAR(200) NOT NULL,
            token VARCHAR(200) ,
            email_confirmed INT NOT NULL DEFAULT 0,
            PRIMARY KEY (id)
        )
        """
        user_info = """
        CREATE TABLE IF NOT EXISTS user_info (
            user_id INT,
            gender VARCHAR (200) DEFAULT 'female',
            sex VARCHAR (200) DEFAULT 'bisexual',
            likes INT NOT NULL DEFAULT 0,
            bio TEXT (800),
            interests TEXT (1000),
            fame_rating INT DEFAULT 0,
            latlon VARCHAR(400),
            last_seen DATETIME NOT NULL,
            location TEXT (1000),
            completed INT NOT NULL DEFAULT 0,

            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        courtship = """
        CREATE TABLE IF NOT EXISTS courtship (
            id INT NOT NULL AUTO_INCREMENT,
            courter_id INT ,
            courted_id INT ,
            matched INT NOT NULL DEFAULT 0,
            PRIMARY KEY (id),
            FOREIGN KEY (courter_id) REFERENCES users(id),
            FOREIGN KEY (courted_id) REFERENCES users(id)
        )
        """
        posts = """
        CREATE TABLE IF NOT EXISTS posts (
            id INT NOT NULL AUTO_INCREMENT,
            author INT,
            title VARCHAR (200) NOT NULL,
            content TEXT (800) NOT NULL,
            date_posted DATETIME NOT NULL,

            PRIMARY KEY (id),
            FOREIGN KEY (author) REFERENCES users(id)
        )
        """
        gallery = """
        CREATE TABLE IF NOT EXISTS gallery (
            poster INT,
            image_name VARCHAR (200) NOT NULL,
            FOREIGN KEY (poster) REFERENCES users(id)
        )
        """
        notifications = """
        CREATE TABLE IF NOT EXISTS notifications (
            id INT NOT NULL AUTO_INCREMENT,
            sender_id INT ,
            reciever_id INT ,
            content TEXT (200) NOT NULL,
            isRead INT NOT NULL DEFAULT 0,
            PRIMARY KEY (id),
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (reciever_id) REFERENCES users(id)
        )
        """

        blocked_users = """
        CREATE TABLE IF NOT EXISTS blocked_users (
            blocker_id INT,
            blocked_id INT,

            FOREIGN KEY (blocker_id) REFERENCES users(id),
            FOREIGN KEY (blocker_id) REFERENCES users(id)
        )
        """


        with self._client.cursor() as cursor:
            # Users table.
            cursor.execute(users)

        with self._client.cursor() as cursor:
            # info table.
            cursor.execute(user_info)

        with self._client.cursor() as cursor:
            # courtship table.
            cursor.execute(courtship)

        with self._client.cursor() as cursor:
            # ports tables.
            cursor.execute(posts)

        with self._client.cursor() as cursor:
            # gallery tables.
            cursor.execute(gallery)

        with self._client.cursor() as cursor:
            # notifications table.
            cursor.execute(notifications)

        with self._client.cursor() as cursor:
            # blocked_users table.
            cursor.execute(blocked_users)

        print("The table should have been created")


    # User Crud
    def register_user(self, details):
        sql = """
        INSERT INTO users (username, firstname, lastname, password, email, age)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        username = details['username']
        firstname = details['firstname']
        lastname = details['lastname']
        email = details['email']
        # email_confirmed = details['email_confirmed']
        password = details['password']
        age = details['age']

        self._exec_sql(sql, (username, firstname, lastname, password, email, age))

        # with self._client.cursor() as cursor:
        # 	cursor.execute(sql, (username, firstname, lastname, password, email, int(email_confirmed)))

        # self._client.commit()

    def get_user(self, query, fields=None):
        sql = """
        SELECT * from users where username = %s
        """
        q = ''

        if 'username' in query.keys():
            sql = """
            SELECT * from users where username = %s
            """
            q = query['username']
        elif 'email' in query.keys():
            sql = """
            SELECT * from users where email = %s
            """
            q = query['email']
        elif 'firstname' in query.keys():
            sql = """
            SELECT * from users where 'firstname' = %s
            """
            q = query['firstname']
        elif 'lastname' in query.keys():
            sql = """
            SELECT * from users where lastname = %s
            """
            q = query['lastname']
        elif 'id' in query.keys():
            sql = """
            SELECT * from users where id = %s
            """
            q = query['id']

        self.get_block_users(1)

        return self._exec_sql_ret(sql, (q,))

    def update_user(self, details):
        sql = """
        UPDATE users 
        SET username = %s,
            firstname = %s,
            lastname = %s,
            age = %s,
            password = %s,
            image_name = %s,
            email = %s
        WHERE id = %s
        """

        u_id = details['id']
        username = details['username']
        firstname = details['firstname']
        lastname = details['lastname']
        age = details['age']
        password = details['password']
        image_name = details['image_name']
        email = details['email']

        self._exec_sql(sql, (username, firstname, lastname, age, password, image_name, email, u_id))

    def delete_user(self, id):
        sql = """
        DELETE FROM users WHERE id = %s
        """
        self.delete_user_info(id)
        self._exec_sql(sql, (id,))

    def count_users(self):
        sql = """
        SELECT count(*) FROM users
        """

        return self._exec_sql_ret(sql)


    # User info
    def update_user_info(self, info, create=False):
        ''' Creates or updates the users information in the table '''
        sql = None

        if create:
            sql = '''
            INSERT INTO `user_info` (gender, sex, bio, interests, fame_rating, latlon, last_seen, location, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
        else:
            sql = '''
            UPDATE user_info
            SET gender = %s,
                sex  = %s,
                bio = %s,
                interests = %s,
                fame_rating = %s,
                latlon = %s,
                last_seen = %s,
                location  = %s,
            WHERE user_id = %s;

            '''
        print('[sql value]',sql)
        gender = info['gender']
        sex = info['sex']
        bio = info['bio']
        interests = info['interests']
        fame_rating = info['fame_rating']
        latlon = info['latlon']
        last_seen = info['last_seen']
        location = info['location']
        user_id = info['id']

        interests = ';'.join(interests)
        location = ';'.join(location)

        self._exec_sql(sql, (gender, sex, bio, interests, fame_rating, latlon, last_seen, location, user_id))

    def get_user_info(self, user_id):
        ''' Returns the specified users information 
            
            This should be called before the user is deleted to avoid orphaned data.
        '''
        sql = '''
        SELECT * FROM user_info WHERE user_id = %s
        '''
        result = self._exec_sql_ret(sql, (user_id,))

        result['interests'] = (result['interests']).split(';')
        result['location'] = (result['location']).split(';')

        return result

    def delete_user_info(self, user_id):
        ''' Deletes the specified users information '''
        sql = '''
        DELETE FROM user_info WHERE user_id = %s
        '''

        self._exec_sql(sql, (user_id,))

    def block_user(self, blocker_id, blocked_id):
        ''' Add both IDs to the table. '''
        sql = '''
        INSERT INTO blocked_users (blocker_id, blocked_id)
        VALUES (%s, %s)
        '''

        self._exec_sql(sql, (blocker_id, blocked_id))

    def get_block_users(self, blocker_id):
        sql = '''
        SELECT blocked_id FROM blocked_users WHERE blocker_id = %s
        '''

        print("Testing Blocked table", self._exec_sql_ret_all(sql, (blocker_id)), " End of test")
        

    def update_likes(self, user_id, new_count):
        sql = '''
        UPDATE user_info
        SET likes = %s
        WHERE user_id = %s
        '''

        self._exec_sql(sql, (new_count, user_id))



    # Posts
    def create_post(self, post):
        ''' Creates a post'''
        sql = '''
        INSERT INTO posts (author, title, content, date_posted)
        VALUES (%s, %s, %s, %s)
        '''

        title = post['title']
        content = post['content']
        date_posted = post['date_posted']
        author = post['author']

        self._exec_sql(sql, (author, title, content, date_posted))

    def get_post(self, author):
        sql = '''
        SELECT * FROM posts WHERE author = %s
        '''

        return self._exec_sql_ret(sql, (author,))
    
    def get_posts(self):
        sql = '''
        SELECT * FROM posts
        '''
        return self._exec_sql_ret_all(sql)

    def update_post(self, post):
        ''' Update the post of a single user '''

        sql = '''
        UPDATE posts
        SET title = %s,
            content = %s,
            date_posted = %s,
        WHERE author = %s,
        '''

        title = post['title']
        content = post['content']
        date_posted = post['date_posted']
        author = post['author']

        self._exec_sql(sql, (title, content, date_posted, author))

    def delete_post(self, author):
        ''' Delete a users post'''

        sql =  '''
        DELETE FROM posts WHERE author = %s 
        '''

        self._exec_sql(sql, (author,))


    # Gallery
    def add_image(self, image_name, poster):
        sql = '''
        INSERT INTO gallery (poster, image_name)
        VALUES (%s, %s)
        '''

        self._exec_sql(sql, (poster, image_name))

    def get_image(self, image_name):
        sql = '''
        SELECT * FROM gallery WHERE image_name = %s
        '''

        return self._exec_sql_ret(sql,(image_name,))

    def get_user_images(self, poster):
        sql = '''
        SELECT * FROM gallery WHERE poster = %s
        '''

        return self._exec_sql_ret_all(sql, (poster,))

    def delete_image(self, image_name):
        sql = '''
        DELETE FROM gallery WHERE image_name = %s
        '''

        self._exec_sql(sql, (image_name,))


    # Notifications
    def add_notification(self, sender_id, reciever_id, content):
        sql = '''
        INSERT INTO notifications (sender_id, reciever_id, content)
        VALUES (%s, %s, %s)
        '''

        self._exec_sql(sql, (sender_id, reciever_id, content))

    def get_notifications(self, reciever_id):
        sql = '''
        SELECT * FROM notifications WHERE reciever_id = %s
        '''

        return self._exec_sql_ret_all(sql, (reciever_id,))

    def delete_notification(self, id):
        sql = '''
        DELETE FROM notifications WHERE id = %s
        '''

        self._exec_sql(sql, (id,))


    # Courting
    def court(self, courter_id, courted_id):
        ''' Adds a record of who courts who.'''
        sql = '''
        INSERT INTO courtship (courter_id, courted_id)
        VALUES (%s, %s)
        '''

        self._exec_sql(sql, (courter_id, courted_id))

    def accept_courting(self, courter_id, courted_id):
        ''' This sets the "matched" field to true, meaning that the two parties are 
            now courting each other.
        '''

        sql= '''
        UPDATE courtship
        SET matched = 1
        WHERE courted_id = %s AND courter_id = %s
        '''

        self._exec_sql(sql, (courted_id, courter_id))

    def get_all_courters(self, courted_id):
        ''' Gets all entries where the user is being courted '''

        sql = '''
        SELECT * FROM courtship WHERE courted_id = %s
        '''

        return self._exec_sql_ret_all(sql, (courted_id,))

    def get_all_courted(self, couter_id):
        ''' Gets all the entries where the user is courting someone '''

        sql = '''
        SELECT * FROM courtship WHERE courter_id = %s
        '''

        return self._exec_sql_ret_all(sql, (couter_id,))


    # Internal functions
    def _exec_sql(self, sql, args=None):
        ''' This function executes the sql '''
        with self._client.cursor() as cursor:
            cursor.execute(sql, args)

        self._client.commit()

    def _exec_sql_ret(self, sql, args=None):
        ''' Executes the sql and returns one value from the database '''
        results = None

        with self._client.cursor() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchone()

        return results

    def _exec_sql_ret_all(self, sql, args=None):
        ''' Executes the sql and returns one value from the database '''
        results = None

        with self._client.cursor() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchall()

        return results




if __name__ == '__main__':
    db = DB()
    # db.create_tables()
    details = {
        'username': 'Lebogang',
        'firstname': 'Lebogang',
        'lastname': 'Petsoane',
        'email': 'email',
        'email_confirmed': 0,
        'password': 'LebogangsPassword',
        'age' : 21,
        'image_name': 'default.png',
        'fame_rating': 0,
        'gender': 'female',
        'sex': 'bisexual',
        'bio': 'This is the bio',
        'interests': ['Volley ball', 'Coding'],
        'location': ['Johanesburg', 'South Africa'],
        'latlon': '12,1231,343,124,',
        'last_seen': datetime.utcnow()

    }
    # Test user crud
    print('\n\n[user crud]')
    db.register_user(details)
    print(db.get_user({'username': details['username']}))
    details['username'] = 'Neophyl',
    details['id'] = 1
    db.update_user(details)
    db.delete_user(7)

    # Test user_info
    print('\n\n[user info]')
    db.update_user_info(details, True)
    print(db.get_user_info(details['id']))

    # Test posts crud
    print('\n\n[post crud]')
    post = {
        'author': 1,
        'title': 'This is a simple test',
        'content': 'Wow if this works I should be done with the minor parts',
        'date_posted': datetime.utcnow()
    }
    db.create_post(post)
    print(db.get_post(1))


    # Gallery 
    print('\n\n[Gallery]')
    db.add_image('test', 1)
    print(db.get_image('test'))
    print(db.get_user_images(1))

    # Notifications
    print('\n\n[Notifications]')
    db.add_notification(1, 2, 'Bluh has just liked you')
    print(db.get_notifications(1))

    # Courting
    print('\n\n[Courting]')
    db.court(1, 2)
    print(db.get_all_courters(2))
    print(db.get_all_courted(1))