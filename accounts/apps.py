from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configure the accounts app and set up group permissions."""

    name = "accounts"

    def ready(self):
        """Assign permissions to groups after migrations."""
        from django.db.models.signals import post_migrate
        post_migrate.connect(setup_permissions, sender=self)


def setup_permissions(sender, **kwargs):
    """Create groups and assign permissions to vendor and buyer."""
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from accounts.models import UserProfile

    vendor, _ = Group.objects.get_or_create(name='vendor')
    buyer, _ = Group.objects.get_or_create(name='buyer')

    userprofile_ct = ContentType.objects.get_for_model(UserProfile)

    can_manage_store, _ = Permission.objects.get_or_create(
        codename='can_manage_store',
        name='Can manage stores',
        content_type=userprofile_ct,
    )
    can_manage_product, _ = Permission.objects.get_or_create(
        codename='can_manage_product',
        name='Can manage products',
        content_type=userprofile_ct,
    )
    can_purchase, _ = Permission.objects.get_or_create(
        codename='can_purchase',
        name='Can purchase products',
        content_type=userprofile_ct,
    )
    can_review, _ = Permission.objects.get_or_create(
        codename='can_review',
        name='Can leave reviews',
        content_type=userprofile_ct,
    )

    vendor.permissions.set([can_manage_store, can_manage_product])
    buyer.permissions.set([can_purchase, can_review])
