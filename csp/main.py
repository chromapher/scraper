import requests
import bs4
import csv

def requestScore(subject, id):
    r = requests.get(f"https://csp.edu.vn/tra-cuu-diem-thi?scheduleId=11&examNumber={subject}.{id}")
    html = bs4.BeautifulSoup(r.text, features="html.parser")
    table = html.body.find('div', class_="tuyensinh_detail")
    rows = table.find("table").find_all("tr")
    data = {}
    for row in rows:
        cols = row.find_all("td")
        key = cols[0].text.strip()
        value = cols[1].text.strip()
        data[key] = value
    return(data)

subject = "CS"
start = 1579
end = 1811
listOfScores = []

for id in range(start, end+1):
    print(f"Requesting score for {subject}.{id:04}")
    listOfScores.append(requestScore(subject, f'{id:04}'))

column_order = ['Họ và tên', 'Số báo danh', 'Văn', 'Toán', 'Chuyên', 'Tổng điểm']
with open(f"{subject}.csv", mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.DictWriter(file, fieldnames=column_order)
    writer.writeheader()
    for row in listOfScores:
        writer.writerow({key: row.get(key, '') for key in column_order}) 

print(f"CSV file '{subject}.csv' has been created successfully!")