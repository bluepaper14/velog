import feedparser
import git
import os

# ✅ Velog RSS 주소 (지현님 계정)
rss_url = 'https://v2.velog.io/rss/@bluepaper14'

# 깃허브 레포지토리 경로
repo_path = '.'
posts_dir = os.path.join(repo_path, 'velog-posts')

# 폴더 없으면 생성
if not os.path.exists(posts_dir):
    os.makedirs(posts_dir)

# Git repository 로드
repo = git.Repo(repo_path)

# RSS 피드 파싱
feed = feedparser.parse(rss_url)

# 새 글 감지 및 저장
for entry in feed.entries:
    # 파일명 안전하게 변환
    file_name = entry.title.replace('/', '-').replace('\\', '-') + '.md'
    file_path = os.path.join(posts_dir, file_name)

    # 기존 파일 없을 때만 생성
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {entry.title}\n\n")
            f.write(entry.description)

        repo.git.add(file_path)
        repo.git.commit('-m', f"Add post: {entry.title}")

# 변경사항 푸시
repo.git.push()
