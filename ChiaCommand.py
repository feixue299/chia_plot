import glob
import os.path
import platform


class ChiaCommand:
    @staticmethod
    def getChiaPath():
        return ChiaCommand.getChiaLocationPath() + "chia"

    @staticmethod
    def getChiaLocationPath():
        if platform.system().lower() == 'windows':
            print("windows")
            path = os.getenv('LOCALAPPDATA')
            chia_path = path + "\\chia-blockchain\\app-?.?.?\\resources\\app.asar.unpacked\\daemon\\"
            result = ChiaCommand.search(chia_path, ".exe")
            return result[0] if len(result) > 0 else None
        else:
            print("mac os")
            return "/Applications/Chia.app/Contents/Resources/app.asar.unpacked/daemon/"

    @staticmethod
    def search(files, file_format='.png'):
        def _get_all_filepath(path_file, f_format):
            # 默认获取png图片
            all_path = [os.path.join(x[0], y)
                        for x in os.walk(path_file)
                        for y in x[2] if os.path.splitext(y)[1] == f_format]
            return all_path

        if not os.path.isdir(files):
            # 获取文件绝对路径，支持*.*模糊匹配
            actual_files = glob.glob(files)
        else:
            actual_files = _get_all_filepath(files, file_format)
        print("actual_files:", actual_files)
        return actual_files
