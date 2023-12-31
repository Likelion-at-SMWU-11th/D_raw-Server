# Generated by Django 4.2.4 on 2023-08-18 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MatchUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('quick', '빠르게찾기'), ('profile', '프로필보고찾기')], default='없음', max_length=7)),
                ('time_choice', models.CharField(choices=[('AM', '오전'), ('PM', '오후')], default='', max_length=2)),
                ('start_hour', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12)])),
                ('place', models.TextField(verbose_name='place')),
                ('blind', models.CharField(choices=[('L', '없음'), ('M', '경증 장애'), ('H', '중증 장애')], default='없음', max_length=3)),
                ('birth', models.PositiveIntegerField(choices=[(1915, 1915), (1916, 1916), (1917, 1917), (1918, 1918), (1919, 1919), (1920, 1920), (1921, 1921), (1922, 1922), (1923, 1923), (1924, 1924), (1925, 1925), (1926, 1926), (1927, 1927), (1928, 1928), (1929, 1929), (1930, 1930), (1931, 1931), (1932, 1932), (1933, 1933), (1934, 1934), (1935, 1935), (1936, 1936), (1937, 1937), (1938, 1938), (1939, 1939), (1940, 1940), (1941, 1941), (1942, 1942), (1943, 1943), (1944, 1944), (1945, 1945), (1946, 1946), (1947, 1947), (1948, 1948), (1949, 1949), (1950, 1950), (1951, 1951), (1952, 1952), (1953, 1953), (1954, 1954), (1955, 1955), (1956, 1956), (1957, 1957), (1958, 1958), (1959, 1959), (1960, 1960), (1961, 1961), (1962, 1962), (1963, 1963), (1964, 1964), (1965, 1965), (1966, 1966), (1967, 1967), (1968, 1968), (1969, 1969), (1970, 1970), (1971, 1971), (1972, 1972), (1973, 1973), (1974, 1974), (1975, 1975), (1976, 1976), (1977, 1977), (1978, 1978), (1979, 1979), (1980, 1980), (1981, 1981), (1982, 1982), (1983, 1983), (1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004)], verbose_name='Birth')),
                ('gender', models.CharField(blank=True, choices=[('F', '여성'), ('M', '남성')], default='여성', max_length=2)),
                ('prefer_gender', models.CharField(blank=True, choices=[('F', '여성'), ('M', '남성'), ('N', '모두 가능')], default='여성', max_length=5)),
                ('list', models.CharField(choices=[('Bank', '모바일 뱅킹'), ('Ecommerce', '전자상거래'), ('Service', '공공서비스'), ('Docs', '전자 문서 처리'), ('Sns', '소셜 미디어'), ('Kiosk', '키오스크')], default='', max_length=9)),
                ('plus', models.CharField(choices=[('Y', '성인 안내사 선호'), ('N', '연령 상관 없음')], default='', max_length=2)),
                ('care', models.CharField(blank=True, max_length=300)),
            ],
        ),
    ]
