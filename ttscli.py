import argparse
import requests
import time

server_url = "http://127.0.0.1:8000"


"""
Klient nie implementuje architektury trójwarstwowej z powodu braku istniena warstwy związanej z przechowywaniem danych.
Jest to aplikacja konsolowa która:
- przyjmuje parametry z konsoli,
- przetwarza i waliduje je (warstwa aplikacji), oraz
- wysyła dane do serwera i oczekuje na odpowiedź (warstwa prezentacji)
Aplikacja nie przechowuje żadnego stanu, po odebraniu sygnału aplikacja zamykma się i nic nie zapisuje.
W zadaniu nie było nic wspomniane o przechowywaniu stanu klienta, więc jest jedynie możliwe zaimplementowanie
architektury dwuwarstwowej.
"""


def set_parameters(lang: str, rate: int, volume: float, gender: str) -> None:
    config = {
        "lang": lang,
        "rate": rate,
        "volume": volume,
        "gender": gender
    }
    r = None
    try:
        print("Sending parameters request...")
        r = requests.patch(f"{server_url}/set_parameter", json=config)
    except Exception as e:
        print(f"Failed to send parameter request: {e}")
        exit(1)
    if not r.status_code == 200:
        print(f"Failed to send parameter request: HTTP {r.status_code} - {r.text}")
        exit(1)


def server_text_request(text: str, out_file: str) -> None:
    r = None
    try:
        print("Sending data request...")
        r = requests.post(f"{server_url}/to_speech", json={"text": text})
    except Exception as e:
        print(f"Failed to send data request: {e}")
        exit(1)
    if r.status_code == 200:
        with open(out_file, "wb") as f:
            print(f"Saving result as {f.name}... ", end="")
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
            print("Saved!")
    else:
        print(f"Failed to send data request: HTTP {r.status_code} - {r.text}")
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A client for a Text-To-Speech app")
    parser.add_argument("text", type=str,
                        help="Text to send to server",
                        nargs="?")
    parser.add_argument("-o", "--output", type=str,
                        help="Output speech file",
                        default=f"tts{time.strftime('%Y-%m-%d_%H-%M-%S')}.mp3", required=False)
    parser.add_argument("-s", "--source", type=str,
                        help="Input file", required=False)
    parser.add_argument("-l", "--lang", type=str,
                        help="TTS language",
                        default="en", required=False)
    parser.add_argument("-V", "--volume", type=float,
                        help="TTS volume",
                        default=1.0, required=False)
    parser.add_argument("-r", "--rate", type=int,
                        help="TTS speech rate in words per minute",
                        default=180, required=False)
    parser.add_argument("-g", "--gender", type=str,
                        help="TTS voice's gender (male or female)",
                        default="male", required=False)

    args = parser.parse_args()

    if args.gender not in ["male", "female"]:
        print("Please select valid gender option (\"male\" or \"female\").")
        exit(1)

    text_input = None
    if args.source:
        with open(args.source, "r") as f:
            text_input = f.read()
    elif args.text:
        text_input = args.text
    else:
        print("Please provide text input or file in -s argument.")
        exit(1)

    set_parameters(args.lang, args.rate, args.volume, args.gender)
    server_text_request(text_input, args.output)

    exit(0)
