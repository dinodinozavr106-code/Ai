data = r.json()
    if "candidates" in data:
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
    else:
        answer = "Извините, не смог получить ответ. Ошибка: " + str(data)
