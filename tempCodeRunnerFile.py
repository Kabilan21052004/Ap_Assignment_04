import os
import time
import threading
import requests
from urllib.parse import urlparse

def fetch_file(url, destination="downloads"):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)

        name = os.path.basename(urlparse(url).path)
        if not name:
            name = f"file_{int(time.time())}.dat"

        full_path = os.path.join(destination, name)

        begin = time.time()
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(full_path, 'wb') as output_file:
            for block in response.iter_content(chunk_size=8192):
                if block:
                    output_file.write(block)

        finish = time.time()
        print(f"Downloaded {name} ({total_size/1024:.1f} KB) in {finish - begin:.2f} seconds")
        return True
    except Exception as err:
        print(f"Failed to download {url}: {str(err)}")
        return False

def download_sequentially(links, destination="downloads"):
    print("\nStarting sequential download...")
    start = time.time()
    downloaded = 0

    for link in links:
        if fetch_file(link, destination):
            downloaded += 1

    end = time.time()
    duration = end - start
    print(f"\nSequential download completed: {downloaded}/{len(links)} files in {duration:.2f} seconds")
    return duration

def download_with_threads(links, destination="downloads", max_concurrent=5):
    print(f"\nStarting multi-threaded download with {max_concurrent} threads...")
    start = time.time()
    active_threads = []
    success_counter = [0]

    def task(link):
        if fetch_file(link, destination):
            success_counter[0] += 1

    for link in links:
        thread = threading.Thread(target=task, args=(link,))
        active_threads.append(thread)
        thread.start()

        while threading.active_count() > max_concurrent:
            time.sleep(0.1)

    for thread in active_threads:
        thread.join()

    end = time.time()
    duration = end - start
    print(f"\nThreaded download completed: {success_counter[0]}/{len(links)} files in {duration:.2f} seconds")
    return duration

def load_urls_from_file(path):
    try:
        with open(path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except Exception as error:
        print(f"Failed to read file: {str(error)}")
        return []

def run_downloader():
    print("Concurrent Downloader Tool")
    print("==========================")

    while True:
        print("\nChoose an option to provide download URLs:")
        print("1. Input URLs manually")
        print("2. Read URLs from a file")
        print("3. Use predefined sample URLs")
        print("4. Exit program")

        option = input("\nEnter choice (1-4): ")

        if option == '1':
            print("\nEnter URLs (one per line). Press Enter on an empty line to stop:")
            link_list = []
            while True:
                entry = input()
                if not entry:
                    break
                link_list.append(entry)

        elif option == '2':
            file_path = input("\nEnter the file path containing URLs: ")
            link_list = load_urls_from_file(file_path)

        elif option == '3':
            link_list = [
                "https://www.netflix.com/in/",
                "https://www.apple.com/in/",
                "https://www.google.co.in/"
            ]
            print("\nUsing sample URLs:")
            for u in link_list:
                print(f"- {u}")

        elif option == '4':
            print("Exiting...")
            break

        else:
            print("Invalid input. Please try again.")
            continue

        if not link_list:
            print("No URLs were provided. Please try again.")
            continue

        download_path = input("\nEnter download directory (default is 'downloads'): ") or "downloads"

        try:
            thread_limit = int(input("\nMax concurrent downloads (default: 5): ") or "5")
        except ValueError:
            thread_limit = 5
            print("Invalid input; using 5 threads by default.")

        time_seq = download_sequentially(link_list, download_path)
        time_threaded = download_with_threads(link_list, download_path, thread_limit)

        speed_boost = time_seq / time_threaded if time_threaded > 0 else 0
        print("\nDownload Performance Summary:")
        print(f"- Sequential: {time_seq:.2f} seconds")
        print(f"- Threaded:   {time_threaded:.2f} seconds")
        print(f"- Speedup:    {speed_boost:.2f}x")

        print("\nDo you want to download more files? (y/n):")
        if input().lower() != 'y':
            print("Done. Goodbye!")
            break

run_downloader()
