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
    'input_file': 'input.txt',
    'prev_month': '00',
    'disc_limit': 10,
    'disc_left': 0,  # by default
    'lp_l_count': 0,
    'disc_ship': 0,
    'price_ship': 0,
}


def save(data_ln, ignored=False):
    if ignored:
        print(f"{' '.join(data_ln)} Ignored")
    else:
        print(f"{' '.join(data_ln)} "
              f"{float_to_str(data['price_ship'])} "
              f"{float_to_str(data['disc_ship'])}")
    # with open('result.txt', 'a') as result:
    #     result.write(f'{result_ln}\n')


def check_month(trans):  # or better call it check month?
    if trans['tr_date'][1] != data['prev_month']:
        data['disc_left'] = data['disc_limit']
        data['prev_month'] = trans['tr_date'][1]  # transaction month
        data['lp_l_count'] = 0
    else:
        pass


def float_to_str(float_nr):
    """If argument is float or integer f-n converts it to string type float with 2 decimals"""
    try:
        return '{:.2f}'.format(float_nr)
    except:
        return float_nr


def check_s_price(trans):
    """Checks s size package discount, out data we will change later with return"""
    disc = couriers[trans['courier']]['price_s'] - min_s_price()
    if disc == 0:
        data['price_ship'] = couriers[trans['courier']]['price_s']  # formating float to string
        data['disc_ship'] = '-'
    elif data['disc_left'] - disc > 0:
        data['disc_left'] -= disc
        data['price_ship'] = min_s_price()
        data['disc_ship'] = disc
    else:
        disc = data['disc_left']
        data['disc_left'] = 0
        data['price_ship'] = couriers[trans['courier']]['price_s'] - disc
        data['disc_ship'] = disc


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
                    data['price_ship'] = 0
                    data['disc_ship'] = disc
                else:
                    disc = data['disc_left']
                    data['disc_left'] = 0
                    data['price_ship'] = couriers['LP']['price_l'] - disc
                    data['disc_ship'] = disc
            else:
                data['price_ship'] = couriers['LP']['price_l']
                data['disc_ship'] = '-'


def mondial_relay(trans):
    match trans['size']:
        case 'S':
            check_s_price(trans)
        case 'M':
            pass
        case 'L':
            pass


def discount_calculator(input_file):
    with open(input_file, 'r', encoding='utf-8') as data_file:
        for data_ln in data_file:  # line turi /n
            data_ln = data_ln.split()  # PERDARO I LISTA IR PASALINA LISNUS \N
            try:
                trans = {
                    'tr_date': data_ln[0].split('-'),
                    'size': data_ln[1],
                    'courier': data_ln[2]
                }
            except:
                save(data_ln, ignored=True)
            else:
                check_month(trans)
                match trans['courier']:
                    case 'LP':
                        la_poste(trans)
                    case 'MR':
                        mondial_relay(trans)
                    case None:
                        print('No courier data found')
                save(data_ln)


discount_calculator(data['input_file'])
