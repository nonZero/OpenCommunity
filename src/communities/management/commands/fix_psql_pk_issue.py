# coding: utf-8
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Fix duplicate key value violates unique constraint error on committee table"

    def handle(self, *args, **options):
        cursor = connection.cursor()
        cursor.execute("SELECT setval('communities_committee_id_seq', (SELECT MAX(id) FROM communities_committee)+1)")
        print "Done"
