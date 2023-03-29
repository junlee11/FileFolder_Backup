import shutil, schedule, time, os
from datetime import datetime
from datetime import timedelta

class BackupClass():
    def __init__(self):
        self.interval = 0
        self.FileFolder = ''
        self.src_path = ''
        self.tar_path = ''        
    
    def input_fun(self):
        self.interval = int(input('백업할 시간 간격(분) 입력 : '))
        self.FileFolder = int(input('백업대상 파일(0) 폴더(1) : '))
        self.src_path = input('백업할 대상의 경로 : ')
        self.tar_path = input('백업 저장되는 폴더 : ')
        self.delete_interval = int(input('삭제 기준 시간(시간) 입력 : '))
    
    def backup_job(self):
        str_now = datetime.now().strftime('%Y%m%d %H%M%S')
        last_name = self.src_path[self.src_path.rfind('\\') + 1:]
        
        if self.FileFolder == 0:
            #파일
            shutil.copy2(self.src_path, self.tar_path + '\\' + str_now + ' ' + last_name)
        elif self.FileFolder == 1:
            #폴더
            shutil.copytree(self.src_path, self.tar_path + '\\' + str_now + ' ' + last_name)
        
        self.delete_job()
    
    def delete_job(self):
                
        for name in os.listdir(self.tar_path):
            if os.path.isfile(self.tar_path + '\\' + name) and self.chk_bool_time(name[name.rfind('\\')+1:]):
                os.remove(self.tar_path + '\\' + name)
            elif not os.path.isfile(self.tar_path + '\\' + name) and self.chk_bool_time(name[name.rfind('\\')+1:]):
                shutil.rmtree(self.tar_path + '\\' + name)
            
    def chk_bool_time(self, name) -> bool:
        name = name[:15]
        name_time = datetime.strptime(name, '%Y%m%d %H%M%S')
        if (datetime.now() - timedelta(self.delete_interval)) > name_time:
            return True
        else :
            return False

if __name__ == '__main__':
    cls = BackupClass()    
    cls.input_fun()
    cls.backup_job()
    schedule.every(cls.interval).minutes.do(cls.backup_job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)