import glob
import json
import shutil
from typing import List, Tuple

from settings import SUBSTITUTES, EOS_token, NWL_token


def load_all_json_conv(path_of_disc: str) -> List[str]:
    """From a path, clean the arborescence and stock path in a list

    Arguments:
        path_of_disc {str} -- path of the facebook datas

    Returns:
        list -- list of of path of json containing the infos given by facebook
    """
    # if not iterable:
    json_disc = []
    # path_disc = []
    # nom_disc = []
    for dossier in glob.glob(f'{path_of_disc}/*'):
        # nom_disc.append(dossier.split('\\')[-1].split('_')[0])
        # path_disc.append(dossier)
        for fichier in glob.glob(f'{dossier}/*'):
            if fichier.split('/')[-1] in ["photos", "gifs", "files",
                                          "videos", "audio"]:
                shutil.rmtree(fichier)
            elif fichier.split('/')[-1] != "message_1.json":
                print(fichier)
            else:
                # if iterable:
                #    yield fichier
                # else:
                json_disc.append(fichier)
    # if not iterable:
    return json_disc


def get_chat_friend_and_me(dict_disc: list) -> List[dict]:
    """Return only the discussions with one friend and me (only 2 peoples)

    Arguments:
        dict_disc {list} -- list of the dicts containing the discussions

    Returns:
        list -- list of all discussions with only two peoples (and me)
    """
    # if not gen:
    duo_convs = []
    for msg_json in dict_disc:
        with open(msg_json, 'r') as msg_json:
            dict_msg = json.load(msg_json)
        if (len(dict_msg['participants']) == 2 and
                dict_msg['is_still_participant']):
            # if gen:
            #    yield dict_msg
            # else:
            duo_convs.append(dict_msg)
    # if not gen:
    return duo_convs


def cleanContent(content: List[str]) -> List[str]:
    """Clean the words from the regex in settings (ex : hello... => hello ...)

    Arguments:
        content {list} -- sentence divided by words (into a list)

    Returns:
        [type] -- [description]
    """
    buffer = []
    new_content = []
    for word in content:
        matched = False
        for reg in SUBSTITUTES:
            try:
                if reg.match(word):
                    matched = True
                    regex = reg
            except TypeError:
                continue
        if matched:
            word_splitted = regex.split(word)
            buffer.append(word_splitted[1])
            buffer.append(word_splitted[2])
            new_content += buffer
        else:
            new_content.append(word)
    return new_content


def get_discussions(duo_convs: List[dict]) -> List[Tuple[str, List[str]]]:
    """Load discussion by sentences into a form of dialog
    msg_person1 / msg_person1 / msg_person2 / msg_person1
    => big_msg_person1 / msg_person2 / msg_person1

    Arguments:
        duo_convs {List[dict]} -- List of the dictionnaries containing the
                                    facebook dicussions

    Returns:
        List[tuple] -- List with all the dialog : [(person1, List[str]),
                                                    (person2, List[str]),
                                                    (person1, List[str]),
                                                    (person2, List[str])]
    """

    # if not iterable:
    all_discussions = []
    for friend_conv in duo_convs:
        participants_names = [person["name"]
                              for person in friend_conv['participants']]
        participants_names.remove('Pierre Snell')
        friend_name = participants_names[0].encode('latin1').decode('utf8')
        message = []
        discussion = []
        friend_conv["messages"] = list(reversed(friend_conv["messages"]))
        locuteur = friend_conv["messages"][0]["sender_name"]
        for msg_infos in friend_conv["messages"]:
            try:
                content = msg_infos["content"].encode('latin1').decode('utf8')
                content = content.split()
                content = cleanContent(content)
            except KeyError:
                continue
            sender_name = msg_infos["sender_name"]
            if sender_name == locuteur:
                if len(message) > 100:
                    continue
                if message:
                    message.append(NWL_token)
                message += content
            else:
                message.append(EOS_token)
                discussion.append((locuteur, message))
                message = content
                locuteur = sender_name
        # if iterable:
        #    yield discussion
        # else:
        if discussion:
            all_discussions.append(discussion)
    # if not iterable:
    return all_discussions


def make_pairs(discussions: List[Tuple[str, List[str]]]) -> List[Tuple[List[str], List[str]]]:
    """From the tuple of a discussion, load only the pairs, starting by friend

    Arguments:
        discussions {List[tuple]} -- List with all the dialog :
                                    [(person1, List[str]),
                                    (person2, List[str]),
                                    (person1, List[str]),
                                    (person2, List[str])]

    Returns:
        List[tuple] -- List of tuple with only question, answer.
                            answer is always the one of facebook data
    """
    pair_of_sentences = []
    for discuss in discussions:
        # print(discuss)
        if discuss[0][0] == "Pierre Snell":
            discuss = discuss[1:]
        for i in range(0, len(discuss)-1, 2):
            pair_of_sentences.append((discuss[i][1], discuss[i+1][1]))
    return pair_of_sentences
