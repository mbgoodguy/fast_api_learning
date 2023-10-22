from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from auth.base_config import current_user
from tasks.tasks import send_email_report_dashboard

router = APIRouter(prefix='/report')


@router.get('/dashboard')
def get_dashboard_report(background_tasks: BackgroundTasks, user=Depends(current_user)):
    send_email_report_dashboard(user.username)
    background_tasks.add_task(send_email_report_dashboard, user.username)
    return {
        'status': 200,
        'data': 'Письмо отправлено',
        'details': None
    }

