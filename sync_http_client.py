import time
import requests

def fetch_url(url: str) -> str:
    return requests.get(url).text[:15]


def main() -> None:
    url: str = "https://google.com"

    start_time = time.time()

    for i in range(5):
        res: str = fetch_url(url)
        print(res)

    print(f"It took: {time.time() - start_time}")


if __name__ == "__main__":
    main()
