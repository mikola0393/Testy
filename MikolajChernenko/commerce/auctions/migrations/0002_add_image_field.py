# auctions/migrations/0002_add_image_field.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='listing_images/'),
        ),
    ]
