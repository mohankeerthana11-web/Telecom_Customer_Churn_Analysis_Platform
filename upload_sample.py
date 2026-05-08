import httpx

url = "http://localhost:8001/upload/"
with open("sample_telecom_data.csv", "rb") as f:
    files = {"file": ("sample_telecom_data.csv", f, "text/csv")}
    response = httpx.post(url, files=files)
print(response.json())