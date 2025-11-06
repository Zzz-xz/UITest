def get_remote_current_path(ssh) -> str:
    try:
        stdin, stdout, stderr = ssh.exec_command('pwd')
        result = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return result if not error else f"获取路径失败: {error}"
    except Exception as e:
        return f"获取路径失败: {str(e)}"
def get_remote_dir_files(ssh) -> str:
    try:
        stdin, stdout, stderr = ssh.exec_command('ls -l')
        result = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        return result if not error else f"获取文件列表失败: {error}"
    except Exception as e:
        return f"获取文件列表失败: {str(e)}"