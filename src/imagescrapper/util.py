import os
import re
import zipfile
from urllib import request

import wget


def download_chromedriver():
    def get_latestversion(version):
        url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + str(
            version
        )
        response = request.get(url)
        version_number = response.text
        return version_number

    def download(download_url, driver_binaryname, target_name):
        # download the zip file using the url built above
        latest_driver_zip = wget.download(download_url, out="./temp/chromedriver.zip")

        # extract the zip file
        with zipfile.ZipFile(latest_driver_zip, "r") as zip_ref:
            zip_ref.extractall(
                path="./temp/"
            )  # you can specify the destination folder path here
        # delete the zip file downloaded above
        os.remove(latest_driver_zip)
        os.rename(driver_binaryname, target_name)
        os.chmod(target_name, 755)

    if os.name == "nt":
        replies = os.popen(
            r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        ).read()
        replies = replies.split("\n")
        for reply in replies:
            if "version" in reply:
                reply = reply.rstrip()
                reply = reply.lstrip()
                tokens = re.split(r"\s+", reply)
                fullversion = tokens[len(tokens) - 1]
                tokens = fullversion.split(".")
                version = tokens[0]
                break
        target_name = "./bin/chromedriver-win-" + version + ".exe"
        found = os.path.exists(target_name)
        if not found:
            version_number = get_latestversion(version)
            # build the donwload url
            download_url = (
                "https://chromedriver.storage.googleapis.com/"
                + version_number
                + "/chromedriver_win32.zip"
            )
            download(download_url, "./temp/chromedriver.exe", target_name)
            return target_name

    elif os.name == "posix":
        reply = os.popen(r"chromium --version").read()

        if reply != "":
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[1]
            tokens = fullversion.split(".")
            version = tokens[0]
        else:
            reply = os.popen(r"google-chrome --version").read()
            reply = reply.rstrip()
            reply = reply.lstrip()
            tokens = re.split(r"\s+", reply)
            fullversion = tokens[2]
            tokens = fullversion.split(".")
            version = tokens[0]

        target_name = "./bin/chromedriver-linux-" + version
        print("new chrome driver at " + target_name)
        found = os.path.exists(target_name)
        if not found:
            version_number = get_latestversion(version)
            download_url = (
                "https://chromedriver.storage.googleapis.com/"
                + version_number
                + "/chromedriver_linux64.zip"
            )
            download(download_url, "./temp/chromedriver", target_name)
