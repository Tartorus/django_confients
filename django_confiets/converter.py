def update(forward_map, source_field, target_field, output_field_type):
    cases = list()

    for k, v in forward_map.items():
        args = {source_field: k, 'then': models.Value(v)}
        cases.append(models.When(**args))

    update_args = {target_field: models.Case(*cases, output_field=output_field_type())}
    return update_args




def forward(apps, schema_editor):
    Event = apps.get_model('core', 'Event')
    severity_map = dict(low=1, medium=2, high=3)
    upd_args = update(severity_map, 'severity', 'severity_1', models.SmallIntegerField)
    Event.objects.update(**upd_args)


"""Должно быть 2 миграции иначе возникают проблемы.
1 миграция:
- создает буферное поле с конечным типо поля;
- делает original_field нулевым.
2 миграция:
- удаляет original_field;
- переименовыевает buffer_field в original_field
- делает поле не нулевым (опционально) """

class Migration(migrations.Migration):

    dependencies = [
        ('app', ''),
    ]

    operations = [
        migrations.AddField(
            model_name='model_name',
            name='buffer_field',
            field=models.SmallIntegerField(choices=[(1, 'Низкая'), (2, 'Средняя'), (3, 'Высокая')], db_index=True,
                                           default=3, verbose_name='серьезность'),
        ),

        migrations.AlterField(
            model_name='model_name',
            name='original_field',
            field=models.CharField(choices=[('low', 'Низкая'), ('medium', 'Средняя'), ('high', 'Высокая')], db_index=True, default='high', max_length=7, verbose_name='серьезность', null=True)
        )
    ]


class Migration(migrations.Migration):


    dependencies = [
        ('app', '0021_auto_20180710_0840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='severity',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='severity_1',
            new_name='severity'
        ),
