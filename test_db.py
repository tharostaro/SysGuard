from database import init_db, save_metric, get_history
from logger import setup_logger

logger = setup_logger()

init_db()

save_metric("CPU", 15.5)
save_metric("RAM", 42.3)

logger.info("SysGuard database test completed")

print("\n[ DATABASE HISTORY ]")

for row in get_history():
    print(row)

print("\nTest completed!")
