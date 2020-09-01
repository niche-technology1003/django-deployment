import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()


# Fake Data Population
import random
from first_app.models import Topic, Webpage, AccessRecord
from faker import Faker

fakegen = Faker()

topics = ['Search', 'Social',  'Marketplace', 'Games']


def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t


def population(n=5):
    for entry in range(n):
        # get the topic
        top = add_topic()

        # create the fake data for grabbed topic
        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        # populate webpages
        webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]

        # create a fake access records
        acc_rec = AccessRecord.objects.get_or_create(name=webpg, date=fake_date)[0]


if __name__ == '__main__':
    print("Population script started")
    population(10)
    print("Data population completed")
