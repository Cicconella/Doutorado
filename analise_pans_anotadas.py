
# Convert YOLO Label to csv:



# Na pasta: /var/home/aninha/Desktop/Doutorado/Dados/yolo_data, temos 3 subpastas (treino, teste, val) que contem 2 pastas: images e labels, na labels 1 arquivo txt por imagem com 1 linha por bbox no formato: class_id center_x center_y width height, por exemplo: 
# 0 0.502147 0.539265 0.382244 0.112971
# 0 0.504242 0.626951 0.444579 0.120904

# quero criar um arquivo csv para todo dataset com as colunas: box	score	class_name	filename, exemplo: [0.5727807934085528, 0.33512187426288925, 0.6384204301983119, 0.37643782248099644]	0.876635730266571	raiz residual	173496323_2_34_residual.png

# BBox no formato padrao papiron yolo -> xyxy (labels)
# BBox no formato usado deploy-papiron/odpv -> yxyx (csv)


#!/usr/bin/env python3
from pathlib import Path
import csv
import pandas as pd

# ======= CONFIG =======
BASE = Path("/var/home/aninha/Desktop/Doutorado/Dados/yolo_data")
SPLITS = ["treino", "teste", "val"]
CLASSNAMES_CSV = Path("/var/home/aninha/Desktop/Doutorado/Dados/yolo_data/yolo_classnames.csv")
OUT_CSV = BASE / "dataset_boxes_yxyx.csv"
IMG_EXTS = [".jpg", ".jpeg", ".png", ".bmp", ".JPG", ".JPEG", ".PNG", ".BMP"]
# ======================

def load_classnames(path: Path) -> dict:
    """
    Lê CSV com cabeçalho: class_id,class_name
    Constrói {id:int -> name:str}
    """
    df = pd.read_csv(path, dtype={"class_id": "int64", "class_name": "string"})
    df["class_name"] = df["class_name"].astype(str).str.strip()
    return {int(row["class_id"]): row["class_name"] for _, row in df.iterrows()}

def yolo_cxcywh_to_xyxy(cx, cy, w, h):
    x1 = cx - w/2.0
    y1 = cy - h/2.0
    x2 = cx + w/2.0
    y2 = cy + h/2.0
    # clamp [0,1]
    x1 = max(0.0, min(1.0, x1))
    y1 = max(0.0, min(1.0, y1))
    x2 = max(0.0, min(1.0, x2))
    y2 = max(0.0, min(1.0, y2))
    return x1, y1, x2, y2

def xyxy_to_yxyx(x1, y1, x2, y2):
    return y1, x1, y2, x2

def find_image_for_label(images_dir: Path, stem: str) -> str:
    for ext in IMG_EXTS:
        cand = images_dir / f"{stem}{ext}"
        if cand.exists():
            return cand.name
    return f"{stem}.png"

def parse_label_line(line: str):
    """
    Aceita:
      - 5 valores: class cx cy w h
      - 6 valores: class cx cy w h score
    """
    parts = line.strip().split()
    if len(parts) < 5:
        return None
    cls_id = int(float(parts[0]))
    cx, cy, w, h = map(float, parts[1:5])
    score = parts[5] if len(parts) >= 6 else ""
    if score != "":
        try:
            score = float(score)
        except:
            pass
    return cls_id, cx, cy, w, h, score

def main():
    class_map = load_classnames(CLASSNAMES_CSV)

    rows = []
    for split in SPLITS:
        labels_dir = BASE / split / "labels"
        images_dir = BASE / split / "images"
        if not labels_dir.exists():
            continue

        for txt in labels_dir.glob("*.txt"):
            stem = txt.stem
            filename = find_image_for_label(images_dir, stem)

            with txt.open("r", encoding="utf-8") as f:
                for line in f:
                    parsed = parse_label_line(line)
                    if not parsed:
                        continue
                    cls_id, cx, cy, w, h, score = parsed

                    x1, y1, x2, y2 = yolo_cxcywh_to_xyxy(cx, cy, w, h)  # xyxy
                    yxyx = xyxy_to_yxyx(x1, y1, x2, y2)                # yxyx (deploy)

                    class_name = class_map.get(cls_id, str(cls_id))

                    rows.append({
                        "box": f"[{yxyx[0]}, {yxyx[1]}, {yxyx[2]}, {yxyx[3]}]",
                        "score": score,
                        "class_name": class_name,
                        "filename": filename
                    })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["box", "score", "class_name", "filename"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV gerado com {len(rows)} linhas em: {OUT_CSV}")

if __name__ == "__main__":
    main()
