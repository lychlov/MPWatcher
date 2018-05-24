from apis.use_api import get_article_info
from crawler.article_tasks import download_videos
import _thread
url = 'https://mp.weixin.qq.com/s?__biz=MzU0MjQ1ODQxMA==&mid=2247483940&idx=1&sn=8ad01dc2c4305993f861a7bea1f16137&chksm=fb1b1561cc6c9c7745c9eb4d5b7eb10e81eeec882b4c33fc4ada783b7ac20cbf00bea8896954&mpshare=1&scene=1&srcid=0507ZVlFoGCAsgxRyQ3Xdp80&pass_ticket=HWZMx5AHq59uTXZQp9X91Qxlbq0loKsy%2FEUaHDPvT1iJL%2FflpXc4bmButMhmEme3#rd'
# url = 'https://mp.weixin.qq.com/s?__biz=MzAwMDI2MjU1Ng==&mid=2650495904&idx=1&sn=4b980f1f42dd852fbd8b8079f5807f3c&chksm=82e45353b593da457efd8eaa2157b9a6a950f39dc21d3d9519cd4cf369f330370e8c5033bb08&mpshare=1&scene=1&srcid=0523vcBvLDobWeoXMAZjeU9b&pass_ticket=N0owVjmLJQsStOHKTn5v%2BLwmBqT5AvSKO6NQgn4yslQOaDmH3VIaaQJvEmMJK6OT#rd'

temp_dict = {"title": "政变四周年，曼谷反军方大示威今日正式爆发！",
             "summary": 'jianjie',
             "cover": "http://sdfsdf",
             "receive_time": "2018-05-23 23:23:23",
             "account": '泰国网'}
video_urls = ['https://v.qq.com/iframe/preview.html?vid=g0662k6xk0t&amp;width=500&amp;height=375&amp;auto=0']
picture_urls_temp = [
    'https://mmbiz.qpic.cn/mmbiz_png/2U1Ohu1dZsyLh2PlRV5ymhSDwicfAH1w4ow8lwNkS4TN5bpkibBB3ibNsP5t3Sk96VN3TI40CbLeRR4u2qs5R8aBA/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJPWiandMt7UNGibIXsJ2QelE8PGsyYLbfTnOsvyaETqsOl9KnYwfIR6yQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJLdGWUgyiascWSZf2dm5XdHs0kGLmlVytdYic9EFYeX3pN6pN4Y1yJfKA/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJXs4SbAUR7tmWuq91F07sJfiaOKLG1TNbZrAsbnFGzV4pYuKaiazhPBOg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_png/2U1Ohu1dZsyLh2PlRV5ymhSDwicfAH1w4jicSc4PYic3BepxHFKENpld90m11e9F0iavucibvUZ7ibYqVaasaN7aga0g/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJAdQz0T6dZibBoUKf8ziamqHkUTic0Fb8s4ia1Qv2mQQF9llkZCbuEb1IqQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJnTzYSve7TGeXXCEicxzuRK43zJcKf7td5omPoaMdHwl53NJ0boSkX4g/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJs0uDAia0EsuoFoasQc9Aa9V2icaPjPXWFibZBeretA9mzicKRVaic1JqBtw/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJRrralA7qyqsRicTHm9ubz3ibexiaiblvWpaYRZ7RJuLhvrCf0Pcost4pbQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/ENw5LI09ksyeibVR7EEpfOPmSxH69OWibTnmGbiaNajIq5JqPhgfLECAcu41WgoMfzVmeibckD5xhrEf4kIH8J2UnA/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_gif/nibxMsb16PQQiccxgtA7bxjNbzDs1BrpI7MX16pXEXcCaP6WBQsVJXRdm4oFXLvf27Pu7iabQicJaMr5otibgyFAMaQ/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJWgl0s6m2mNTfUbV8oTsBZxKyOJKBcRcFvCia7T9XSdbHL6gmweT3MQQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJA8oVvWKPbJT3VR9Wl8HLiciaDChkGXFesmgM1UPT3GaW6PfWQvPbbpNw/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJtpqCgosZ8icxdDuLr8HvAUvjtDODo0AwxmCX5QONphxQdwMxjicIoJMQ/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJZeuoEvbY4rYuwprzztpLZjMh9rkyRNj0yLpicsuCWpoawVibH0wpzLCg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJGYwhUnesuPib65aPVibJgT5YdtxSbgic6HFYSa6WgME5ibStXcKKVIy0Fg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJ3gpOR68dqdnp3BBaQGZ9cBpTmZsepzeNcDa8IK3DicUuHvht2qc7fLg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJFaIWBN9vRI8tPiatEFOibyn7WdJWCYW9c9HAslL5EE80Ud8CZeZm4mKg/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJG6SfLGOmvFuDvCWyXMfJXsiacQLva0TiaHuE0Vl7Yibn3qBIcuEZJ7n0w/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_gif/ENw5LI09ksyeibVR7EEpfOPmSxH69OWibTnmGbiaNajIq5JqPhgfLECAcu41WgoMfzVmeibckD5xhrEf4kIH8J2UnA/640?wx_fmt=gif',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJzGC04A0u33icNVs02dL9z6jxbIKnD47Y9JqUIfyxic8lHwnUBrkvLYRg/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJD4z3RpfibhBqKA421iaJSo3ic1UF3y1b9GTwBXWwAnuKx8mlr9Tg5Y91Q/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJqib113SYNsdIM0SF37kUibRMjvsmWs29mpFBdiavJI8XeXNk2EPkictAvQ/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/a76nL5zFMCqfKLBIJZ2X4n2dsmdZwvTxqoxHMwLOb5Yjqoqb7IajFdicKwe2xEft7oltZG9qoiaVNYuTtHgmh5bw/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJEAgSicxxCvNGicZQpQTXrRiaAfzmibaqyTsXqo4s7UicG0pZpn7LlIN70Qw/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_png/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJibNYSdUzfibpIKTL7dxusrP29JHzP8uctLgSMyXqgoOwD8Q2SaOuC49Q/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_png/yyRO8jtwmzPrTxwABSgXTzXw5WCqTialynibVPmrIwIpVVsibaLYbVqS64oicJXX8tUEGibvdOM783cUGfh5MT962UQ/640?wx_fmt=png',
    'https://mmbiz.qpic.cn/mmbiz_jpg/MhfGKpsUKDFCYeU94ibdCtCB3VhGgoeoJdOicl3nicsvsY1hc1lSibwdQb7YYm6tl0UUF8rkMmKgfb66cQYnsJjfUA/640?wx_fmt=jpeg',
    'https://mmbiz.qpic.cn/mmbiz_jpg/nSCFwRAl6zs1UndkfCmghhRXHZ9tmI2In35oobHhyicJVtN7ECBnuV1KAia73Pj3XBACfyev3ePlUF839WaCsX8Q/640?wx_fmt=jpeg']

# download_videos(temp_dict, '/Users/zhikuncheng/devspace/IMG_STORE', video_urls)
# _thread.start_new_thread(download_videos, (temp_dict, '/Users/zhikuncheng/devspace/IMG_STORE', video_urls))

res = get_article_info(url)
print(res)