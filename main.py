from data_engineering import DataEngineering

CONFIG_FILE_NAME = 'config.yaml'


def main():
    data_engineering = DataEngineering()

    try:
        data_engineering.setup(CONFIG_FILE_NAME)
    except ValueError as e:
        print(e)
        return

    data_engineering.run()
    # db_manager.create_init_status('ERR6004692', False, 'user_777', 'bufuktepe@gmail.com')
    # db_manager.create_init_status('ERR6004724', True, None, None)
    # db_manager.create_init_status('ERR6004725', False, 'user_777', 'bufuktepe@gmail.com')


if __name__ == '__main__':
    main()