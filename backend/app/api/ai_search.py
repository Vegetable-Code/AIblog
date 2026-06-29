from fastapi import APIRouter, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, desc, func
from fastapi import APIRouter, Depends, Query
from ..core.database import get_db
from ..models.post import Post
from ..models.category import Category
from ..models.tag import Tag
from typing import Optional

router = APIRouter(prefix="/ai", tags=["AI搜索"])

# 常见技术词和分类的映射
TECH_KEYWORDS = {
    "transformer": ["transformer", "attention", "self-attention", "bert", "gpt", "注意力机制"],
    "大模型": ["llm", "large language model", "gpt", "大模型", "语言模型", "chatgpt", "claude", "deepseek"],
    "机器学习": ["machine learning", "ml", "机器学习", "监督学习", "非监督学习", "强化学习"],
    "深度学习": ["deep learning", "dl", "深度学习", "cnn", "rnn", "lstm", "gan", "卷积神经网络"],
    "python": ["python", "flask", "fastapi", "django", "pytorch", "tensorflow", "numpy", "pandas"],
    "docker": ["docker", "container", "k8s", "kubernetes", "容器", "微服务"],
    "frontend": ["vue", "react", "javascript", "typescript", "css", "html", "tailwind", "frontend", "前端"],
    "database": ["mysql", "sql", "nosql", "redis", "mongodb", "postgresql", "数据库", "sqlalchemy"],
    "devops": ["devops", "ci/cd", "github actions", "jenkins", "连续集成", "自动化部署"],
    "algorithm": ["algorithm", "算法", "数据结构", "leetcode", "排序", "搜索"],
}

# 常见问题类型的固定回答
FAQ = {
    "你是谁": "我是这个博客的 AI 助手，可以帮你搜索相关技术文章。试试问我“Transformer是什么”或“怎么学 Python”！",
    "能做什么": "我能帮你搜索博客中的技术文章！只要输入你感兴趣的技术词或问题，我就能找到相关的内容。比如“怎么学深度学习”、“Docker入门”等。",
    "你好": "你好！欢迎来到 AI 工程师博客，有什么技术问题想了解吗？输入你的问题，我帮你搜索相关文章！",
}

@router.get("/search")
def ai_search(
    q: str = Query(..., min_length=1, max_length=200, description="\u7528\u6237\u95ee\u9898"),
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    query = q.strip().lower()

    # 检查是否是常见问题
    for key, answer in FAQ.items():
        if key in query:
            return {"answer": answer, "articles": [], "is_faq": True}

    # 扩展搜索词
    search_terms = [query]
    for tech, keywords in TECH_KEYWORDS.items():
        for kw in keywords:
            if kw in query:
                search_terms.extend(keywords)
                break

    # 去重
    search_terms = list(set(search_terms))

    # 构建搜索条件
    conditions = []
    for term in search_terms:
        conditions.append(Post.title.contains(term))
        conditions.append(Post.summary.contains(term))
        conditions.append(Post.content.contains(term))

    posts = (
        db.query(Post)
        .options(joinedload(Post.category), joinedload(Post.tags))
        .filter(Post.is_published == True)
        .filter(or_(*conditions))
        .order_by(desc(Post.is_top), desc(Post.published_at))
        .limit(limit)
        .all()
    )

    # 生成回答
    if not posts:
        return {
            "answer": f"对不起，没有找到与“{q}”相关的文章。请尝试其他关键词，或浏览首页文章列表。",
            "articles": [],
            "is_faq": False,
        }

    # 生成回答提示
    if len(posts) == 1:
        answer = f"找到 1 篇与“{q}”相关的文章："
    else:
        answer = f"找到 {len(posts)} 篇与“{q}”相关的文章："

    articles = []
    for post in posts:
        articles.append({
            "id": post.id,
            "title": post.title,
            "slug": post.slug,
            "summary": (post.summary or "")[:150],
            "category": post.category.name if post.category else None,
            "tags": [t.name for t in post.tags[:3]],
            "published_at": post.published_at.isoformat() if post.published_at else None,
        })

    return {
        "answer": answer,
        "articles": articles,
        "is_faq": False,
    }
