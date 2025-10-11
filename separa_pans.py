from pathlib import Path
import zipfile

# Caminho base onde os zips serão criados
output_dir = Path("/media/anaciconelle/32325044-d805-46b1-b3b7-55fe691ae743/MaChironData/Pans-Zipadas")
output_dir.mkdir(parents=True, exist_ok=True)

# Pasta onde estão os .txt (ex: Alphaville_lista_imgs.txt)
txt_dir = Path("/home/anaciconelle/Desktop/Doutorado/exames_por_origem")

for txt in sorted(txt_dir.glob("*_lista_imgs.txt")):
    bairro = txt.stem.split("_", 1)[0]
    zip_path = output_dir / f"{bairro}.zip"

    # Conta quantas linhas válidas há no txt
    with txt.open("r", encoding="utf-8", errors="ignore") as f:
        linhas = [l.strip() for l in f if l.strip()]
    total = len(linhas)

    print(f"\n🔄 Processando bairro: {bairro}  ({total} arquivos listados)")

    missing = []
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for line in linhas:
            src = Path(line)
            if src.is_file():
                # Adiciona o arquivo ao zip (apenas o nome)
                zf.write(src, arcname=src.name)
            else:
                missing.append(str(src))

    print(f"📦 ZIP criado: {zip_path}")
    if missing:
        print(f"⚠️  {len(missing)} arquivos não encontrados:")
        for m in missing[:5]:
            print("  -", m)
        if len(missing) > 5:
            print("  ...")
    else:
        print("✅ Todos os arquivos encontrados e zipados com sucesso!")

print("\n🚀 Finalizado! Todos os zips foram salvos em:")
print(f"   {output_dir}")
