import webbrowser
from pathlib import Path
from PIL import Image
import PySimpleGUI as sg
from decimal import Decimal, ROUND_HALF_UP

source_code = {
    'SourceCode_URL': 'https://github.com/Gladiale/Change_ImageDPI_ImageSize',
    'SourceCode_Font': ('Courier New', 11, 'underline')
}

size = (5, 5)

left = 185
right = 0
top = 0
bottom = 0

# Themeの設定
sg.theme('Dark Red')

# レイアウトを作成(PySimpleGUIのレイアウトはリスト形式で記述します)
layout = [
    [sg.Text('処理したいフォルダを選んでください：')],
    [sg.InputText(), sg.FolderBrowse(key='router')],
    [sg.Text('変更したいDPIを設定'),sg.InputText(size=size, key='dpiChange')],
    [sg.Text('処理したいファイル種類'), sg.Checkbox("JPG", key="C_JPG", default=True),
    sg.Checkbox("JPEG", key="C_JPEG", default=True), sg.Checkbox("PNG", key="C_PNG", default=True), sg.Checkbox("TGA", key="C_TGA", default=False)],
    [sg.Radio('DPI情報ロストのファイルを', group_id='runWay', default=True, key="addDPI"),
    sg.InputText('200', key="dpiSetDefault", size=size), sg.Text('DPIと見なして処理')],
    [sg.Radio("DPI情報ロストのファイルは何の処理もしないままPASS", group_id='runWay', key="noneDPI")],
    [sg.Submit(button_text='実行ボタン', key="startBtn"), sg.Text('ver 1.03', pad=((left,right),(top,bottom)), text_color='deeppink'),
    sg.Text('(SourceCode)', tooltip=source_code['SourceCode_URL'], enable_events=True, font=source_code['SourceCode_Font'], text_color='violet', key=f'URL {source_code["SourceCode_URL"]}')]
]

# windowオブジェクト生成
window = sg.Window('アニメ用画像DPI(原画サイズ)変更ツール', layout)

# windowを表示
while True:
    event, values = window.read()

    # 右上のXボタン押した時にウインドウ画面を閉じる
    if event is None:
        break

    if event.startswith("URL "):
        url = event.split(' ')[1]
        webbrowser.open(url)

    if event == 'startBtn':
        _dir = values['router']
        if _dir == '':
            sg.Popup('Error: ファイルパースが選んでいません')
            break

        if values['dpiChange'] == '':
            sg.Popup('Error: 変更したいDPIが入力されていません')
            break

        dpiChange = int(values['dpiChange'])

        addDPI = values['addDPI']
        noneDPI = values['noneDPI']

        Boolean_JPG = values['C_JPG']
        Boolean_JPEG = values['C_JPEG']
        Boolean_PNG = values['C_PNG']
        Boolean_TGA = values['C_TGA']

        match Boolean_JPG:
            case True:
                _extension = ['.jpg']
            case _:
                _extension = []
        match Boolean_JPEG:
            case True:
                _extension.append('.jpeg')
            case _:
                pass
        match Boolean_PNG:
            case True:
                _extension.append('.png')
            case _:
                pass
        match Boolean_TGA:
            case True:
                _extension.append('.tga')
            case _:
                pass

        if len(_extension) == 0:
            sg.Popup("最低一つのファイル種類は選んでください")
            break
        
        # print(_extension)
        _files = [i for i in Path(_dir).glob('**/*.*') if i.suffix in _extension]

        # ** プログレスバーを生成 **
        BAR_MAX = len(_files)
        layoutProgressBar = [
            [sg.Text('進捗状況', text_color='violet'), sg.Text(key="result", text_color='violet')],
            [sg.ProgressBar(BAR_MAX, orientation='h', size=(40,20), key='-PROG', bar_color=('aqua','navy'))],
            [sg.Cancel()]
        ]
        windowProgress = sg.Window('進捗状況', layoutProgressBar)

        if BAR_MAX == 0:
            sg.Popup('Error: 指定したファイルが見つかりません')
            break
        
        # エラー情報を格納
        error_message = []

        for index, file_path in enumerate(_files):
            # timeoutを設定すると、設定時間後.read()を抜けることができます。単位はミリ秒
            eventProgress, valuesProgress = windowProgress.read(timeout=1)

            # print(index, file_path)

            try:
                # ** DPI変更のmainプログラム **
                img = Image.open(file_path)
                # 画像にDPI情報が含まない場合の処理
                if 'dpi' not in img.info.keys():
                    match addDPI:
                        case True:
                            if values['dpiSetDefault'] == '':
                                sg.Popup('Error: DPI情報ロストのファイルに対してデフォルトのDPIが設置されていません')
                                break
                            dpiSetDefault = int(values['dpiSetDefault'])
                            dpiSource = dpiSetDefault
                            
                            # decimalモジュールを採用（四捨五入）
                            width = Decimal(str(float(dpiChange * img.width / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                            height = Decimal(str(float(dpiChange * img.height / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

                            img_resized = img.resize((int(width), int(height)))
                            img_resized.save(file_path, dpi = (dpiChange, dpiChange), quality=95)

                            img.close()
                            img_resized.close()
                        case _:
                            pass
                # 画像のDPIが0の場合の処理
                elif img.info['dpi'][0] == 0:
                    match addDPI:
                        case True:
                            if values['dpiSetDefault'] == '':
                                sg.Popup('Error: DPI情報ロストのファイルに対してデフォルトのDPIが設置されていません')
                                break
                            dpiSetDefault = int(values['dpiSetDefault'])
                            dpiSource = dpiSetDefault
                            
                            # decimalモジュールを採用（四捨五入）
                            width = Decimal(str(float(dpiChange * img.width / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                            height = Decimal(str(float(dpiChange * img.height / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

                            img_resized = img.resize((int(width), int(height)))
                            img_resized.save(file_path, dpi = (dpiChange, dpiChange), quality=95)

                            img.close()
                            img_resized.close()
                        case _:
                            pass
                else:
                    dpiSource = img.info['dpi'][0]

                    if dpiSource == dpiChange:
                        img.close()
                    else:
                        # decimalモジュールを採用（四捨五入）
                        width = Decimal(str(float(dpiChange * img.width / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)
                        height = Decimal(str(float(dpiChange * img.height / dpiSource))).quantize(Decimal('0'), rounding=ROUND_HALF_UP)

                        img_resized = img.resize((int(width), int(height)))
                        img_resized.save(file_path, dpi = (dpiChange, dpiChange), quality=95)
                        # print(id(img), id(img_resized))

                        img.close()
                        img_resized.close()
            except Exception as e:
                error_message.append(e)

            target = str(file_path).split('\\')[-1]
            windowProgress["result"].update(target)

            # キャンセルボタンか、ウインドウの右上のxが押された場合の処理
            if eventProgress == 'Cancel' or eventProgress == sg.WIN_CLOSED:
                sg.Popup('処理がキャンセルしました')
                break

            # プログレスバーの表示更新（カウンタ(index)をインクリメントして表示）
            windowProgress['-PROG'].update(index + 1)
        windowProgress.close()

        if index + 1 == BAR_MAX:
            match len(error_message):
                case 0:
                    sg.Popup(f'全プロセスを無事終了しました！\n今回処理したファイルの数は：{BAR_MAX} 件になります')
                case _:
                    sg.PopupError(f'以下{len(error_message)}件の処理は失敗になります：\n{error_message}')

# ウインドウの破棄と終了
window.close()