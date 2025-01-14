# py-fastApi

## local build
 # poetry install
 # poetry run uvicorn app.main:app --reload

## 테스트 명령어 
 # poetry run pytest test


# Group
id
name
desc

# Group Manager
group_id
manager_id

# Group member
id
group_id
user_id
status 가입(요청,승인,거절)
status ENUM('requested', 'approved', 'rejected'),

# User
id
name

# post
id
title
content

# Group Post
post_id
user_id
group_id

# Comment
id
title
par_id (comment id  루트면 null)
content
post_id
user_id

# notification ??

