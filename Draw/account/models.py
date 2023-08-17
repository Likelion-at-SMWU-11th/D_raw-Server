from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class Guide(models.Model):
    TERM_CHOICES = [ # 안내사 경력 기간 선택지
        ('1', '3개월 미만'),
        ('2', '3개월~6개월'),
        ('3','6개월~1년'),
        ('4', '1년 이상'),
    ]
    LOCATION_CHOICES = [ # 안내사 활동 지역 선택지
        ('1', '서울특별시'),
        ('2', '부산광역시'),
        ('3', '대구광역시'),
        ('4', '인천광역시'),
        ('5', '광주광역시'),
        ('6', '대전광역시'),
        ('7', '울산광역시'),
        ('8', '세종특별자치시'),
        ('9', '경기도'),
        ('10', '강원도'),
        ('11', '충청북도'),
        ('12', '충청남도'),
        ('13', '전라북도'),
        ('14', '전라남도'),
        ('15', '경상북도'),
        ('16', '경상남도'),
        ('17', '제주특별자치도'),
    ]
    name = models.CharField(verbose_name='안내사 이름', max_length=5, null=True, default='')
    age = models.IntegerField(verbose_name='나이', null=True, default=0)
    rate = models.IntegerField(verbose_name='받은 칭찬도장 개수', null=True)
    start_date = models.DateTimeField(verbose_name='안내사 첫 시작일', null=True)
    career = models.CharField(verbose_name='안내사 경력', choices=TERM_CHOICES, max_length=20, null=True, default='')
    location = models.CharField(verbose_name='안내사 활동 가능 지역', choices=LOCATION_CHOICES, max_length=20, null=True, default='')


class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, user_id, password, email, nickname, introduce, profile_photo, gender, **kwargs):
        """
        주어진 개인정보로 일반 User 인스턴스 생성
        """       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_id = user_id,
            email = email,
            nickname = nickname,
            introduce = introduce,
            profile_photo = profile_photo,
            gender = gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, password, **extra_fields):
        """
        주어진 개인정보로 관리자 User 인스턴스 생성
        최상위 사용자이므로 권한 부여
        """
        user = self.create_user(
            user_id = user_id,
            email = email,
            nickname = user_id,
            password = password,
            introduce = None,
            profile_photo = None,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to="img/avatar/", blank=True, null=True)
    user_id = models.CharField(unique=True, blank=False, null=False, max_length=15)
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    nickname = models.CharField(unique=True, blank=False, null=False, max_length=15)
    introduce = models.CharField(blank=True, null=True,  max_length=50)
    profile_photo = models.ImageField(blank=True, null=True,  max_length=400)
    last_login = models.DateField(auto_now=True, null=True)
    gender = models.CharField(unique=True, null=True, max_length=10)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 user id로 설정
    USERNAME_FIELD = 'user_id'
    # 필수 작성 field
    REQUIRED_FIELDS = ['email']