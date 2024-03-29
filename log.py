from multiprocessing import Process, Queue
from logging.handlers import RotatingFileHandler, QueueHandler
import logging, os, psutil


def kill_process_by_pid(pid):
    try:
        # 使用PID获取进程对象
        process = psutil.Process(pid)
        # 终止进程
        print(f"killing {pid}")
        process.terminate()
        print(f"killed {pid}")
    except psutil.NoSuchProcess:
        print(f"No process with PID {pid}")


def set_logger(log_name="Logger", log_level="INFO", path = "common.log"):  # common logger
    """
    log_level =  {"DEBUG", "ERROR", "INFO"}
    """
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            pass
        
    # define logging level
    log_level_mappings = {"DEBUG": logging.DEBUG, "ERROR": logging.ERROR,}
    log_level = log_level_mappings.get(log_level.upper(), logging.INFO)
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)

    # define logging formatter
    # formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    # define file_handler
    file_handler = RotatingFileHandler(filename=path, maxBytes=1024**3,
                                        backupCount=2, encoding="utf-8")  #单log maxBytes字节，最多保存两条历史log
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    
    # define stream_handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(log_level)
    
    # add handler
    logger.addHandler(file_handler) 
    logger.addHandler(stream_handler)
    return logger

    
class QueueLogger:  # win multi-processing logger
    def __init__(self, log_path="./queue.log",log_level = "INFO", use_queue = True) -> None:
        self.log_path = log_path
        self.log_level = log_level
        if use_queue:
            self.loggerQueue = Queue()
            self.pidQueue = Queue()
            

    def kill_all_pid(self):  # when logger_process get error message
        pid_list = []
        while not self.pidQueue.empty():
            pid_list.append(self.pidQueue.get())
        for pid in pid_list[::-1]:
            kill_process_by_pid(pid)  # kill by LIFO 


    def _sub_logger_process(self):  # 在子进程从共享队列中获取message并处理输出
        queue = self.loggerQueue
        logger = set_logger('queueLogger',self.log_level, self.log_path)
        # run forever
        while True:
            # consume a log message, block until one arrives
            message = queue.get()
            if message is None:  # check for shutdown
                break
            # log the message
            #print(f"{message.levelname} process name:{message.processName}, process id:{message.process}")  # 可获取message所在进程id
            logger.handle(message)

            if message.levelname == "ERROR":  # kill all pids if error
                self.kill_all_pid()
                break
    
    def start_logger_process(self):  # 开启queue message处理进程
        logger_p = Process(target=self._sub_logger_process, args=())
        logger_p.start()
    
    def shutdown_logger_process(self):
        self.loggerQueue.put(None)

    def init_queue_log(self, error_kill = True):
        # add shared queue handler
        queue = self.loggerQueue
        sub_logger = logging.getLogger('queueLogger')
        queue_handler = QueueHandler(queue)  # add a handler that uses the shared queue
        sub_logger.addHandler(queue_handler)
        sub_logger.setLevel(logging.DEBUG)  # 设置子进程记录的日志等级
        if error_kill:
            self.pidQueue.put(os.getpid())  # 存入pid，log为error时清理所有pid
        return sub_logger