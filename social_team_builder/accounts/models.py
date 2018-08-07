''' user model for the accounts app '''
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from PIL import Image


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    display_name = models.CharField(max_length=140)
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        ''' overide init to save a copy of the orginal avatar '''
        super(User, self).__init__(*args, **kwargs)
        self.__original_avatar = self.avatar

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        ''' resize the image before saving to the database '''
        if self.avatar:
            if self.avatar != self.__original_avatar:
                try:
                    image = Image.open(self.avatar['image'])
                    image.thumbnail((300, 300), Image.ANTIALIAS)
                    new_name = 'tn_{}'.format(self.avatar['image'].name)
                    path = settings.MEDIA_ROOT + '/' + new_name
                    image.save(path, 'JPEG')
                    self.avatar = new_name
                except IOError:
                    print('image resize failed')
        else:
            self.avatar = '/default_avatar.jpeg'
            # add in username
        self.username = '@{}'.format(self.display_name.replace(' ', ''))

        # no change as no image selected; save an empty avatar
        super(User, self).save(*args, **kwargs)
        self.__original_avatar = self.avatar

    def __str__(self):
        return "{}".format(self.username)

    def get_short_name(self):
        return self.display_name

    def get_long_name(self):
        return "{}@{}".format(self.display_name, self.username)

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.pk})