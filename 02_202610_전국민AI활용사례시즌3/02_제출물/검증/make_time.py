"""시간 비교 기록표 만들기. 책 폴더는 읽기만 하고, 결과는 이 폴더에만 쓴다.

python -I make_time.py hand            손 정리 기록표 (묶음 1)
python -I make_time.py check AI결과.json  AI 결과 확인 기록표 (묶음 2)
"""
import json, sys
from pathlib import Path

MANUAL = Path(r"D:\11.my_projects\07.book\02.wikidocs_blog\book\dots\frames\manual")
HERE = Path(__file__).parent
N = 18
EXCLUDE = {"스크린샷 2026-10-09 141555.png", "스크린샷 2026-10-09 133952.png"}  # 오류 검사 B 표본


def pick(folder):
    files = sorted(p for p in (MANUAL / folder).glob("*.png") if p.name not in EXCLUDE)
    return [{"id": f"{i+1:02d}", "name": p.name, "path": str(p), "url": p.as_uri()} for i, p in enumerate(files[:N])]


SETS = {"hand": ("12.초안수정", "묶음 1: 손으로 정리"), "check": ("16.주소전환", "묶음 2: AI 결과 확인·고치기")}
# 10-09 색인의 그 시간대 한 줄 (사람과 AI에게 같은 단서로 준다)
CLUE = {"12.초안수정": "11:02~11:45 초안 수정, Gmail 저장, 하루·강사 재수정, 받는사람·참조, 링크",
        "16.주소전환": "13:39~14:49 주소 전환, 초안 주소 변경, 다온 문의 발송·수신, 고객 회신 보완·본문·발송·수신, 최민지 답장 작성·발송, 캘린더(한지우 이름)"}

mode = sys.argv[1]
folder, title = SETS[mode]
items = pick(folder)
if mode == "check":
    ai = {r["name"]: r for r in json.loads((HERE / sys.argv[2]).read_text(encoding="utf-8"))["items"]}
    for it in items:
        it["memo"] = ai.get(it["name"], {}).get("memo", "")
        it["mask"] = ai.get(it["name"], {}).get("mask", "")
(HERE / f"시간비교_{mode}_목록.json").write_text(json.dumps({"folder": folder, "items": items}, ensure_ascii=False, indent=1), encoding="utf-8")
tpl = (HERE / "time_template.html").read_text(encoding="utf-8")
data = json.dumps({"mode": mode, "title": title, "folder": folder, "clue": CLUE[folder], "items": items}, ensure_ascii=False)
name = "시간비교_1_손정리.html" if mode == "hand" else "시간비교_2_AI확인.html"
(HERE / name).write_text(tpl.replace("__DATA__", data), encoding="utf-8")
print(name, len(items))
