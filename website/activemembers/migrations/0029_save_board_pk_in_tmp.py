# Generated by Django 2.0.8 on 2018-09-01 15:13

from django.db import migrations


def migrate_to(apps, schema_editor):
    Board = apps.get_model("activemembers", "Board")
    TemporaryBoard = apps.get_model("activemembers", "TemporaryBoard")

    boards = Board.objects.all()
    for board in boards:
        TemporaryBoard.objects.create(parent=board.committee_ptr_id)


def migrate_back(apps, schema_editor):
    TemporaryBoard = apps.get_model("activemembers", "TemporaryBoard")

    boards = TemporaryBoard.objects.all()
    for temp_board in boards:
        schema_editor.execute(
            'INSERT INTO activemembers_board (committee_ptr_id, is_board)'
            ' VALUES ({}, 1);'
            .format(temp_board.parent))


class Migration(migrations.Migration):

    dependencies = [
        ('activemembers', '0028_create_tmp_board_model'),
    ]

    operations = [
        migrations.RunPython(migrate_to, migrate_back),
    ]
