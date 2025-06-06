# Generated by Django 5.2.1 on 2025-06-01 19:56

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import listings.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=150, unique=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", listings.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                ("role_id", models.AutoField(primary_key=True, serialize=False)),
                ("role_name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                ("property_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("location", models.CharField(max_length=255)),
                (
                    "price_per_night",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "host",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("booking_id", models.AutoField(primary_key=True, serialize=False)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("total_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("confirmed", "Confirmed"),
                            ("canceled", "Canceled"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="listings.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("review_id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                ("comment", models.TextField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="listings.property",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="role",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="listings.role",
            ),
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("message_id", models.AutoField(primary_key=True, serialize=False)),
                ("message_body", models.TextField()),
                ("sent_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "recipient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="received_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sent_messages",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["sender"], name="idx_message_sender"),
                    models.Index(fields=["recipient"], name="idx_message_recipient"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("payment_id", models.AutoField(primary_key=True, serialize=False)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "payment_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("payment_method", models.CharField(max_length=50)),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="listings.booking",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["booking"], name="idx_payment_booking")
                ],
            },
        ),
        migrations.AddIndex(
            model_name="property",
            index=models.Index(fields=["host"], name="idx_property_host"),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["property"], name="idx_booking_property"),
        ),
        migrations.AddIndex(
            model_name="booking",
            index=models.Index(fields=["user"], name="idx_booking_user"),
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.CheckConstraint(
                condition=models.Q(("start_date__lt", models.F("end_date"))),
                name="check_start_date_before_end_date",
            ),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(fields=["property"], name="idx_review_property"),
        ),
        migrations.AddIndex(
            model_name="review",
            index=models.Index(fields=["user"], name="idx_review_user"),
        ),
    ]
