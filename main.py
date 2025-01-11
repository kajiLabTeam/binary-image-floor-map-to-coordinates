from PIL import Image
import datetime

# 二値画像を読み込む
image_path = "./imgs/14号館5F.png"  # 二値画像ファイルへのパス
floor_id = "01F8VYXK67BGC1F9RP1E4S9YTV"  # 適切なfloor_idを指定してください

# 画像を開く
image = Image.open(image_path)
if image.mode != "L":
    print("画像がグレースケールではありません。グレースケールに変換します。")
    image = image.convert("L")

width, height = image.size

# ピクセル値を取得
pixels = image.load()

# 現在のタイムスタンプ
current_timestamp = datetime.datetime.now().isoformat()

# SQL文の格納リスト
values = []

# バッチサイズ（1ファイルあたりの行数）
batch_size = 2000000
batch_count = 0  # ファイル番号

# 座標ごとに値を収集
for y in range(height):
    for x in range(width):
        # ピクセル値をチェック（黒: 0, 白: 255）
        is_walkable = pixels[x, y] > 127  # 127を閾値として扱う
        values.append(f"({x}, {y}, {str(is_walkable).upper()}, '{floor_id}')")

        # バッチが満たされた場合
        if len(values) == batch_size:
            # SQL文を生成
            sql = (
                "INSERT INTO coordinates (x, y, is_walkable, floor_id) VALUES\n" +
                ",\n".join(values) +
                ";"
            )

            # ファイルに保存
            batch_count += 1
            file_name = f"7-insert_coordinates_batch_{batch_count}.sql"
            try:
                with open(file_name, "w") as f:
                    f.write(sql)
                print(f"SQLバッチファイルを作成しました: {file_name}")
            except Exception as e:
                print(f"ファイルの保存に失敗しました: {e}")

            # valuesをリセット
            values = []

# 残りのデータを書き込む
if values:
    batch_count += 1
    sql = (
        "INSERT INTO coordinates (x, y, is_walkable, floor_id) VALUES\n" +
        ",\n".join(values) +
        ";"
    )
    file_name = f"7-insert_coordinates_batch_{batch_count}.sql"
    try:
        with open(file_name, "w") as f:
            f.write(sql)
        print(f"最後のSQLバッチファイルを作成しました: {file_name}")
    except Exception as e:
        print(f"ファイルの保存に失敗しました: {e}")

print("すべてのSQLバッチファイルの生成が完了しました。")
