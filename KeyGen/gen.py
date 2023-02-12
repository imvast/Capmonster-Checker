import random
import time

def main():
    random.seed(int(time.time()))
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"

    with open("keys.txt", "w") as f:
        start = time.time()
        for i in range(100_000):
            b = [chars[random.randint(0, len(chars) - 1)] for i in range(32)]
            f.write("".join(b) + "\n")

        elapsed = time.time() - start
        print(f"[*] Generated 100,000 keys in {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
