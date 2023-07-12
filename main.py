from screenshot import Screenshot
import traceback
import signal
import logging
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

# Configure the logging system
logging.basicConfig(level=logging.INFO,  # Set the log level to DEBUG
                    format='%(asctime)s %(levelname)s: %(message)s',  # Define the log message format
                    datefmt='%Y-%m-%d %H:%M:%S')  # Define the date format


def keyboard_interrupt_handler(sig, frame):
    logging.info('Script stopped')
    del screenshot
    exit(0)

# Register the keyboard interrupt handler
signal.signal(signal.SIGINT, keyboard_interrupt_handler)

with open('links.txt', 'r') as file:
    links = file.readlines()

errors_file = open('errors.txt', 'a')
errors_count = 0
timedout_count = 0

## CДЕЛАТЬ ТАК ЧТО ПОСЛЕ ЗАМОРОЗКИ БРАЛИСЬ НОВЫЕ РАЗМКРЫ СТРАНИЦЫ nuxt sippor workshops

for i, link in enumerate(links):
    screenshot = Screenshot(size={'width': 1920, 'height': 1200}, scale_factor=2, wait_time=60, freeze_page=True)
    if link == '\n':
        continue
    file_directory = 'images2/'
    file_name = '_'.join(link.split('/')[2:]).replace('.', '_') + '_' + str(i) + '.png'
    output_file_name = file_directory + file_name

    print(f"{i+1}/{len(links)} # screenshoting {link[:-1]}")

    try:
        status = screenshot.get_fullpage_screenshot_as_file(link, output_file_name)
        if not status:
            timedout_count += 1
    except Exception as e:
        print(f"{i+1}/{len(links)} # FAILED {link[:-1]}")
        errors_file.write(link)
        errors_count += 1
        traceback.print_exc()
    finally:
        print(f'{i+1}/{len(links)} # done with {link}')
    
    del screenshot

all_pages_count = len(links)
print('PROCESS HAD BEEN FINISHED', f'Succesful: {all_pages_count - errors_count - timedout_count}/{all_pages_count} | Timedout: {timedout_count}/{all_pages_count} | Failed completely: {errors_count}/{all_pages_count}')
