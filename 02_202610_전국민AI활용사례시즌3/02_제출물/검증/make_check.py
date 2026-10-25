"""오류 검사 확인표 만들기. 책 폴더는 읽기만 하고, 결과는 OUT 폴더에만 쓴다."""
import json, random, re, sys
from pathlib import Path

BOOK = Path(r"D:\11.my_projects\07.book\02.wikidocs_blog\book\dots")
MANUAL = BOOK / "frames" / "manual"
OUT = Path(sys.argv[1])
SEED = 20261023
rng = random.Random(SEED)

# A. 10-10 색인 설명: 파일별 한 줄
rows, folder = [], None
for line in (MANUAL / "INDEX-20261010.md").read_text(encoding="utf-8").splitlines():
    m = re.match(r"\|\s*([^|]*?)\s*\|\s*(\d{6})\s*\|\s*(.+?)\s*\|\s*$", line)
    if not m:
        continue
    if m.group(1):
        folder = m.group(1)
    p = MANUAL / folder / f"스크린샷 2026-10-10 {m.group(2)}.png"
    if p.exists():
        rows.append({"path": str(p), "folder": folder, "desc": m.group(3)})
A = rng.sample(rows, 20)

# B. 폴더 분류: 10-10 색인 밖의 직접 캡처
indexed = {r["path"] for r in rows}
caps = sorted(str(p) for p in MANUAL.glob("*/**/*.png")
              if "38.일요일" not in p.parts and not p.name.startswith(("frame-", "sheet-"))
              and str(p) not in indexed)
B = [{"path": p, "folder": str(Path(p).relative_to(MANUAL).parent)} for p in rng.sample(caps, 15)]

# C. 영상에서 뽑은 장면
frames = sorted(str(p) for p in MANUAL.glob("38.일요일/**/frame-*.png"))
frames += sorted(str(p) for p in (BOOK / "frames").glob("00-02*/*.png"))
C = [{"path": p, "folder": str(Path(p).parent.relative_to(BOOK / "frames"))} for p in rng.sample(frames, 15)]

# D. 책에 실린 그림 (최종 결과의 가림)
refs = sorted({m for f in (BOOK / "chapters").glob("*.md")
               for m in re.findall(r"!\[[^\]]*\]\(\.\./images/([^) ]+)", f.read_text(encoding="utf-8"))})
D = [{"path": str(BOOK / "images" / r), "folder": "책 본문"} for r in rng.sample(refs, 10)]

Q = {
    "A": ["노란 상자의 한 줄 설명(AI가 쓴 메모)이 그림 내용과 맞나", "이 그림이 폴더 이름의 단계에서 찍은 화면인가"],
    "B": ["이 그림이 폴더 이름의 단계에서 찍은 화면인가"],
    "C": ["이 장면이 후보 폴더 이름의 구간에서 나온 것인가", "글자를 읽을 수 있을 만큼 선명한가"],
    "D": ["가려야 할 것(프로필, 계정·메일 주소, 개인 메일 목록, 실명)이 보이지 않나"],
}
TITLE = {"A": "AI가 쓴 색인 설명 (10-10 캡처)", "B": "최종 장면 폴더 (사람이 넣고 AI가 바로잡은 결과, 건너뛰어도 됨)",
         "C": "AI가 영상에서 뽑은 장면", "D": "책에 실린 그림의 가림 (최종 결과)"}
items = [{"id": f"{k}{i+1:02d}", "group": k, **it} for k, g in zip("ABCD", (A, B, C, D)) for i, it in enumerate(g)]
for it in items:
    it["url"] = Path(it["path"]).as_uri()

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "오류검사_표본.json").write_text(json.dumps({"seed": SEED, "questions": Q, "titles": TITLE, "items": items},
                                                ensure_ascii=False, indent=1), encoding="utf-8")
tpl = (Path(__file__).parent / "check_template.html").read_text(encoding="utf-8")
data = json.dumps({"questions": Q, "titles": TITLE, "items": items}, ensure_ascii=False)
(OUT / "오류검사_확인표.html").write_text(tpl.replace("__DATA__", data), encoding="utf-8")
print(len(rows), len(caps), len(frames), len(refs), len(items))
