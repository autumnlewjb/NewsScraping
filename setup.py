from notify_run import Notify


def register_notify():
    reg = Notify()
    print('Register at {}'.format(reg.register().endpoint))

    input('Press Enter after registration')

    with open('registered.txt', 'w+') as output_file:
        output_file.write('1')
