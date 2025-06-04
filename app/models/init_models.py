from app.models.user import User
from app.models.post import Post, Comment, Like

User.update_forward_refs()
Post.update_forward_refs()
Comment.update_forward_refs()
Like.update_forward_refs()
