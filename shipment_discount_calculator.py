couriers = {
    'LP': {
        'name': 'La Poste',
        'price_s': 1.5,
        'price_m': 4.9,
        'price_l': 6.9,
    },
    'MR': {
        'name': 'Mondial Relay',
        'price_s': 2,
        'price_m': 3,
        'price_l': 4,
    }
}
data = {
    'prev_month': '01',
    'disc_limit': 10,
    'disc_left': 0, #by default
}



def check_disc(trans): # or better call it check month?
    if trans['tr_date'][1] != data['prev_month']:
        data['disc_left'] = data['disc_limit']
        data['prev_month'] = trans['tr_date'][1]  # transaction month
    else:
        pass


def check_s_price(trans):
    '''Checks s size package discount, out data we will change later with return'''
    disc = couriers[trans['courier']]['price_s'] - min_s_price()
    if disc == 0:
        out_data = {
            'price': couriers[trans['courier']]['price_s'],  # gal reikes paversti i stringa
            'disc': '-',
        }
        print(out_data)
    elif data['disc_left'] - disc > 0:
        data['disc_left'] -= disc
        out_data = {
            'price': min_s_price(),
            'disc': disc,
        }
        print(out_data)
    else:
        disc = data['disc_left']
        data['disc_left'] = 0
        out_data = {
            'price': couriers[trans['courier']]['price_s'] - disc,
            'disc': disc
        }
        print(out_data)


def min_s_price(): # I think we need to implement this to check s size fnction
    s_prc_list = []
    for courier in couriers:
        s_prc_list.append(couriers[courier]['price_s'])
    return min(s_prc_list)


def la_poste(trans):
    match trans['size']:
        case 'S':
            check_s_price(trans)
        case 'M':
            pass
        case 'L':
            pass
    print('LP')


def mondial_relay(trans):
    pass


with open('input.txt', 'r', encoding='utf-8') as data_file:
    for data_ln in data_file:  # line turi /n
        data_ln = data_ln.split()  # PERDARO I LISTA IR PASALINA LISNUS \N
        try:
            trans = {
                'tr_date': data_ln[0].split('-'),
                'size': data_ln[1],
                'courier': data_ln[2]
            }
        except:
            print('Ignored')
        else:
            check_disc(trans)
            print(data)
            match trans['courier']:
                case 'LP':
                    la_poste(trans)
                case 'MR':
                    mondial_relay(trans)
                case None:
                    print('No courier found')
