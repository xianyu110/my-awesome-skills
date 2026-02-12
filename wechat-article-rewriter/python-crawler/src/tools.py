"""
    工具模块，包含一些常用的工具函数，如保存内容到缓存文件等
    功能1: 
        save_cache(content)   # 保存内容到缓存文件


"""


# 保存内容到缓存文件, 用于调试
def save_cache(content):
    with open(r'src/cache/test_cache.txt', 'w', encoding='utf-8') as f:
        f.write(content)



