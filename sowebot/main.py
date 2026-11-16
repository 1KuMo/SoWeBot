import requests
import os
from dotenv import find_dotenv, load_dotenv, set_key
from datetime import datetime, date, timedelta

env_file = find_dotenv()
load_dotenv(env_file)

if not os.getenv("SWS_KEY"):
    raise ValueError("SoWeSign token needed")


### GET 
token = os.getenv("SWS_KEY")
url = "https://app.sowesign.com/api/student-portal/future-courses?limit=25"
aScanner = ["ELEARNING", "CONFERENCE", "CRS-TD-CV"] # AUTONOMIE ? 

headers = {
    "Authorization" : "Bearer " + token,
    "Accept": "application/json"
}

### POST 
refreshToken = os.getenv("REFRESH_TOKEN")
url_post = "https://app.sowesign.com/api/portal/authentication/token/refresh"
headers_post = {
    "Authorization" : "Bearer " + refreshToken,
    "Accept": "application/json"
}

#===================================================
def refresh_token():
    response = requests.post(url_post, json=None, headers=headers_post, timeout=15)
    statut = response.status_code

    if statut == 200 :
        return response.json(), True
    else :
        return f'error: {statut}', False


def get_json(headers, url):
    response = requests.get(headers=headers, url=url, timeout=15)
    statut = response.status_code

    if statut in (400, 401) :
        new_data, ret = refresh_token()
        if ret :
            new_token = new_data["token"]

            set_key(env_file, "SWS_KEY", new_token)
            load_dotenv(env_file, override=True)

            headers["Authorization"] = "Bearer " + new_token
            response = requests.get(headers=headers, url=url, timeout=15)
            statut = response.status_code

    if statut == 200:
            response_json = response.json()
            return response_json

    else :
        return f'error: {statut}'

# print(get_json(headers, url))


def extraire_cours(edt:list):
    cours_a_scanner = []
    ''' reprise de help.md

    cours_a_scanner : list
    │
    └── cours : dict
        │
        ├── id : int
        ├── nom : str
        ├── date : str
        ├── debut : datetime
        ├── fin : datetime
        ├── categorie : str
        ├── opening : timedelta
        └── closing : timedelta
    '''

    for cours in edt:
        if cours["data"]["data7"] in aScanner:
            cours_a_scanner.append({
                "id": cours["id"],
                "nom": cours["name"],
                "date": cours["date"],
                "debut": datetime.fromisoformat(
                    cours["date"] + "T" + cours["start"]
                ),
                "fin": datetime.fromisoformat(
                    cours["date"] + "T" + cours["end"]
                ),
                "categorie": cours["data"]["data7"],
                "opening": timedelta(minutes=cours["openingDelay"]),
                "closing": timedelta(minutes=cours["closingDelay"])
            })

    return cours_a_scanner

# print(extraire_cours(get_json(headers, url)))


def todayCourses(tab_cours):
    tab = []
    today = date.today().isoformat()

    for cours in tab_cours:
        if cours["date"] == today:
            tab.append(cours)

    return tab

# print(todayCourses(extraire_cours(get_json(headers, url))))


def toScan(tab):
    now = datetime.now().astimezone()

    for cours in tab:
        heure_ouverture = cours["debut"] - cours["opening"]
        heure_fermeture = cours["fin"] + cours["closing"]

        if heure_ouverture <= now <= heure_fermeture:
            print(f"to scan : {cours['id']}")


edt = get_json(headers, url)
cours = extraire_cours(edt)
cours_du_jour = todayCourses(cours)
toScan(cours_du_jour)