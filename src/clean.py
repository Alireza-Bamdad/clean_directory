import shutil
import sys
from pathlib import Path
from src.data import DATA_DIR
from src.utils.io import read_json
from loguru import logger


class OraganizeFiles:
    """
        This class is used to organize files in a directory by
        moving files into directories based on extension.
    """
    
    def __init__(self):
                
        ext_dir = read_json(DATA_DIR / 'extensions.json')
        self.extenstion = {}
        for dir_name, ext_list in ext_dir.items():
            for ext in ext_list:
                self.extenstion[ext] = dir_name

        # logger.info(f'{self.extenstion}')
    def __call__(self, directory):
        """ Organize files in a directory by moving them
            to sub directories based on extension.
        """
        
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f'{directory} does not exist')
        
        for file_path in directory.iterdir():
            # ignor directoris
            if file_path.is_dir():
                continue
            
            # ignor hidden file
            if file_path.name.startswith('.'):
                continue
                
            # move files
            if file_path.suffix not in self.extenstion:
                DEST_DIR = directory / 'other'
                
            else:
                DEST_DIR = directory / self.extenstion[file_path.suffix]
                
            DEST_DIR.mkdir(exist_ok=True)
            logger.info(f'moving {file_path} to {DEST_DIR}')
            shutil.move(str(file_path), str(DEST_DIR))
            


if __name__ == '__main__':
    org_files = OraganizeFiles()
    org_files(sys.argv[1])
    logger.info("Done")