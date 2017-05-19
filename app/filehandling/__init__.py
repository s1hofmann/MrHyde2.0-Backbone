import base64
from binascii import Error as Base64Error
from os import makedirs
from os.path import join

from app import current_config


def create_diff_file(repo_id, diff):
    try:
        file_name = ''.join(['/tmp/', repo_id, '_patch.diff'])
        file_out = open(file_name, 'w')
    except IOError as e:
        if len(diff) > 20:
            diff = diff[:20]
        raise FileHandlingException("create_diff_file(%s, %s)" % (repo_id, diff), e.__str__())
    else:
        file_out.write(diff)
        file_out.close()
        return file_name


def deploy_error_page(deploy_path, error_type, error_msg):
    from jinja2 import FileSystemLoader, Environment
    template_loader = FileSystemLoader(searchpath=current_config.TEMPLATEDIR)
    template_env = Environment(loader=template_loader)
    error_page = template_env.get_template('error.html')
    try:
        makedirs(deploy_path, 0o755, True)
    except OSError:
        pass
    index_file_path = join(deploy_path, 'index.html')
    index_file = open(index_file_path, 'w')
    index_file.write(error_page.render(error=error_type, msg=error_msg))
    index_file.close()


def dispatch_static_files(deploy_path, files):
    for file in files:
        if 'path' not in file.keys() or 'data' not in file.keys():
            raise FileHandlingException("dispatch_static_files(%s)" % deploy_path, 'Unable to unmarshall data.')
        raw_path = file['path'].split('/')
        raw_data = file['data']
        file = raw_path[-1]
        data = None
        try:
            data = base64.standard_b64decode(raw_data)
        except Base64Error as exception:
            raise FileHandlingException("dispatch_static_files(%s)" % deploy_path, exception.__str__())
        rel_path = join(raw_path[0:-1])
        abs_path = join(deploy_path, rel_path)
        try:
            makedirs(abs_path, 0o755, True)
        except OSError:
            # We're good to go, output dir is present
            pass
        file_path = join(abs_path, file)
        with open(file_path, 'wb') as out:
            if data is not None:
                out.write(data)


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
