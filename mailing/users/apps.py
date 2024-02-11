from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from mailing_service.models import MailingList, Client  # Make sure to import the correct models

        moderator_group, moderator_created = Group.objects.get_or_create(name='Менеджеры')
        users_group, users_created = Group.objects.get_or_create(name='Пользователи')
        content_type_mailing = ContentType.objects.get_for_model(MailingList)
        content_type_client = ContentType.objects.get_for_model(Client)
        can_view_mailings_permission, moderator_created = Permission.objects.get_or_create(
            codename='can_view_mailings',
            name='Может просматривать рассылки',
            content_type=content_type_mailing
        )
        can_view_users_permission, moderator_created = Permission.objects.get_or_create(
            codename='can_view_users',
            name='Может просматривать пользователей',
            content_type=content_type_client
        )
        can_block_users_permission, moderator_created = Permission.objects.get_or_create(
            codename='can_block_users',
            name='Может блокировать пользователей',
            content_type=content_type_client
        )
        can_disable_mailings_permission, moderator_created = Permission.objects.get_or_create(
            codename='can_disable_mailings',
            name='Может отключать рассылки',
            content_type=content_type_mailing
        )

        moderator_group.permissions.add(
            can_view_mailings_permission,
            can_view_users_permission,
            can_block_users_permission,
            can_disable_mailings_permission
        )

        moderator_group.save()
        users_group.save()
