# 전남 22개 시군 관광 활성화를 위한 AI 추천 플랫폼: TourAPI + RAG 기반 축제·여행지 큐레이션

- 시즌1 수상작 / 분야: 지역사회 문제해결을 위한 AI 활용 / ★ 시즌 최우수
- 원문: https://ai.software.kr/board/community/219
- 👤 하얀돌고래426 / 📅 2026-05-14 / 👁 조회 354
- 한 줄 소개: Claude Code와 함께 전남 22개 시군 관광 데이터를 큐레이션하는 AI 추천 플랫폼(jntour.site)을 1인 개발
- 활용 AI 도구: Claude code, OpenAI GPT-4o-mini(API)
- 본문 글자 수: 2276자 (공백 포함)
- 첨부파일:
  - [스크린샷 2026-05-14 오후 7.33.49.png](https://ai.software.kr/board/download/485)
  - [스크린샷 2026-05-14 오후 7.34.07.png](https://ai.software.kr/board/download/486)
  - [스크린샷 2026-05-14 오후 9.36.41.png](https://ai.software.kr/board/download/487)
  - [스크린샷 2026-05-14 오후 9.35.29.png](https://ai.software.kr/board/download/488)
  - [스크린샷 2026-05-14 오후 9.34.38.png](https://ai.software.kr/board/download/489)

## 본문 (게시판 원문 그대로)

① 어떤 상황에서 AI를 활용했나요?
전남에서 여행 갈 때마다 시군별 축제, 캠핑장, 여행지 정보가 한국관광공사 TourAPI, 지자체 홈페이지, 블로그에 죄다 흩어져 있어서 매번 똑같은 검색을 반복했습니다. TourAPI 4.0은 데이터가 풍부한데 raw JSON이라 일반 사용자가 그대로 쓸 수 있는 형태는 아니고요. "여수 5월 첫째 주에 가족이랑 갈 만한 축제랑 근처 캠핑장 묶어줘" 정도는 한 번에 답해주는 서비스가 있었으면 좋겠다 싶어서 직접 만들기로 했습니다.

② 어떤 AI를 어떻게 활용했나요?
Claude Code(Sonnet/Opus 4.7)랑 GPT-4o-mini를 같이 썼는데, 둘이 잘하는 게 달라서 자연스럽게 역할이 갈렸습니다.
Claude Code는 개발 파트너 역할이었습니다. FastAPI 엔드포인트 짜고, TourAPI의 searchFestival2랑 areaBasedList2를 같이 호출해서 축제+숙소를 묶는 로직 만들고, 코드 리뷰하고, 나중에 NAS에서 Ubuntu 서버로 이전할 때 Docker Compose랑 Cloudflare Tunnel 설정까지 같이 봐줬습니다.
GPT-4o-mini는 사용자 응답을 담당합니다. 자연어 질의에서 지역·카테고리·기간을 뽑아내고, RAG로 검색한 결과를 그대로 던지면 너무 딱딱하니까 추천 문장으로 다듬는 데 썼습니다.
RAG는 ko-sroberta 한국어 임베딩 + SQLite 벡터 스토어로 구성했습니다. 작업하다 보니 TourAPI 문서에 잘 나오지 않는 detailIntro2 필드에 축제 날짜가 들어있는 케이스가 꽤 많아서, 거기까지 긁어와서 인덱싱했습니다.

③ 활용 결과 어떤 변화가 있었나요?
주말 이틀 만에 MVP를 띄우고, 그 다음 한 주 동안 22개 시군 필터 칩, 축제 날짜 보강, 코스 저장 + 공유 URL + OG 미리보기까지 붙였습니다. 지금도 jntour.site에서 돌아가는 중입니다.
운영 들어가서 도움이 더 컸습니다. Docker Compose 자동 구성, Cloudflare Tunnel 라우팅, cron으로 매일 백업·헬스체크 거는 것까지 Claude Code랑 같이 셋업했고, NAS에서 Ubuntu 서버로 옮길 때는 30분 정도 끊겼는데 다행히 백업 덕에 데이터는 안 날아갔습니다.

④ 나만의 방식 또는 개선 포인트는 무엇인가요?
처음엔 그냥 "이거 만들어줘" 식으로 던졌는데, 프로젝트가 커질수록 같은 설명을 매번 반복하게 되더라고요. 그래서 코드 짜기 전에 룰 파일부터 만들어두는 습관이 생겼습니다.

CLAUDE.md — 프로젝트가 뭐고, 어떤 코딩 컨벤션을 쓰는지
design-system/MASTER.md — 색상·타이포·간격 디자인 토큰
workflow.md — 작업 크기별(Trivial/Small/Medium/Large) 에이전트 굴리는 방식

이렇게 깔아두니까 새 기능 붙일 때마다 컨텍스트를 다시 설명할 필요가 없어졌고, architect / planner / code-reviewer / security-reviewer를 병렬로 돌릴 수 있어서 혼자 개발하는데 옆에 PR 리뷰어가 한 명 더 있는 느낌이 됐습니다.

⑤ 다른 사람도 따라 할 수 있나요?
비전공자도 따라 할 수 있게 만들어 둔 구조입니다.
먼저 프로젝트 루트에 CLAUDE.md부터 씁니다. Claude Code 설치하고 어떤 서비스인지, 어떤 톤으로 코드를 쓸지, 어떤 스택을 쓸지 세 줄만 적어두면 절반은 끝났다고 봅니다. 새 대화창 열 때마다 같은 설명을 반복할 일이 없어지거든요.
다음은 작업 크기로 갈래를 나눕니다. 텍스트 수정 같은 자잘한 건 그냥 직접 던지고, 새 기능이나 리팩토링은 architect → planner → reviewer 순으로 multi-agent로 굴립니다. 이 분기 하나만 정해두면 일이 훨씬 가벼워집니다.
공공 API + RAG 패턴은 도메인만 바꿔서 재사용 가능합니다. TourAPI 자리에 문화재청 OpenAPI, 농산물유통정보, 지자체 공공시설 API를 끼우면 같은 구조로 맛집 큐레이션, 문화재 안내, 시설 예약 서비스로 갈 수 있습니다.
배포는 Cloudflare Tunnel + Docker Compose면 도메인비(연 만 원대)만 들고, 집에 안 쓰는 PC 한 대만 있으면 24시간 운영이 가능합니다.
도메인을 바꾸는 건 어렵지 않은데, 새 도메인의 공공데이터를 한 번씩 직접 파보는 단계(예: detailIntro2 같은 비공식 필드 발굴)는 결국 거쳐야 합니다. 이게 보통 가장 시간 걸리는 부분입니다.

사이트: https://jntour.site
