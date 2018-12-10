import datetime

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


import datetime

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, sex, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        now = datetime.date.today()
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            sex=sex,
            created_at=now,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=20,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    sex = models.CharField(
        verbose_name='sex',
        max_length=10,
        null=True
    )
    created_at = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    # set current time to created_date
    def set_created_date(self):
        self.created_at = datetime.date.today()



class User_realation(models.Model):
    uid = models.ForeignKey(MyUser, related_name='uid_UR', on_delete=models.CASCADE)
    friend_id =models.ForeignKey(MyUser, related_name='friend_id_UR', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('uid', 'friend_id'),)

    primary = ('uid', 'friend_id')


    def __str__(self):
        return "User_realation"


class One_to_one_msg_record(models.Model):
    mid = models.IntegerField(primary_key=True)
    form_id = models.ForeignKey(MyUser, related_name='from_id_O2O', on_delete=models.CASCADE)
    to_id = models.ForeignKey(MyUser, related_name='to_id_O2O', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_time = models.DateField(auto_now_add=True)

    def __str__(self):
        return "One_to_one_msg_record"

class Group(models.Model):
    gid = models.IntegerField(primary_key=True)
    gname = models.CharField(max_length=20)
    create_time = models.DateField(auto_now_add=True)
    num_of_group = models.IntegerField()
    master_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)


class Group_msg(models.Model):
    mid = models.IntegerField()
    form_id = models.ForeignKey(MyUser, related_name='from_id_GM', on_delete=models.CASCADE)
    gid = models.ForeignKey(Group, related_name='gid_GM', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    create_time = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (('mid', 'gid'),)

    primary = ('mid', 'gid')



class G_msg_config(models.Model):
    uid = models.ForeignKey(MyUser, related_name='uid_GMC', on_delete= models.CASCADE)
    gid = models.ForeignKey(Group, related_name='gid_GMC', on_delete= models.CASCADE)
    last_read_msg_id = models.ForeignKey(Group_msg,  related_name='last_read_msg_id', on_delete=models.CASCADE,null=False)

    class Meta:
        unique_together = (('uid', 'gid'),)

    primary = ('uid', 'gid')