from datetime import datetime, timedelta

date = "КЕЧА, 18:22"

publication_time = date.split(", ")[1]
publication_date = str(datetime.now() - timedelta(days=1)).split()[0]
publication_datetime = f"{publication_date} {publication_time}"
print(datetime.strptime(publication_datetime, "%Y-%m-%d %H:%M"))