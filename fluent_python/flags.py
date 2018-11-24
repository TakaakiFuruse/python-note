import time
import sys

POP20_CC = ("CN IN US BR PK NG BD RU JP MX").split()

def save_flag(img, filename):
    print(f"{img} was saved as {filename}")
    
def get_flag(cc):
    time.sleep(1)
    print(f"downloading {cc}")
    return f"{cc}"

def download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        save_flag(image, image + ".gif")
    return len(cc_list)
        
def main(download_many):
    t0 = time.time()
    count = download_many(POP20_CC)
    elapsed = time.time() - t0
    print(f"{count} flags downloaded in {elapsed}s")
    
main(download_many)