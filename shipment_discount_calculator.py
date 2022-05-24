couriers = {
    #  Dictionary with couriers data
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
    # Default variables for calculation
    'prev_month': '00',
    'disc_limit': 10,  # Discount limit per month
    'disc_left': 0,
    'lp_l_count': 0,  # Number of LP company's L size shipments in given month
}


def output_data(shipment, discount_data, bad_input_data=False):  # Need to change name
    """
    Outputs shipment(list) and discount data(dict) if input data is correct.
    Here we also can save data to a specific file if necessary.
    """
    if bad_input_data:
        print(f"{' '.join(shipment)} Ignored")
    else:
        print(f"{' '.join(shipment)} "
              f"{float_to_str(discount_data['reduced_price'])} "
              f"{float_to_str(discount_data['discount'])}")
    # with open('result.txt', 'a') as result:
    #     result.write()


def check_month(shipment):
    """If shipment month is new resets discount data"""
    if shipment['tr_date'][1] != data['prev_month']:
        data['disc_left'] = data['disc_limit']
        data['prev_month'] = shipment['tr_date'][1]  # transaction month
        data['lp_l_count'] = 0
    else:
        pass


def float_to_str(float_arg):
    """If argument is float or integer converts it to string type number with 2 decimals"""
    try:
        return '{:.2f}'.format(float_arg)
    except:
        return float_arg


def calc_s_price(shipment):
    """Calculates S size package price and discount"""
    discount = couriers[shipment['courier']]['price_s'] - min_s_price()
    if discount == 0:
        discount_data = {
            'reduced_price': couriers[shipment['courier']]['price_s'],
            'discount': '-',
        }
        return discount_data

    elif data['disc_left'] - discount > 0:
        data['disc_left'] -= discount
        discount_data = {
            'reduced_price': min_s_price(),
            'discount': discount,
        }
        return discount_data

    else:
        discount = data['disc_left']
        data['disc_left'] = 0
        discount_data = {
            'reduced_price': couriers[shipment['courier']]['price_s'] - discount,
            'discount': discount,
        }
        return discount_data


def min_s_price():  # I think we need to implement this to check s size fnction
    s_price_list = []
    for courier in couriers:
        s_price_list.append(couriers[courier]['price_s'])
    return min(s_price_list)


def la_poste(shipment):
    match shipment['size']:
        case 'S':
            return calc_s_price(shipment)
        case 'M':
            discount_data = {
                'reduced_price': couriers['LP']['price_m'],
                'discount': '-',
            }
            return discount_data

        case 'L':
            data['lp_l_count'] += 1
            if data['lp_l_count'] == 3:
                discount = couriers['LP']['price_l']

                if data['disc_left'] - discount >= 0:
                    data['disc_left'] -= discount
                    discount_data = {
                        'reduced_price': 0,
                        'discount': discount,
                    }
                    return discount_data

                else:
                    discount = data['disc_left']
                    data['disc_left'] = 0
                    discount_data = {
                        'reduced_price': couriers['LP']['price_l'] - discount,
                        'discount': discount,
                    }
                    return discount_data

            else:
                discount_data = {
                    'reduced_price': couriers['LP']['price_l'],
                    'discount': '-',
                }
                return discount_data


def mondial_relay(shipment):
    match shipment['size']:
        case 'S':
            return calc_s_price(shipment)
        case 'M':
            discount_data = {
                'reduced_price': couriers['MR']['price_m'],
                'discount': '-',
            }
            return discount_data
        case 'L':
            discount_data = {
                'reduced_price': couriers['MR']['price_l'],
                'discount': '-',
            }
            return discount_data


def discount_calculator(input_file):
    """
    Main f-n, opens file and switch through the cases.
    Each case is for other courier.
    Handles exceptions.
    """
    with open(input_file, 'r', encoding='utf-8') as data_file:
        for transaction_line in data_file:  # line turi /n
            transaction_list = transaction_line.split()  # Splits string to list
            try:
                #  Trying make dict from list
                shipment = {
                    'tr_date': transaction_list[0].split('-'),
                    'size': transaction_list[1],
                    'courier': transaction_list[2]
                }
            except IndexError:
                #  Runs if not enough or not correct data in shipment is given.
                output_data(transaction_list, discount_data=None, bad_input_data=True)
            else:
                #  Runs if try block is ok
                #  Switches through courier cases
                check_month(shipment)
                match shipment['courier']:
                    case 'LP':
                        discount_data = la_poste(shipment)
                    case 'MR':
                        discount_data = mondial_relay(shipment)
                    case None:
                        raise Exception('No courier data found')

                output_data(transaction_list, discount_data)


discount_calculator('input.txt')
