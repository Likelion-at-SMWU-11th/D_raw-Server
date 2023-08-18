from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, username, password, email, profile_photo, **kwargs):
        """
        주어진 개인정보로 일반 User 인스턴스 생성
        """       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = email,
            profile_photo = profile_photo,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        """
        주어진 개인정보로 관리자 User 인스턴스 생성
        최상위 사용자이므로 권한 부여
        """
        user = self.create_user(
            username = username,
            email = email,
            password = password,
            profile_photo = None,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('guide', 'Guide'),
    )

    # 이용자 관련 필드
    METHOD_CHOICE = [
        ('quick', '빠르게찾기'),
        ('profile', '프로필보고찾기'),
    ]
    method = models.CharField(
        choices=METHOD_CHOICE, max_length=7, default='', null=True
    )

    # 날짜 선택
    start_time = models.DateField(auto_now=False, verbose_name='매칭 시간', null=True)

    # 시간
    time_choice = models.CharField(
        max_length=2,
        choices=[
            ('AM', '오전'),
            ('PM', '오후')
        ],
        default='',
        null=True
    )
    start_hour = models.IntegerField(choices=[(i, i) for i in range(1, 13)], null=True, default='0')

    # 장소
    place = models.TextField(verbose_name='place', null=True)

    # 시각장애 여부
    BLIND_CHOICES = [
        ('L', '없음'),
        ('M', '경증 장애'),
        ('H', '중증 장애'),
    ]
    blind = models.CharField(
        choices=BLIND_CHOICES, max_length=3, default='', null=True
    )

    # 출생년도 선택 리스트
    birth = models.PositiveIntegerField(
        verbose_name='Birth',
        choices=[(year, year) for year in range(1915, 2005)],
        null=True,
        default='0',
    )

    # 성별 선택 리스트
    GENDER_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
    ]
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=2, blank=True, default='', null=True
    )

    # 선호하는 성별 선택 리스트
    PREFER_GENDER_CHOICES = [
        ("F", "여성"),
        ("M", "남성"),
        ("N", "모두 가능"),
    ]
    prefer_gender = models.CharField(
        choices=PREFER_GENDER_CHOICES, max_length=5, blank=True, default='', null=True
    )

    # 집중 케어 필요 항목
    LIST_CHOICES = [
        ("Bank", "모바일 뱅킹"),
        ("Ecommerce", "전자상거래"),
        ("Service", "공공서비스"),
        ("Docs", "전자 문서 처리"),
        ("Sns", "소셜 미디어"),
        ("Kiosk", "키오스크"),
    ]

    list = models.CharField(
        choices=LIST_CHOICES, max_length=9, default='', null=True
    )

    # 안내사 매칭 추가 문의
    PLUS_CHOICES = [
        ("Y", "성인 안내사 선호"),
        ("N", "연령 상관 없음"),
    ]

    plus = models.CharField(
        choices=PLUS_CHOICES, max_length=2, default='', null=True
    )

    # 그 외 유의사항
    care = models.CharField(max_length=300, blank=True, null=True)

    # 안내사 관련 필드
    TERM_CHOICES = [
        ('1', '3개월 미만'),
        ('2', '3개월~6개월'),
        ('3', '6개월~1년'),
        ('4', '1년 이상'),
    ]
    LOCATION_CHOICES = [
        ('1', '서울특별시'),
        ('2', '부산광역시'),
        # 나머지 선택지들...
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user') # 가이드 안내사 구분
    username = models.CharField(unique=True, blank=False, null=False, max_length=15) # 이름
    email = models.CharField(unique=True, blank=False, null=False, max_length=255) # 이메일
    profile_photo = models.ImageField(blank=True, null=True,  max_length=400) # 프로필 사진 
    gender = models.CharField(blank=True, null=True, max_length=10) # 성별
    age = models.IntegerField(verbose_name='나이', null=True, default=0) # 나이
    rate = models.IntegerField(verbose_name='받은 칭찬도장 개수', null=True) # 가이드 - 받은 도장 개수
    start_date = models.DateTimeField(auto_now = False, verbose_name='안내사 첫 시작일', null=True) # 가이드 - 안내사 첫 활동일
    career = models.CharField(verbose_name='안내사 경력', choices=TERM_CHOICES, max_length=20, null=True, default='') # 가이드 - 경력
    location = models.CharField(verbose_name='안내사 활동 가능 지역', choices=LOCATION_CHOICES, max_length=20, null=True, default='') # 가이드 - 활동 가능 지역

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 user id로 설정
    USERNAME_FIELD = 'username'
    # 필수 작성 field
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        # return self.user_id
        return self.username
    
class Guide(models.Model):
    TERM_CHOICES = [
        ('1', '3개월 미만'),
        ('2', '3개월~6개월'),
        ('3', '6개월~1년'),
        ('4', '1년 이상'),
    ]
    LOCATION_CHOICES = [
        ('1', '서울특별시'),
        ('2', '부산광역시'),
        # 나머지 선택지들…
    ]

    name = models.CharField(verbose_name='안내사 이름', max_length=5, null=True, default='')
    age = models.IntegerField(verbose_name='나이', null=True, default=0)
    rate = models.IntegerField(verbose_name='받은 칭찬도장 개수', null=True)
    start_date = models.DateTimeField(auto_now = False, verbose_name='안내사 첫 시작일', null=True)
    career = models.CharField(verbose_name='안내사 경력', choices=TERM_CHOICES, max_length=20, null=True, default='')
    location = models.CharField(verbose_name='안내사 활동 가능 지역', choices=LOCATION_CHOICES, max_length=20, null=True, default='')
