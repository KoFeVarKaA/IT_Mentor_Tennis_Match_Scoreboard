import requests

base_url = "http://185.21.156.184:8000/new-match"

for i in range(123, 151):
    data = {
        "playerOne": f"{i}",
        "playerTwo": f"{i}"
    }
    response = requests.post(base_url, data=data)
    print(f"Создан матч для Игрок{i} и Соперник{i}. Статус: {response.status_code}")
