try:
    print('out try')
    try:
        2/0
        print('inner try')
    except:
        print('inner ex')
except:
    print('oter ex')
    