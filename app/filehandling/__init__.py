# import base64
# from binascii import Error as Base64Error
# from os import makedirs, listdir
# from os.path import isfile, isdir, join
# from sqlite3 import Error as SQLError


def create_diff_file(repo_id, diff):
    try:
        file_name = ''.join(['/tmp/', repo_id, '_patch.diff'])
        file_out = open(file_name, 'w')
    except IOError as e:
        if len(diff) > 10:
            diff = diff[:10]
        raise FileHandlingException("create_diff_file(%s, %s)" % (repo_id, diff), e.__str__())
    else:
        file_out.write(diff)
        file_out.close()
        return file_name


# def file_download(self, repo_id, file_name):
#     repo_id = repo_id.split('/')[0]
#     if len(repo_id) > 1 and repo_id.split('/')[1:]:
#         file_path = repo_id.split('/')[1:][0]
#     else:
#         file_path = []
#
#     try:
#         database = dbhandler.DbHandler(self.cm().db_file())
#         repo_path = database.list('repo', 'path', "id='%s'" % repo_id)[0]
#         abs_path = '/'.join([repo_path, ''.join(file_path), file_name])
#         if isfile(abs_path):
#             return True
#         else:
#             return False
#     except OSError as exception:
#         raise
#     except SQLError as exception:
#         raise
#
#
# def deploy_error_page(self, deploy_path, error_type, error_msg):
#     if not isdir(deploy_path):
#         makedirs(deploy_path, 0o755, True)
#     index_file_path = join(deploy_path, 'index.html')
#     index_file = open(index_file_path, 'w')
#     index_file.write(template('list_view', rows=[error_msg], header=error_type))
#     index_file.close()
#
#
# def list_directory(path):
#     try:
#         repo_path = ''.join([self.__cm.base_dir, '/', path])
#         file_list = [f for f in listdir(repo_path)]
#         return file_list
#     except OSError as exception:
#         raise FileHandlingException("list_directory(%s)" % path, exception.strerror)
#
#
# def dispatch_static_files(deploy_path, files):
#     for file in files:
#         raw_path = file['path'].split('/')
#         raw_data = file['data']
#         file = raw_path[-1]
#         data = None
#         try:
#             data = base64.standard_b64decode(raw_data)
#         except Base64Error as exception:
#             logger.warning(exception.__str__())
#         rel_path = '/'.join(raw_path[0:-1])
#         abs_path = '/'.join([deploy_path, rel_path])
#         makedirs(abs_path, 0o755, True)
#         filepath = '/'.join([abs_path, file])
#         with open(filepath, 'wb') as out:
#             if data is not None:
#                 out.write(data)


class FileHandlingException(Exception):
    def __init__(self, cmd, msg):
        self._cmd = cmd
        self._msg = msg
        if cmd is not None and msg is not None:
            Exception.__init__(self, "Error performing %s. More details: %s" % (cmd, msg))
        elif cmd is not None:
            Exception.__init__(self, "Error performing %s." % cmd)
        else:
            Exception.__init__(self, "Error performing file operation.")

    @property
    def msg(self):
        return self._msg

    @property
    def cmd(self):
        return self._cmd
