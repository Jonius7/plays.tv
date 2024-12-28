import requests
import re
import time
import httpx


def parse_files():
    parse_list_of_urls("3 Parsed Urls")
    parse_list_of_urls("3a Parsed Urls")
    parse_list_of_urls("3b Parsed Urls")

def parse_list_of_urls(filename):
    with open(filename + ".txt", "r", newline='', encoding="UTF-8") as infile, \
         open(filename + ".output" + ".txt", "w", newline='', encoding="UTF-8") as outfile:
        for line in infile:
            #print(line)
            video_url = get_page_source(source=line)
            #time.sleep(1)
            #print("Your url: " + video_url)
            outfile.write(video_url + "\n")
    print(f"Processing complete. Check {filename}.output.txt")
    infile.close()
    outfile.close()

def get_page_source(quality=720,
                    source="https://web.archive.org/web/20191210100723/https://plays.tv/video/5b768fcfa003e8f045/ya-just-got-milled-son-"):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    #session = requests.Session()
    #session.headers.update({
    #    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    #})
    for attempt in range(3):
        try:
            print(source.strip())
            #r = httpx.get(source.strip())
            r = requests.get(source, headers=headers)
            #r = session.get(source)
            
            if r.status_code == 200:
                page_source = r.text

                lines = page_source.splitlines()

                line_number = 130
                pattern = fr'src="\/\/[/a-zA-z.0-9:-]*720.mp4'
                
                if len(lines) >= line_number:
                    specific_line = lines[line_number - 1]
                    #print(f"Line {line_number}: {specific_line}")

                    match = re.search(pattern, specific_line)
                    url = match.group().lstrip('src="//')

                    if match:
                        print(f"Url found: {url}")
                        return url
                    else:
                        print("No match found.")
                                
                else:
                    print(f"The page source has only {len(lines)} lines.")
                
                #720.mp4" type="video/mp4">
            if r.status_code == 429:
                print("Rate limit hit. Waiting before retrying...")
                time.sleep(2)  # Wait before retrying
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(120)  # Wait seconds before retrying
    else:
        print("All attempts failed.")
