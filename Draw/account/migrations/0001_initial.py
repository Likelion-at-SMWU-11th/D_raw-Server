
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=5, null=True, verbose_name='안내사 이름')),
                ('age', models.IntegerField(default=0, null=True, verbose_name='나이')),
                ('rate', models.IntegerField(null=True, verbose_name='받은 칭찬도장 개수')),
                ('start_date', models.DateTimeField(null=True, verbose_name='안내사 첫 시작일')),
                ('career', models.CharField(choices=[('1', '3개월 미만'), ('2', '3개월~6개월'), ('3', '6개월~1년'), ('4', '1년 이상')], default='', max_length=20, null=True, verbose_name='안내사 경력')),
                ('location', models.CharField(choices=[('1', '서울특별시'), ('2', '부산광역시')], default='', max_length=20, null=True, verbose_name='안내사 활동 가능 지역')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('method', models.CharField(choices=[('quick', '빠르게찾기'), ('profile', '프로필보고찾기')], default='', max_length=7, null=True)),
                ('time_choice', models.CharField(choices=[('AM', '오전'), ('PM', '오후')], default='', max_length=2)),
                ('start_hour', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)], default='0', null=True)),
                ('place', models.TextField(null=True, verbose_name='place')),
                ('blind', models.CharField(choices=[('L', '없음'), ('M', '경증 장애'), ('H', '중증 장애')], default='', max_length=3, null=True)),
                ('birth', models.PositiveIntegerField(choices=[(1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004)], default='0', null=True, verbose_name='Birth')),
                ('prefer_gender', models.CharField(blank=True, choices=[('F', '여성'), ('M', '남성'), ('N', '모두 가능')], default='', max_length=5, null=True)),
                ('list', models.CharField(choices=[('Bank', '모바일 뱅킹'), ('Ecommerce', '전자상거래'), ('Service', '공공서비스'), ('Docs', '전자 문서 처리'), ('Sns', '소셜 미디어'), ('Kiosk', '키오스크')], default='', max_length=9, null=True)),
                ('plus', models.CharField(choices=[('Y', '성인 안내사 선호'), ('N', '연령 상관 없음')], default='', max_length=2, null=True)),
                ('care', models.CharField(blank=True, max_length=300, null=True)),
                ('role', models.CharField(choices=[('user', 'User'), ('guide', 'Guide')], default='user', max_length=10)),
                ('username', models.CharField(max_length=15, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('profile_photo', models.ImageField(blank=True, max_length=400, null=True, upload_to='')),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('age', models.IntegerField(default=0, null=True, verbose_name='나이')),
                ('rate', models.IntegerField(null=True, verbose_name='받은 칭찬도장 개수')),
                ('start_date', models.DateTimeField(null=True, verbose_name='안내사 첫 시작일')),
                ('career', models.CharField(choices=[('1', '3개월 미만'), ('2', '3개월~6개월'), ('3', '6개월~1년'), ('4', '1년 이상')], default='', max_length=20, null=True, verbose_name='안내사 경력')),
                ('location', models.CharField(choices=[('1', '서울특별시'), ('2', '부산광역시')], default='', max_length=20, null=True, verbose_name='안내사 활동 가능 지역')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
