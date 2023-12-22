#### 本ツールはフォルダのネスト構造も対応されております

#### SourceCode を exe ファイル化の方法

python をインストールされた環境で順次以下のコマンドを実行

```
pip install Pillow

pip install PySimpleGUI

pip install pyinstaller

cd 本ソースコードのいるフォルダパス
(例：cd D:\Test)

pyinstaller Change_ImageDPI_ImageSize_Fin.py --noconsole
```

以上の手順で自分の環境で exe 化はできると思います。
