import requests

import login_credentials

spring_phase_order = ['O'] #['O', 'R', 'B']
fall_phase_order = [] #['O', 'R', 'B']

def download_order_images(game_name, session, partial_url, url_args_template):
    more_orders = True
    consecutive_failed = 0

    i = 0
    increment = 2
    while more_orders:
    #for i in range(-1, 4)[::2]:
        spring = i
        fall = i + 1
        counter = 1
        for phase in spring_phase_order:
            true_partial_url = partial_url + remaining_args_template.format(**{
                "gdate": spring,
                "phase": phase,
            })
            file_path = "./images/{}_{}_{}_{}.png".format(game_name, str(spring).zfill(3), counter, phase)
            print "Spring {}: ".format(phase),
            success = save_image_from_url(session, true_partial_url, file_path)
            if success == False:
                consecutive_failed += 1
            else:
                consecutive_failed = 0
            counter += 1
        counter = 1
        for phase in fall_phase_order:
            true_partial_url = partial_url + remaining_args_template.format(**{
                "gdate": fall,
                "phase": phase,
            })
            file_path = "./images/{}_{}_{}{}.png".format(game_name, str(fall).zfill(3), counter, phase)
            success = save_image_from_url(session, true_partial_url, file_path)
            if success == False:
                consecutive_failed += 1
            else:
                consecutive_failed = 0
            counter += 1
        if consecutive_failed >= 3:
            more_orders = False
        i += increment

    return True

def save_image_from_url(session, url, file_path):
    if not url:
        print "Failed to get URL for image(s)."
        return False
    """
    if url in ignore_list:
        print "URL is in ignore list."
        return False
    """
    if not file_path:
        return False

    print(url)
    image = download_image(session, url)
    if not image:
        return False
    save_image(image, file_path)

def download_image(session, image_url):
    try:
        image_request = session.get(image_url)
        print image_request
        image_request.raise_for_status()
    except requests.exceptions.HTTPError:
        print "No image at this location: {}".format(image_url)
        return
    except requests.exceptions.ConnectionError, socket.error:
        print "Failed to download. URL is: {}".format(image_url)
        failed_downloads.append(image_url)
        return
    return image_request

def save_image(image, file_path):
    """
    if os.path.isfile(file_path):
        print "Error: cannot save image; file already exists."
        return False
    """
    with open(file_path, 'w+') as f:
        for chunk in image.iter_content(1024):
            f.write(chunk)
    print u"Saved {}".format(file_path.split('/')[-1])
    file_name = file_path.split('/')[-1]
    return True

def get_game_url(game_id):
    #url = "http://www.playdiplomacy.com/game_history.php?game_id={game_id}".format(game_id=game_id)
    #remaining_url_args = "&gdate={gdate}&phase={phase}"
    partial_url = "http://www.playdiplomacy.com/games/1/{game_id}/game-history-{game_id}".format(game_id=game_id)
    remaining_url_args = "-{gdate}-{phase}.png"
    return partial_url, remaining_url_args

def login(session):
    login_url = "http://www.playdiplomacy.com/login.php"
    headers = {"content-type": "application/x-www-form-urlencoded"}
    request = session.post(login_url, data={"username": login_credentials.username, "password": login_credentials.password})
    print request
    request.raise_for_status()

    # TEST
    with open("./test.html", 'w+') as f:
        f.write(unicode(request.headers))


session = requests.Session()
login(session)

game_id = 134848
game_name = 'Nerds'
partial_url, remaining_args_template = get_game_url(game_id)
download_order_images(game_name, session, partial_url, remaining_args_template)
