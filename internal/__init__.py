# internal保存
#现在，假设你的组织为你提供了 app/internal/admin.py 文件。
# 它包含一个带有一些由你的组织在多个项目之间共享的管理员路径操作的 APIRouter。
# 对于此示例，它将非常简单。但是假设由于它是与组织中的其他项目所共享的，因此我们无法对其进行修改，
# 以及直接在 APIRouter 中添加 prefix、dependencies、tags 等：
# from fastapi import APIRouter
# router = APIRouter()
# @router.post("/")
# async def update_admin():
#     return {"message": "Admin getting schwifty"}
# 但是我们仍然希望在包含 APIRouter 时设置一个自定义的 prefix，以便其所有路径操作以 /admin 开头，
# 我们希望使用本项目已经有的 dependencies 保护它，并且我们希望它包含自定义的 tags 和 responses。
# 我们可以通过将这些参数传递给 app.include_router() 来完成所有的声明，而不必修改原始的 APIRouter：
## 具体查看官方文档：https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/