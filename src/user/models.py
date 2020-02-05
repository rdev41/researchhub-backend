from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.utils import timezone
from allauth.socialaccount.providers.orcid.provider import OrcidProvider
from storages.backends.s3boto3 import S3Boto3Storage

from discussion.models import Thread, Comment, Reply
from hub.models import Hub
from mailing_list.models import EmailRecipient
from paper.models import Paper
from researchhub.settings import BASE_FRONTEND_URL
from summary.models import Summary
from utils.models import DefaultModel


class User(AbstractUser):
    """
    User objects have the following fields by default:
        https://docs.djangoproject.com/en/2.2/ref/contrib/auth/#django.contrib.auth.models.User
    """
    reputation = models.IntegerField(default=100)
    upload_tutorial_complete = models.BooleanField(default=False)
    has_seen_first_coin_modal = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    bookmarks = models.ManyToManyField(
        'paper.Paper',
        related_name='users_who_bookmarked'
    )

    def __str__(self):
        return '{} / {}'.format(
            self.email,
            self.first_name + ' ' + self.last_name
        )

    class Meta:
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        # A unique constraint is enforced on the username on the database
        # level. This line is used to ensure usernames are not empty without
        # requiring the client to enter a value in this field. It also forces
        # emails to be unique.
        #
        # If we want to allow client specified usernames, simply remove the
        # set username line.

        if (self.email is not None) and (self.email != ''):
            self.username = self.email

        user_to_save = super(User, self).save(*args, **kwargs)

        # Keep Email Recipient up to date with email
        if (self.email is not None) and (self.email != ''):
            if hasattr(self, 'emailrecipient') and (
                self.emailrecipient is not None
            ):
                if self.emailrecipient.email != self.email:
                    er = self.emailrecipient
                    er.email = self.email
                    er.save()
            else:
                EmailRecipient.objects.create(user=self, email=self.email)

        return user_to_save

    def set_has_seen_first_coin_modal(self, has_seen):
        self.has_seen_first_coin_modal = has_seen
        self.save()


@receiver(models.signals.post_save, sender=User)
def attach_author_and_email_preference(
    sender,
    instance,
    created,
    *args,
    **kwargs
):
    if created:
        Author.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
        )


class University(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}_{self.city}'

    class Meta:
        ordering = ['name']


class ProfileImageStorage(S3Boto3Storage):
    def __init__(self):
        super(ProfileImageStorage, self).__init__()

    def url(self, name):
        if 'http' in name:
            return name
        else:
            return super(ProfileImageStorage, self).url(name)


fs = ProfileImageStorage()


class Author(models.Model):
    user = models.OneToOneField(
        User,
        related_name='author_profile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=30)  # Same max_length as User
    last_name = models.CharField(max_length=150)  # Same max_length as User
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    description = models.TextField(
        null=True,
        blank=True
    )
    profile_image = models.FileField(
        upload_to='uploads/author_profile_images/%Y/%m/%d',
        max_length=1024,
        default=None,
        null=True,
        blank=True,
        storage=fs
    )
    university = models.ForeignKey(
        University,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    facebook = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True
    )
    twitter = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True
    )
    linkedin = models.CharField(
        max_length=255,
        default=None,
        null=True,
        blank=True
    )

    def __str__(self):
        university = self.university
        if university is None:
            university_name = ''
            university_city = ''
        else:
            university_name = university.name
            university_city = university.city
        return (f'{self.first_name}_{self.last_name}_{university_name}_'
                f'{university_city}')

    @property
    def orcid_id(self):
        try:
            return (
                self.user.socialaccount_set.get(provider=OrcidProvider.id).uid
            )
        except Exception:
            return None

    @property
    def profile_image_indexing(self):
        if self.profile_image is not None:
            try:
                return self.profile_image.url
            except ValueError:
                return str(self.profile_image)
        return None

    @property
    def university_indexing(self):
        if self.university is not None:
            return self.university
        return None


class Action(DefaultModel):
    user = models.ForeignKey(
        User,
        related_name='actions',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    read_date = models.DateTimeField(default=None, null=True)
    hubs = models.ManyToManyField(
        Hub,
        related_name='actions',
    )

    def __str__(self):
        return 'Action: {}-{}, '.format(
            self.content_type.app_label,
            self.content_type.model,
            self.object_id
        )

    def set_read(self):
        self.read_date = timezone.now()
        self.save()

    @property
    def frontend_view_link(self):
        link = BASE_FRONTEND_URL
        if isinstance(self.item, Summary):
            link += '/paper/{}/'.format(self.item.paper.id)
        elif isinstance(self.item, Paper):
            link += '/paper/{}/'.format(self.item.id)
        elif isinstance(self.item, Thread):
            link += '/paper/{}/discussion/{}'.format(
                self.item.paper.id,
                self.item.id
            )
        elif isinstance(self.item, Comment):
            link += '/paper/{}/discussion/{}'.format(
                self.item.paper.id,
                self.item.thread.id
            )
        elif isinstance(self.item, Reply):
            link += '/paper/{}/discussion/{}'.format(
                self.item.paper.id,
                self.item.thread.id,
            )
        else:
            raise Exception('frontend_view_link not implemented')
        return link
