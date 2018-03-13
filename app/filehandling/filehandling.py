import base64
import logging
from binascii import Error as Base64Error
from os import makedirs
from os.path import join
from shutil import copyfile

from app import current_config

LOGGER = logging.getLogger(__name__)


def create_diff_file(repo_id, diff):
    """
    Helper method which stores received patch data to a *.diff file in order to patch a repository.
    :param repo_id: Repository ID, used to generate a unique filename.
    :param diff: Contents of the *.diff file.
    :return: Absolute path to *.diff file
    """
    file_name = ''.join(['/tmp/', repo_id, '_patch.diff'])
    try:
        with open(file_name, 'w') as file_out:
            file_out.write(diff)
            file_out.close()
            return file_name
    except OSError as e:
        if len(diff) > 20:
            diff = diff[:20]
        raise FileHandlingException("create_diff_file(%s, %s)" % (repo_id, diff), e.__str__())


def deploy_error_page(deploy_path):
    """
    Helper method which deploys a static error page to a repositories deployment path.
    In case of an error during processing this page gets deployed to inform the user.
    :param deploy_path: Path to deploy the page to.
    :return: None
    """
    try:
        makedirs(deploy_path, 0o755, True)
        makedirs(join(deploy_path, 'static'), 0o755, True)
        copyfile(join(current_config.TEMPLATEDIR, 'error.html'), join(deploy_path, 'index.html'))
        copyfile(join(current_config.STATICDIR, 'layout.css'), join(deploy_path, join('static', 'layout.css')))
        copyfile(join(current_config.STATICDIR, 'ic_error.svg'), join(deploy_path, join('static', 'ic_error.svg')))
    except OSError as e:
        LOGGER.error("Unable to deploy static resources of error page. Reason: %s" % e.strerror)
        raise


def dispatch_static_files(deploy_path, files):
    """
    If a post contains 'static files' (e.g. images etc.), these files are added to the server request as a list of
    base64 encoded raw data. On the server side, these chunks of data are parsed and stored at the correct location
    relative to the deployment root.
    :param deploy_path: Deployment root
    :param files: List of file elements ( { path:
    :return:
    """
    for file in files:
        if 'path' not in file or 'data' not in file:
            raise FileHandlingException("dispatch_static_files(%s)" % deploy_path, 'Unable to unmarshall data.')
        raw_path = file['path'].split('/')
        raw_data = file['data']
        file_name = raw_path[-1]
        data = None
        try:
            data = base64.standard_b64decode(raw_data)
        except Base64Error as exception:
            raise FileHandlingException("dispatch_static_files(%s)" % deploy_path, exception.__str__())
        rel_path = '/'.join(raw_path[0:-1])
        abs_path = join(deploy_path, rel_path)
        try:
            makedirs(abs_path, 0o755, True)
        except OSError:
            # We're good to go, output dir is present
            pass
        file_path = join(abs_path, file_name)
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
