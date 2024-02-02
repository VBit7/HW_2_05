import time
import requests

def fetch_url(session: requests.Session, url: str) -> str:
    return session.get(url).text[:15]


def main() -> None:
    url: str = "https://google.com"

    start_time = time.time()

    with requests.Session() as session:
        for i in range(5):
            res: str = fetch_url(session, url)
            print(res)

    print(f"It took: {time.time() - start_time}")


if __name__ == "__main__":
    main()
