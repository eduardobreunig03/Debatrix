from django.contrib import admin
from django.urls import path
from .views import DebateAPIView, SaveDebateView
from .views import CommentAPIView
from .views import RunLLMView
from .views import delete_debate
from .views import  AddPercentageView, AveragePercentageView, GetPercentageView, DebateAPIView, SaveDebateView , SavePinnedDebatesView, GetPinnedDebatesView, UnpinDebateView, GetBotComment
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('debates/', DebateAPIView.as_view(), name="debates"),
    path('save_debate/', SaveDebateView.as_view(), name="save_debate"),
    path('comments/', CommentAPIView.as_view(), name="comments"),
    path('run_llm/', RunLLMView.as_view(), name='run_llm'),
    path('debates/<int:debate_id>/', delete_debate, name='delete_debate'),
    path('add_percentage/', AddPercentageView.as_view(), name='add_percentage'),
    path('average_percentage/<str:debate_id>/', AveragePercentageView.as_view(), name='average_percentage'),
    path('get_percentage/', GetPercentageView.as_view(), name='get_percentage'),
    path('pin_debate', SavePinnedDebatesView.as_view(), name='pin_debate'),
    path('get_pinned_debates/', GetPinnedDebatesView.as_view(), name='get_pinned_debates'),
    path('unpin_debate', UnpinDebateView.as_view(), name='unpin_debate'),
    path('get_ai_comment/', GetBotComment.as_view(), name='get_ai_comment'),
]

