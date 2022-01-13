from json.decoder import JSONDecodeError
from pyexpat import features

from app.constants import *
from app.data_access.game_dao import GameDAO
from app.models.custom_errors import *
from app.models.type import Type
from app.models.game import Game
from datetime import datetime
import requests
from core.models import Game as GameCore

global counter_games
counter_games = 0


def get_all_game_data_xbox(_locale, _country, is_update):
    game_ids_url = GET_GAME_IDS.format(_locale, _country, _country)

    written_game_ids_xbox = open(WRITTEN_GAME_IDS.format(_locale, _country), 'r', encoding='utf-8')
    written_game_ids_xbox_ = written_game_ids_xbox.readlines()
    written_game_ids_xbox.close()

    all_game_ids_xbox_ = []

    for json_obj in requests.get(game_ids_url).json():
        try:
            all_game_ids_xbox_.append(json_obj['id'])
        except KeyError:
            print('Key Error at: {}'.format(json_obj))

    all_game_ids_xbox_ = [x for x in all_game_ids_xbox_ if x not in [a.replace('\n', '')
                                                                     for a in written_game_ids_xbox_]]

    global counter_games
    counter_games = len(written_game_ids_xbox_)

    get_game_xbox_loop(all_game_ids_xbox_, _locale, _country, is_update)

    written_game_ids_xbox = open(WRITTEN_GAME_IDS.format(_locale, _country), 'w', encoding='utf-8')
    written_game_ids_xbox.close()


def get_game_xbox_loop(all_game_ids_xbox_, _locale, _country, is_update):
    dao = GameDAO()
    for id_ in all_game_ids_xbox_:

        page_data_failed_ids_xbox = open(PAGE_DATA_FAILED_IDS.format(_locale, _country), 'a', encoding='utf-8')
        written_game_ids_xbox = open(WRITTEN_GAME_IDS.format(_locale, _country), 'a', encoding='utf-8')
        non_game_ids_xbox = open(NON_GAME_IDS.format(_locale, _country), 'a', encoding='utf-8')

        global counter_games
        print('Getting game : {}'.format(counter_games))
        counter_games += 1

        try:
            if is_update:
                _game = get_game_data_xbox(_locale, _country, str(id_))
                query = dao.get_by_name(_game.get('name'))
                dao.update(query, _game)
            else:
                dao.create(get_game_data_xbox(_locale, _country, str(id_)))
            written_game_ids_xbox.write('{}\n'.format(id_))
            print('\t\tOk:' + str(id_))
        except PageDataIsNotJson as err:
            non_game_ids_xbox.write('{}\n'.format(id_))
            print('\t\t' + err.game_id)
        except GetPageDataFailed as err:
            page_data_failed_ids_xbox.write('{}\n'.format(id_))
            print('\t\t' + err.game_id)
        except GameCore.DoesNotExist:
            dao.create(get_game_data_xbox(_locale, _country, str(id_)))
        except Exception as e:
            print(e)
            raise e
        print('\n')

        page_data_failed_ids_xbox.close()
        written_game_ids_xbox.close()
        non_game_ids_xbox.close()


def get_game_data_xbox(_locale, _country, xbox_id):
    game_info_url = GET_GAME_DETAIL.format(xbox_id, _country, _locale, _country)
    # s = ','.join(i['id'] for i in game_ids if 'id' in i)

    try:
        data = requests.get(game_info_url.format(xbox_id)).json()
    except JSONDecodeError:
        raise PageDataIsNotJson(xbox_id)

    _type = Type()
    store = _type.xbox
    identifier = xbox_id

    locale = _locale  # "tr"
    country = _country  # "TR"

    identifier = xbox_id

    developers = data['Products'][0]['LocalizedProperties'][0]['DeveloperName'].split("|")
    developers = developers if len(developers[0]) > 0 else None
    publishers = data['Products'][0]['LocalizedProperties'][0]['PublisherName'].split("|")
    publishers = publishers if len(publishers[0]) > 0 else None

    pic_urls = ['https:' + json_obj['Uri'] for json_obj in data['Products'][0]['LocalizedProperties'][0]['Images']
                if json_obj['ImagePurpose'] == "Screenshot"]
    pic_urls = pic_urls if len(pic_urls[0]) > 0 else None

    thumbnail = 'https:{}'.format("".join(json_obj['Uri'] for json_obj in
                                          data['Products'][0]['LocalizedProperties'][0]['Images']
                                          if json_obj['ImagePurpose'] == "Poster"))

    thumbnail = thumbnail if len(thumbnail) > 0 else None
    # print(thumbnail)
    vid_urls = None

    tmp_name = data['Products'][0]['LocalizedProperties'][0]['ShortTitle']
    if tmp_name != "":
        name = tmp_name
    else:
        name = data['Products'][0]['LocalizedProperties'][0]['ProductTitle']

    short_desc = data['Products'][0]['LocalizedProperties'][0]['ShortDescription']
    long_desc = data['Products'][0]['LocalizedProperties'][0]['ProductDescription']
    short_desc = short_desc if len(short_desc) > 0 else None
    long_desc = long_desc if len(long_desc) > 0 else None

    release_date = data['Products'][0]['MarketProperties'][0]['OriginalReleaseDate'].split(':')[0]

    genres = data['Products'][0]['Properties']['Categories']

    if genres is not None:
        for i in genres:
            genres.extend(i.split('&'))
            genres.pop(genres.index(i))
        for i in genres:
            genres[genres.index(i)] = genres[genres.index(i)].upper().replace(' ', '')
    else:
        genres = data['Products'][0]['Properties']['Category'].split('&')
        for i in genres:
            genres[genres.index(i)] = genres[genres.index(i)].upper().replace(' ', '')

    genres = genres if len(genres[0]) > 0 else None

    store_url = "https://www.microsoft.com/{}-{}/p/x/{}".format(_locale, _country, xbox_id)

    title_specs = None
    min_specs = None
    rec_specs = None
    price = None

    return Game(
        name=name,
        thumbnail=thumbnail,
        release_date=release_date,
        store_url=store_url,
        locale=locale,
        country=country,
        short_desc=short_desc,
        long_desc=long_desc,
        min_specs=min_specs,
        rec_specs=rec_specs,
        title_specs=title_specs,
        vid_urls=vid_urls,
        pic_urls=pic_urls,
        developers=developers,
        genres=genres,
        price=price,
        publishers=publishers
    ).get()
