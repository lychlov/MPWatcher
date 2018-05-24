1、数据结构
----
### 文章表 ###
> 表名`wechat_article`

| 字段名              | 数据类型| 长度 | 说明       | 描述 |
|:-------------------|:-------|:-----|:--------- |:----|
|article_id|number|||文章id|
|title|varchat|||标题|
|author|varchat|||作者|
|summary|varchat|||文章简介|
|cover|varchat|||简介处贴图|
|content|clob|||内容|
|like_num|number|||点赞数|
|read_num|number|||阅读数|
|comment|json|||评论信息|
|url|varchat|||文章链接|
|source_url|varchat|||阅读原文 链接|
|record_time|date|||爬取时间|
|release_time|date|||发布时间|
|account|varchat|||公众号名|
|__biz|varchat|||公众号唯一参数 可关联公众号表|

