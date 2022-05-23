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
    'prev_month': '00',
    'disc_limit': 10,
    'disc_left': 0,  # by default
    'lp_l_count': 0,
    'disc_ship': '',
    'price_ship': '',
}


def save(data_ln, *args, **kwargs):
    print(f"{' '.join(data_ln)} {' '.join([arg for arg in args])}")


def check_month(trans):  # or better call it check month?
    if trans['tr_date'][1] != data['prev_month']:
        data['disc_left'] = data['disc_limit']
        data['prev_month'] = trans['tr_date'][1]  # transaction month
        data['lp_l_count'] = 0
    else:
        pass


def fl_to_str(float_nr):
    """Takes float nr and returns string with 2 decimals"""
    return '{:.2f}'.format(float_nr)


def check_s_price(trans):
    """Checks s size package discount, out data we will change later with return"""
    disc = couriers[trans['courier']]['price_s'] - min_s_price()
    if disc == 0:
        data['price_ship'] = fl_to_str(couriers[trans['courier']]['price_s'])  # formating float to string
        data['disc_ship'] = '-'
    elif data['disc_left'] - disc > 0:
        data['disc_left'] -= disc
        data['price_ship'] = fl_to_str(min_s_price())
        data['disc_ship'] = fl_to_str(disc)
    else:
        disc = data['disc_left']
        data['disc_left'] = 0
        data['price_ship'] = fl_to_str(couriers[trans['courier']]['price_s'] - disc)
        data['disc_ship'] = fl_to_str(disc)


def min_s_price():  # I think we need to implement this to check s size fnction
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
            data['lp_l_count'] += 1
            if data['lp_l_count'] == 3:
                disc = couriers['LP']['price_l']
                if data['disc_left'] - disc >= 0:
                    data['disc_left'] -= disc
                    data['price_ship'] = fl_to_str(0)
                    data['disc_ship'] = fl_to_str(disc)
                else:
                    disc = data['disc_left']
                    data['disc_left'] = 0
                    data['price_ship'] = fl_to_str(couriers['LP']['price_l'] - disc)
                    data['disc_ship'] = fl_to_str(disc)
            else:
                data['price_ship'] = fl_to_str(couriers['LP']['price_l'])
                data['disc_ship'] = '-'


def mondial_relay(trans):
    match trans['size']:
        case 'S':
            check_s_price(trans)
        case 'M':
            pass
        case 'L':
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
            save(data_ln, 'Ignored')
        else:
            check_month(trans)
            match trans['courier']:
                case 'LP':
                    la_poste(trans)
                case 'MR':
                    mondial_relay(trans)
                case None:
                    print('No courier data found')
            save(data_ln, data['price_ship'], data['disc_ship'])
