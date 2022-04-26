import os
import shutil
import requests
from tqdm import tqdm


class Downloader:
    def __init__(self, url):
        """
        :param url: ダウンロードリンク
        """
        self.url = url  # https://ladse.eng.isas.jaxa.jp/benchmark/Mazda_CdMOBP.zip
        self.filename = os.path.basename(url)  # Mazda_CdMOBP.zip


    def __call__(self):
        print("Downloading...")
        file_size = int(requests.head(self.url).headers["content-length"])
        request = requests.get(self.url, stream=True)  # ダウンロード
        progress = tqdm(total=file_size, unit="B", unit_scale=True)

        # もし、リクエストに成功したならば、保存先パスにダウンロードファイルを保存
        if request.status_code == 200:
            with open("./"+self.filename, "wb") as file:
                for chunk in request.iter_content(chunk_size=1024):
                    file.write(chunk)
                    progress.update(len(chunk))
                progress.close()
                print("Download complete!")
            # 展開
            shutil.unpack_archive(self.filename, "./")
