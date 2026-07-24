from apps.batch.services.news.config import classify_article
res = classify_article('엔비디아 H100 가격 급등')
print(res)
res2 = classify_article('삼성전자 HBM3E 수율 논란')
print(res2)
