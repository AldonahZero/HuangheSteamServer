def get_err(form):
    """
        获取form错误文本
    """
    error_list = []
    for item in form.errors.get_json_data().values():
        error_list.append(item[0].get('message'))
    err_str = '/'.join(error_list)
    return err_str
