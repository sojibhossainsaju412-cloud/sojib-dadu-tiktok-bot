#!/usr/bin/env python3
import cloudscraper, time, random, argparse, re

BANNER = """
╔═══════════════════════════════════════════════════╗
║         SOJIB DADU - TikTok Free Bot             ║
║         Auto Liker + Auto Follower                ║
╚═══════════════════════════════════════════════════╝
"""
BASE_URL = "https://zefoy.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Linux; Android 12) Chrome/124.0.0.0 Mobile Safari/537.36", "Origin": BASE_URL, "Referer": BASE_URL + "/"}

def log(tag, msg): print({"+":" [+]","-":"[-]","*":"[*]","~":"[~]","!":"[!]"}.get(tag,tag), msg)

def countdown(s):
    for r in range(s, 0, -30):
        print(f"    ... {r}s remaining", end="\r", flush=True)
        time.sleep(min(30, r))
    print()

def create_session():
    s = cloudscraper.create_scraper(browser={"browser":"chrome","platform":"android","mobile":True})
    s.headers.update(HEADERS)
    return s

def get_token(s):
    try:
        r = s.get(BASE_URL, timeout=30)
        m = re.search(r'name="_token"\s+value="([^"]+)"', r.text)
        if m:
            log("+", "Token acquired.")
            return m.group(1)
        log("-", "Token not found.")
    except Exception as e:
        log("-", f"Error: {e}")
    return None

def run_service(s, token, url, rounds, endpoint):
    success = 0
    for i in range(rounds):
        log("*", f"Round {i+1}/{rounds}")
        try:
            r = s.post(endpoint, data={"_token": token, "url": url}, timeout=30)
            t = r.text.lower()
            if "success" in t or "sent" in t:
                success += 1
                log("+", f"Sent! Total: {success}")
            elif "wait" in t or "cooldown" in t:
                log("~", "Cooldown. Waiting 5 min...")
                countdown(300)
            else:
                log("~", f"Response: {r.text[:80]}")
        except Exception as e:
            log("-", f"Error: {e}")
        if i < rounds - 1:
            w = random.randint(290, 320)
            log("~", f"Next round in {w}s...")
            countdown(w)
    return success

def main():
    print(BANNER)
    p = argparse.ArgumentParser(description="SOJIB DADU - TikTok Free Bot")
    p.add_argument("--url", help="TikTok video URL")
    p.add_argument("--profile", help="TikTok profile URL")
    p.add_argument("--rounds", type=int, default=5)
    p.add_argument("--likes", action="store_true")
    p.add_argument("--followers", action="store_true")
    args = p.parse_args()

    if not args.likes and not args.followers:
        p.print_help()
        return

    s = create_session()
    log("*", "Connecting to Zefoy...")
    token = get_token(s)
    if not token:
        log("!", "Token failed. Check internet.")
        return

    l, f = 0, 0
    if args.likes and args.url:
        l = run_service(s, token, args.url, args.rounds, f"{BASE_URL}/tiktok-likes-tt")
    if args.followers and args.profile:
        f = run_service(s, token, args.profile, args.rounds, f"{BASE_URL}/tiktok-followers-tt")

    print(f"\n[=] Done. Likes: {l} | Followers: {f}")

if __name__ == "__main__":
    main()
