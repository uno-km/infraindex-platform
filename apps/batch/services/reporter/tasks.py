from celery_app import celery_app
from apps.batch.services.reporter.error_reporter import run_daily_error_report

@celery_app.task(name="reporter.daily_error_report")
def task_daily_error_report():
    """
    매일 아침 8시에 실행되어 미발송(is_sent=False) 에러를 수집,
    LLM으로 요약 후 텔레그램으로 발송하는 배치 태스크.
    """
    run_daily_error_report()
    return "Daily Error Report Finished."
