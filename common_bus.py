import random

# 随机生成 10 组公交车数据
def get_bus_info(station):
    info = []
    for random_bus in range(10):
        bus_name = f"W{random.randint(1, 100)}"
        bus_arrival_time = random.randint(1, 30)
        bus_info = f"{bus_name} 还有 {bus_arrival_time} 分钟到达 {station}"
        info.append({bus_name: bus_info})
    return info

def discover_reports():
    """查找所有的测试报告"""
    import pathlib
    report_dir = pathlib.Path(__file__).parent / 'output'
    reports = [f.name for f in report_dir.iterdir() if f.suffix == '.html']
    return reports