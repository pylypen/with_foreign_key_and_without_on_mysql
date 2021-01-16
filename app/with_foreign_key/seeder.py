from django_seed import Seed
from models import Users

seeder = Seed.seeder()

seeder.add_entity(Users, 10)
seeder.execute()
