from time import time
from django.core.management.base import BaseCommand
from django.db import connection
import time
from with_foreign_key.models import BlogTypes as BlogTypesFK
from without_foreign_key.models import BlogTypes


class Command(BaseCommand):
    help = 'execute speed'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.numbers_of_iterations = 10000
        self.sql_limit = 100

    def handle(self, *args, **options):
        # With FK DB
        self.stdout.write(self.style.SUCCESS('With FK:'))
        self.generate_sql_execute('with_foreign_key', 'comment_to_id', 'type_id', 'created_by_id', BlogTypesFK)

        # Without FK DB
        self.stdout.write(self.style.SUCCESS('=========='))
        self.stdout.write(self.style.SUCCESS('Without FK:'))
        self.generate_sql_execute('without_foreign_key', 'comment_to', 'type', 'created_by', BlogTypes)

    def generate_sql_execute(self, db_prefix, comment_to_id, blog_type_id, created_by_id, model_blog_type):
        counts = 0
        max_time = 0
        min_time = 99999
        random_blog_types = model_blog_type.objects.order_by('?').values_list('id', flat=True)[:5]

        for i in range(self.numbers_of_iterations):
            start_time = time.time()
            sql = """
                SELECT * FROM `{db_prefix}_comments` AS `comment`

                RIGHT JOIN `{db_prefix}_blogs` AS `blog` ON `comment`.`{comment_to_id}` = `blog`.`id`

                RIGHT JOIN `{db_prefix}_users` AS `user` ON `comment`.`{created_by_id}` = `user`.`id`

                WHERE `comment`.`{comment_to_id}` IN (
                    SELECT `blog`.`id` FROM `{db_prefix}_blogs` AS `blog` 

                    RIGHT JOIN `{db_prefix}_blogtypes` AS `blog_type` ON `blog`.`{blog_type_id}` = `blog_type`.`id`

                    RIGHT JOIN `{db_prefix}_users` AS `user` ON `blog`.`{created_by_id}` = `user`.`id`

                    WHERE `blog`.`{blog_type_id}` IN ({}, {}, {}, {}, {})
                )
                LIMIT {sql_limit}
                """.format(
                db_prefix=db_prefix,
                comment_to_id=comment_to_id,
                blog_type_id=blog_type_id,
                created_by_id=created_by_id,
                sql_limit=self.sql_limit,
                *random_blog_types
            )

            cursor = connection.cursor()
            try:
                cursor.execute(sql)
            except Exception as e:
                cursor.close

            exec_time = round((time.time() - start_time), 5)
            max_time = max_time if (max_time > exec_time) else exec_time
            min_time = min_time if (min_time < exec_time) else exec_time
            counts += exec_time

        # REPORTS
        self.stdout.write(self.style.SUCCESS("MAX Exec time: %s seconds" % max_time))
        self.stdout.write(
            self.style.SUCCESS("AVG Exec time: %s seconds" % round(counts / self.numbers_of_iterations, 5))
        )
        self.stdout.write(self.style.SUCCESS("MIN Exec time: %s seconds" % min_time))
