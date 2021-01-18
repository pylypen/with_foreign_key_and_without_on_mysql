from time import time
from django.core.management.base import BaseCommand, CommandError
from with_foreign_key.models import Comments as CommentsWith
from without_foreign_key.models import Comments as CommentsWithout
from django.db import connection
import time


class Command(BaseCommand):
    help = 'execute speed'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.numbers_of_iterations = 100

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('With FK:'))
        self.with_fk()
        self.stdout.write(self.style.SUCCESS('=========='))
        self.stdout.write(self.style.SUCCESS('Without FK:'))
        self.without_fk()

    def with_fk(self):
        counts = 0

        for i in range(self.numbers_of_iterations):
            start_time = time.time()
            sql = """
                SELECT * FROM `with_foreign_key_comments` AS `comment`
    
                RIGHT JOIN `with_foreign_key_blogs` AS `blog` ON `comment`.`comment_to_id` = `blog`.`id`
                
                RIGHT JOIN `with_foreign_key_users` AS `user` ON `comment`.`created_by_id` = `user`.`id`
                
                WHERE `comment`.`comment_to_id` IN (
                    SELECT `blog`.`id` FROM `with_foreign_key_blogs` AS `blog` 
                
                    RIGHT JOIN `with_foreign_key_blogtypes` AS `blog_type` ON `blog`.`type_id` = `blog_type`.`id`
                
                    RIGHT JOIN `with_foreign_key_users` AS `user` ON `blog`.`created_by_id` = `user`.`id`
                
                    WHERE `blog`.`type_id` IN (11, 30, 7)
                )
                LIMIT 1000
                """
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                row = cursor.fetchall()
            except Exception as e:
                cursor.close

            counts += round((time.time() - start_time), 5)

        self.stdout.write(self.style.SUCCESS("AVG Exec time: %s seconds" % round(counts / self.numbers_of_iterations, 5)))

    def without_fk(self):
        counts = 0

        for i in range(self.numbers_of_iterations):
            start_time = time.time()

            sql = """
                SELECT * FROM `without_foreign_key_comments` AS `comment`
    
                RIGHT JOIN `without_foreign_key_blogs` AS `blog` ON `comment`.`comment_to` = `blog`.`id`
                
                RIGHT JOIN `without_foreign_key_users` AS `user` ON `comment`.`created_by` = `user`.`id`
                
                WHERE `comment`.`comment_to` IN (
                
                    SELECT `blog`.`id` FROM `without_foreign_key_blogs` AS `blog` 
                
                    RIGHT JOIN `without_foreign_key_blogtypes` AS `blog_type` ON `blog`.`type` = `blog_type`.`id`
                
                    RIGHT JOIN `without_foreign_key_users` AS `user` ON `blog`.`created_by` = `user`.`id`
                
                    WHERE `blog`.`type` IN (11, 30, 7)
                )
                LIMIT 1000
                """
            cursor = connection.cursor()
            try:
                cursor.execute(sql)
                row = cursor.fetchall()
            except Exception as e:
                cursor.close

            counts += round((time.time() - start_time), 5)

        self.stdout.write(self.style.SUCCESS("AVG Exec time: %s seconds" % round(counts / self.numbers_of_iterations, 5)))
