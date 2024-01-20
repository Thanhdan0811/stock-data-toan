import requests
from bs4 import BeautifulSoup


def get_refresToken_cookiesFrame():
    resp = requests.get("https://finance.vietstock.vn/chi-so-nganh.htm", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "*",
    })
    
    sp = BeautifulSoup(resp.text, features="html.parser")
    classContent = sp.find(attrs={"name": "__RequestVerificationToken"})
    requestToken = classContent.attrs['value']

    setCookie = resp.headers["Set-Cookie"].split("; ")
    dataCookies = resp.cookies["__RequestVerificationToken"]

    
    return {"requestToken": requestToken,"cookie": dataCookies}


def get_stock(req_token, cookie_frame):
    headerInfo = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": f'language=vi-VN; ASP.NET_SessionId=tuyd1dsvhqtin25wlimjjxxh; __RequestVerificationToken={cookie_frame}; Theme=Light; _pbjs_userid_consent_data=3524755945110770; _gid=GA1.2.1679713595.1704869503; AnonymousNotification=; dable_uid=56618015.1704869503736; __gads=ID=27693bd50b7fc418:T=1704869504:RT=1704869816:S=ALNI_MYeyezDtjrFDiLzI_Jy5UMwLu3HhA; __gpi=UID=00000cd4e53f1104:T=1704869504:RT=1704869816:S=ALNI_MaX69JDd1M5tK6sv6f1J3cTRyWliw; _ga_EXMM0DKVEX=GS1.1.1704869502.1.1.1704870008.60.0.0; _ga=GA1.2.908728565.1704869502; _gat_UA-1460625-2=1',
        "Accept-Encoding": "*",
    }
    formData = {
        "type": "1",
        "__RequestVerificationToken": req_token
    }

    # print("headerInfo", headerInfo, "\n", formData)

    resp = requests.post("https://finance.vietstock.vn/data/sectionindex", data=formData, headers=headerInfo)
    # print("resp", resp.json())

    return resp.json()



