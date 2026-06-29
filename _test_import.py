
import sys
sys.path.insert(0, '.')
from app.api.comments import router
print("Comments API loaded OK")

from app.core.deps import get_current_user_optional
print("get_current_user_optional loaded OK")

# Check if the create_comment function uses current_user properly
import inspect
from app.api.comments import create_comment
sig = inspect.signature(create_comment)
print(f"create_comment signature: {sig}")
