import os


def check_structure():
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("temp/autoanswer_DB"):
        os.mkdir("temp/autoanswer_DB")